import csv
import json
import re
import argparse

questionsqueries_path = 'questions_queries.json'

SQL_KEY_WORDS = ['select','where','from','count','top', 'order','like','=','<','>','=<','>=','<=','=>',
'limit','select', 'max','and','or','min','desc','acs','average','is','*','convert',
'else','distinct']
IGNORE = ['(', ')']

# SQL_KEY_WORDS = [' '+w+' ' for w in SQL_KEY_WORDS]
	


def getWord(query,word):
	'''
	Returs word how it is written in the query\
	E.g. getWord('Select Name FROM Table','select') returns 'Select'
	'''
	idx_w = query.lower().find(word.lower())
	if idx_w >= 0:
		w = query[idx_w:idx_w+len(word)]
		return w
	else:
		return False

def preprocessWordsInQuotes(query):
	split_at = ['"',"'"]
	for c in split_at:
		if query.count(c)>0 and query.count(c) % 2 == 0:
			splited = query.split(c)
			splited = [x for x in splited if x]
			# if len(splited)%2 == 0:
			query = ''
			is_like = False
			for i, elt in enumerate(splited):
				if i%2 == 1 and not is_like:
					new_elt = elt.replace(' ','_')
					# print('New elet in quotes: '+new_elt)					
				else:
					if getWord(elt,'LIKE') or getWord(elt,'=') or getWord(elt,' is '):
						is_like = True
					else:
						is_like = False
					new_elt = elt
					new_elt = re.sub('([()])', r' \1 ', new_elt)
					# print('New elt NOT in quotes: '+new_elt)		
				query += new_elt 
				if i<len(splited)-1 or (i>=len(splited)-1 and query.count('"')%2 == 1):
					query += '"'
		# elif c == "'":
		# 	query = re.sub('([()])', r' \1 ', query)
	# if "'" not in query and '"' not in query:
	# 	query = re.sub('([()])', r' \1 ', query)
	return query

def replaceQuotesWithDoubleQuotes(query):
	new_words = list()
	for w in query.split():
		if w[0]=="'" and w[len(w)-1]=="'":
			new_word = '"'+w[1:len(w)-1]+'"'
		else:
			new_word = w
		new_words.append(new_word)
	query = ' '.join(new_words)
	return query

def replaceTablename(query,table_name,verbose=False):
	'''
	We want the table name:
	- to match the one listed in the csv (given as parameter - spaces are replaced by _).
	- to be surrounded by " " (in case it starts with a number).
	'''
	try :
		if table_name not in query:
			w = getWord(query,'from')
			splited = query.split(w)
			query = splited[0]
			## replace all table names if there are several
			for i in range(1,len(splited)):
				replace_name_bool = True
				mystr = splited[i].lstrip()
				if mystr[0] == '(':
					replace_name_bool = False
				elif mystr[0] == "'":
					split_char = "'"
					mystr = mystr[1:]
				elif mystr[0]=='"':
					split_char = '"'
					mystr = mystr[1:]
				else :
					split_char = ' '
				if replace_name_bool:
					mystr = mystr.replace(mystr.split(split_char)[0],'"'+table_name+'"',1)
					mystr = mystr.replace(table_name+'"\'',table_name+'"',1)
					mystr = mystr.replace(table_name+'""',table_name+'"',1)
					query +=  'FROM ' + mystr
		return query
	except TypeError as e:
		if verbose:
			print('ERR when looking for "from" in:')
			print(query)
			print(e)
		return query
	

def doubleQuotesAfter(query,after_word):
	'''
	Need to set double quotes around col headers in case it starts with a number.
	If the word immediately after ' after_word' is key word, don't treat it. E.g. query = SELECT TOP, after_word = select --> don't put quotes around TOP.
	'''
	w = getWord(query,after_word)
	if w:
		splited = query.split(w)
		query = splited[0]
		for j in range(1,len(splited)):
			mystr = splited[j].strip()
			words = re.split(' |,',mystr) 
			new_words = list()
			next_key_word, last_part = None, None
			for word in words:
				word = word.strip()
				if word == '':
					pass
				# Do not process anything after the next key word.
				elif word[0] == '"':
					new_words.append(word)
				elif word.lower() in SQL_KEY_WORDS:
					next_key_word = getWord(mystr,word+' ')
					if not next_key_word:
						next_key_word = ''
					last_part = mystr.split(next_key_word, 1)[1]
					break
				# Do not change the words in IGNORE
				elif word.lower() in IGNORE:
					new_words.append(word)
				# Process (add double quotes) to other words
				else:
					# word = re.sub(r'[^\w\s]','',word)
					if word[0] in ['"',"'"] and word[-1] in ['"',"'"]:
						word = word[1:-1]
					new_words.append('"'+word+'"')
			## reconstruct query:
			query += ' '+after_word+' '
			num_new_words = len(new_words)
			for i, new_word in enumerate(new_words):
				query += new_word 
				# add a coma i) if it's not the last word ii) if it's not a word to ignore and iii) if the next word is not to ignore
				if i < num_new_words -1 and new_word not in IGNORE and new_words[i+1] not in IGNORE:
					query += ', '
			# put back together the rest of the query
			if next_key_word:
				query += ' ' + next_key_word + last_part
			elif last_part:
				query += last_part
	query = query.strip()
	return query


def doubleQuotesForEveryNonKeyWord(query):
	splited = query.split()
	splited_small_caps = query.lower().split()
	new_query = ''
	for i in range(0,len(splited)):
		w = splited[i]
		w_small_caps = splited_small_caps[i]
		if w_small_caps not in SQL_KEY_WORDS:
			new_query += ' "'+w+'"'
		else:
			new_query += ' '+w
	return new_query


def percentageInLike(query):
	'''
	WHERE "Name" LIKE "%Boston%" ---> WHERE "Name" LIKE "%%Boston%"
	'''
	w = getWord(query,'LIKE')
	if w:
		splited = query.split(w)
		query = splited[0]
		for j in range(1,len(splited)):
			mystr = splited[j].lstrip()
			# add a second % sign if there is already one
			if mystr[0:2] == "'%" or mystr[0:2] == "\"%":
				mystr = mystr[0:2] + '%' + mystr[2:]
			# add 2 % signs if there are none
			else:
				mystr = mystr[0:1] + '%%' + mystr[1:]
			# add % sign at the end if there is none
			splited2 = mystr.split('"')
			if len(splited2)>1:
				mystr2 = splited2[1]
				if mystr2[-1] != '%':
					mystr2 = mystr2 + '%'
				splited2[1] = mystr2
				mystr = '"'.join(splited2)
			query += ' LIKE ' + mystr
	return query


def preprocessTOP(query):
	## if mutiple sapces, remove them
	query = re.sub(' +',' ',query)
	## find if "select top" is in query
	w = getWord(query,'SELECT TOP')
	if w:
		idx_top = query.find(w) + len('SELECT ')
	## find if it is followed by a number and memorize it.
		limit_num = query[idx_top+len('top ')]	
	## if last char is ;, delete it
		if query[-1] == ';':
			query = query[0:-1]	
	## add Limit at the of the query
		if limit_num.isdigit():
			len_span_to_delete = len('top 1 ')
			query += ' LIMIT ' + limit_num
			j = idx_top+len('top 1 ')
		else:
			len_span_to_delete = len('top ')
			query += ' LIMIT 1'
			j = idx_top+len('top ')
		## special case where * is missing...
		if query[j:j+len('FROM')].lower() == 'from':
			query = 'SELECT * ' + query[len('SELECT '):]
			idx_top += 2
	## delete Top + limit_num
		query = query[0:idx_top] + query[idx_top+len_span_to_delete:]
	return query

def removeQuotes(query):
	'''
		Remove quotes surrounding ASC, DESC, COUNT, MAX, AVG, MIN, AVERAGE
	'''
	line = re.sub(r'\"(ASC|DESC)\"', r'\1', query)
	line = re.sub(r'\"((COUNT)\((.*)\))\"', r'\1', line)
	line = re.sub(r'\"((MAX)\((.*)\))\"', r'\1', line)
	line = re.sub(r'\"((AVG)\((.*)\))\"', r'\1', line)
	line = re.sub(r'\"((MIN)\((.*)\))\"', r'\1', line)
	line = re.sub(r'\"((AVERAGE)\((.*)\))\"', r'\1', line)
	line = re.sub(r'SELECT AVERAGE', r'SELECT AVG', line)
	line = line.replace('" is "', '" = "')
	return line

def addColumnOrderBy(query):
	column_search = re.search(r'(SELECT|Select|select)( )*(\"[^\"]+\") (FROM|from|From)', query, re.IGNORECASE)
	column = ""
	if column_search:
		column = column_search.group(3)
		# print(column)
	line = query.replace('ORDER BY  ASC', 'ORDER BY '+column+' ASC')
	line = line.replace('ORDER BY  DESC', 'ORDER BY '+column+' DESC')
	line = line.replace(', ASC', ' ASC')
	return line

def queryForSQLParser(query, csv_path,verbose=False):
	for_SQL_parser = dict()
	try:
		with open(csv_path) as csv_file:
			csv_reader = csv.reader(csv_file)
			row_counter = 0
			for row in csv_reader:
				if row_counter == 0:
					table_name = row[0]
				elif row_counter == 1:
					column_names = row
				else:
					break
				row_counter += 1
			for_SQL_parser["table_name"] = table_name
			new_name = 'Table_1'
			query  = replaceTablename(query,new_name)
			for_SQL_parser["query"] = query.replace('"'+new_name+'"',new_name)
			for_SQL_parser["column_names"] =column_names
	except IOError as e:
		if verbose:
			print('ERR open csv')
			print(e)
	return for_SQL_parser


def preprocessQuery(query,csv_path,verbose=False,debug=False):

	table_name = None
	## add spaces before and after ( )
	# query = re.sub('([.,!?()])', r' \1 ', query) ---> increases error rate.
	query = preprocessWordsInQuotes(query)
	if debug:
		print('preprocessWordsInQuotes')
		print(query)
	query = replaceQuotesWithDoubleQuotes(query)
	if debug:
		print('preprocess query0, replaceQuotesWithDoubleQuotes')
		print(query)

	# query = re.sub('([()])', r' \1 ', query)
	try:
		with open(csv_path) as csv_file:
			csv_reader = csv.reader(csv_file)
			for row in csv_reader:
				table_name = row[0]
				# print('table_name from csv :'+table_name)
				break
		if table_name:
			query = replaceTablename(query,table_name)

		if debug:
			print('preprocessQuery1 replaceTablename')
			print(query)
		try:
			query = preprocessTOP(query)
			if debug:
				print('preprocessQuery2 preprocessTOP')
				print(query)
			query = doubleQuotesAfter(query,' MAX (')
			if debug:
				print('preprocessQuery3 doubleQuotesAfter MAX (')
				print(query)
			query = doubleQuotesAfter(query,' MIN (')
			if debug:
				print('preprocessQuery3_bis doubleQuotesAfter MIN (')
				print(query)
			query = doubleQuotesAfter(query,'SELECT ')  
			if debug:
				print('preprocessQuery4 doubleQuotesAfter SELECT')
				print(query)
			query = doubleQuotesAfter(query,' WHERE ')
			if debug:
				print('preprocessQuery5 doubleQuotesAfter WHERE')
				print(query)
			query = doubleQuotesAfter(query,' ORDER BY ')
			if debug:
				print('preprocessQuery6 doubleQuotesAfter ORBER BY')
				print(query)
			query = doubleQuotesAfter(query,' AND ')
			if debug:
				print('preprocessQuery6 doubleQuotesAfter AND')
				print(query)
			query = doubleQuotesAfter(query,' OR ')
			if debug:
				print('preprocessQuery6 doubleQuotesAfter OR')
				print(query)
			query = percentageInLike(query)
			if debug:
				print('preprocess percentageInLike')
				print(query)
			query = removeQuotes(query)
			if debug:
				print('preprocess removeQuotes surrounding ASC, DESC, COUNT, MAX, MIN')
				print(query)
			query = addColumnOrderBy(query)
			if debug:
				print('preprocess addColumnOrderBy')
				print(query)
		except ValueError as e:
			if verbose:
				print('ERR query preprocessing!')
				print(query)
				print(e)

	except IOError as e:
		if verbose:
			print('ERR open csv')
			print(e)

	return query

def main(dataset_json):

	f =  open(dataset_json, 'r')
	content = json.load(f)

	for ex in content:
		sql = ex['sql_transpose']
		id = ex['id']
		csv_path = ('/transposed_csvs/'+id.__str__()+'.csv')
		final_sql = preprocessQuery(sql,csv_path)
		ex['final_sql'] = final_sql

	f.close()

	with open(dataset_json, 'w') as f:
		json.dump(content,f,indent=1)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Preprocess newly generated SQL for type 2 tables.')
	parser.add_argument('dataset', metavar='dataset', type=str, help='Train or test dataset?')	
	args = parser.parse_args()

	main(args.dataset)

	# with open(questionsqueries_path) as qqf:

	# 	content = json.load(qqf)
	# 	c = content['10'] #305
	# 	query = c['query']
	# 	csv_path = c['dirname'] + '/table.csv'
	# 	print('Unpreprocessed query')
	# 	print(query)
	# 	query = preprocessQuery(query,csv_path,debug=True)
	# 	print(query)

