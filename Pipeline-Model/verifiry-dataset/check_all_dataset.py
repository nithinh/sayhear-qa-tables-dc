import json
import csv
import argparse
import sql_tables
import tokenize as tk
import sys
sys.path.insert(0, '../select-clause-pb/features/nb-of-col-and-word-vectors-features/tools/')
# import tools
# import helper_functions as helper
import proximity_fct as pfct
sys.path.insert(0, '../data/transpose-tables/')
import re


def preprocess_query(query):
	if query[-1] == ';':
		query = query[:-1]
	splited_query = query.split('"')
	for i, elt in enumerate(splited_query):
		if 'order_by' in elt.lower() and i % 2 == 0 :
			query = query.replace('order_by','ORDER BY')
			query = query.replace('ORDER_BY','ORDER BY')	
		if 'limit_1' in elt.lower() and i % 2 == 0 and 'order by' in query.lower():
			query = query.replace('LIMIT_1','LIMIT 1')
			query = query.replace('limit_1','LIMIT 1')
		if 'descending' in elt.lower() and i % 2 == 0 and 'order by' in query.lower():
			query = query.replace('descending','DESC')
			query = query.replace('DESCENDING','DESC')
		if 'ascending' in elt.lower() and i % 2 == 0 and 'order by' in query.lower():
			query = query.replace('ascending','ASC')
			query = query.replace('ASCENDING','ASC')
	return query

class QuitException(Exception):
	pass

def save(dataset,content,id):
	f =  open('sayhearfall2018_'+dataset+'.json', 'w')
	content = json.dump(content,f,indent=1)
	f.close()
	with open('last_id_checked.txt', 'w') as f:
		f.write(id.__str__())

def quit(dataset,content,id):
	id -= 1
	save(dataset,content,id)
	print('Saved sayhearfall2018_'+dataset+'.json')
	print('Last id checked:%d'%id)
	# sys.exit(0)
	raise QuitException 

def add_note(ex):
	text = raw_input('\nDo you want to add a note to this example? (y/n)\n')
	b = True
	while b:
		if text == 'Y' or text == 'y' or text == '1':
			text = raw_input('Type in your note\n')
			ex['note'] = text
			print('Note added.')
			b = False
			return
		elif text != 'N' and text != 'n' and text != '0':
			print("This is not a valid answer.")
			text = raw_input('\nDo you want to add a note to this example? (y/n)\n')
		else:
			return

def display_error(dataset,content,ex,id,question,query,expected_answer):
	print('ERROR')
	print('id: %d'%id)
	print('question: %s'%question)
	print('sql tilde operator: %s'%query)
	print('expected answer: %s'%expected_answer)
	ex['ex_valid'] = False
	try:
		while True:
			text = raw_input('\nContinue? (y/n)\n')
			if text == 'Y' or text == 'y' or text == '1':
				add_note(ex)
				return True
			elif text == 'N' or text == 'n' or text == '0':
				quit(dataset,content,id)
			else:
				print('This is not a valid answer.')
		print('\n\n--------------------------------')
	except QuitException:
		raise QuitException

def validate_example(dataset,content,ex,id,question,query,new_query,expected_answer,answer):
	print('id: %d'%id)
	print('question: %s'%question)
	print('sql tilde operator: %s'%query)
	print('generated sql: %s'%new_query)
	print('expected answer: %s'%expected_answer)
	print('predicted answer: %s'%answer)
	try:
		while True:
			text = raw_input('\nDo you want to validate this example? (y/n/q (quit))\n')
			if text == 'Y' or text == 'y' or text == '1':
				return True
			elif text == 'N' or text == 'n' or text == '0':		
				add_note(ex)	
				return False
			elif text == 'Q' or text == 'q':
				quit(dataset,content,id)
			else:
				print('This is not a valid answer.')
		print('\n\n--------------------------------')
	except QuitException:
		raise QuitException


def get_words_tilde_operator(sql):
	if '~' not in sql:
		return False
	sql = sql.split()
	headers_and_words = list()
	for i,w in enumerate(sql):
		if w.lower() == '~':
			header = sql[i-1]
			if sql[i+1][0] == '"' and sql[i+1][-1] != '"':
				sql_after_tilde = ' '.join(sql[i+1:])
				sql_after_tilde_splited_at_quotes = sql_after_tilde.split('"')
				word = sql_after_tilde_splited_at_quotes[1]
			else:
				word = sql[i+1]
			header = header.replace('"','')
			word = word.replace('"','')
			headers_and_words.append([header,word])
	if len(headers_and_words) == 0:
		print('ERR, cannot find any related word.')
	return headers_and_words

def new_word_tilde_operator_2(header,word,csv_path,proximity_fct=pfct.proximityAvg_strings,word2vec=None):
	'''
	new_word_tilde_operator_2: finds the most similar word to "word" in the column "header" of the csv  according to the score computed by proximity_fct.
	1) Find the index of the column in which to look for similar word
	2) for each cell of the column, measures the proximity with "word"
	3) returns the words with the highest proximity
	'''
	with open(csv_path,'r') as f:
		csv_reader = csv.reader(f)
		col_idx = -1	
		max_sim = -1
		max_word = None
		for i,row in enumerate(csv_reader):
			if i == 1:
				for j,h in enumerate(row):
					if h == header:
						col_idx = j
						break
				if col_idx == -1:
					print('Error: cannot find header %s'%header)
					return False
			elif i>1:
				if word2vec:
					sim = proximity_fct(word,row[col_idx],word2vec)
				else:
					sim = proximity_fct(word,row[col_idx])
				if sim > max_sim:
					max_sim = sim
					max_word = row[col_idx]
		return max_word
	print('ERROR cannot find csv')

def proximity_fct_extact_match(s1,s2):
	if s1.decode('utf-8') == s2.decode('utf-8'):
		return 1
	elif s1.decode('utf-8') in s2.decode('utf-8'):
		return 0.5
	else:
		return -1


def new_word_tilde_operator(header,word,csv_path,word2vec):
	'''
		new_word_tilde_operator: finds the most similar word to "word" in the column "header" of the csv applying several strategies.
		Strategies to compute similarity between "word" and cell content:
			1) use word vectors. 
			2) use exact match on "word" (word vectors do not work for digits).
			3) use exact match on the number present in "word".
	'''
	max_word = new_word_tilde_operator_2(header,word,csv_path,proximity_fct=pfct.proximityAvg_strings,word2vec=word2vec)
	if max_word:
		return max_word
	else:
		max_word = new_word_tilde_operator_2(header,word,csv_path,proximity_fct=proximity_fct_extact_match,word2vec=None)
		if max_word:
			# print('hehre.... found extact match')
			# print(max_word)
			return max_word
		else:
			numbers = [int(s) for s in re.findall(r'-?\d+\.?\d*', word)]
			# print(numbers)
			if len(numbers) == 1:
				max_word = new_word_tilde_operator_2(header,numbers[0].__str__(),csv_path,proximity_fct=proximity_fct_extact_match,word2vec=None)
				if max_word : 
					return max_word
	print('new_word_tilde_operator: did not find any solution!')


def write_like_clause(sql,i,words,type):
	header = sql[i-1]
	if type == 'medium':
		sql[i-1] = ' (' + sql[i-1] 
		new_words = '"%% ' + words + ' %" OR ' + header + ' LIKE "' + words + ' %" OR ' + header + ' LIKE "%% ' + words + '" OR ' + header + ' LIKE "'+ words + '") '
	elif type == 'easy':
		new_words = '"%%' + words + '%"'
	elif type == 'hard':
		new_words = '"' + words + '"'
	else :
		print('write_like_clause ERR: wrong type!! (%s)'%type)
		return False
	return new_words


def replace_tilde_operator_and_words(sql,operator=None,new_word=None,like_clause_type=None):
	'''
	In the SQl, replaces the words in the tilde operator with new words.
	If no new words are specified, just adds % at the biginning and the end of the current word
	'''
	# print('in replace_tidle_words_with_new_words')
	sql = sql.split()
	new_sql = list()
	for i,w in enumerate(sql):
		if w.lower() == '~':
			## Replace ~ if asked
			if operator:
				sql[i] = operator
			## There is more than one word to replace (more than one word in double quotes, so we'll work by splitting the SQL on quotes)
			if sql[i+1][0] == '"' and sql[i+1][-1] != '"':
				sql_after_tilde = ' '.join(sql[i+1:])
				sql_after_tilde_splited_at_quotes = sql_after_tilde.split('"')
				## Replace with the provided new word if there is one (the operator would be =)
				if new_word:
					sql_after_tilde_splited_at_quotes[1] = '"'+new_word.decode('utf-8')+'"'
				## If there is not new word, we might need to change the form of the LIKE condition
				elif operator == 'LIKE':
					## Force spacing before and/or after the word(s) in LIKE
					words = sql_after_tilde_splited_at_quotes[1]
					new_words = write_like_clause(sql,i,words,type = like_clause_type)
					sql_after_tilde_splited_at_quotes[1] = new_words

				new_sql = ' '.join(sql[:i+1]) + sql_after_tilde_splited_at_quotes[1] 
				if len(sql_after_tilde_splited_at_quotes) > 2 :
					new_sql += '"'.join(sql_after_tilde_splited_at_quotes[2:])
				# print('replace_tilde_operator_and_words 1')
				# print(new_sql)
			elif new_word:
				sql[i+1] = ('"'+new_word+'"').decode('utf-8')
				new_sql = ' '.join(sql)
			elif operator == 'LIKE':
				words = sql[i+1][1:-1]
				new_words = write_like_clause(sql,i,words,type=like_clause_type)
				sql[i+1] = new_words 
				new_sql = ' '.join(sql)
				# print('replace_tilde_operator_and_words 2')
				# print(new_sql)
			break
	# print(sql)
	while new_word == None and '~' in new_sql: # replace all = and LIKE operators
		new_sql = replace_tilde_operator_and_words(new_sql,operator,new_word,like_clause_type)
	if len(new_sql) == 0:
		new_sql = ' '.join(sql)
	return new_sql


def get_new_query_by_replacing_tilde_words_with_new_words(dataset,content,ex,id,query,csv_path,word2vec):
	if '~' not in query:
		return query
	headers_and_words = get_words_tilde_operator(query)
	# print(headers_and_words)
	if len(headers_and_words) == 0:
		try:
			display_error(dataset,content,ex,id,' '.join(ex['question_parsed']),ex['final_sql'],ex['short_a'])
			return False
		except QuitException:
			raise QuitException
	else:
		new_query = query
		for [header,word] in headers_and_words:
			new_word = new_word_tilde_operator(header,word,csv_path,word2vec)
			# print(new_word)
			if new_word:
				new_query = replace_tilde_operator_and_words(new_query,operator='=',new_word=new_word)
				# return new_query
			else :
				print('ERR: could not find new word for %s in column %s'%(word,header))
				return False
		return new_query

def check_or_recheck(mode,ex,predicted_answer,dataset=None,content=None,id=None,question=None,query=None,new_query=None,expected_answer=None,automatic_validation=False):
	try:
		if mode == 'first_check':
			ex_valid = validate_example(dataset,content,ex,id,question,ex['final_sql'],new_query,expected_answer,predicted_answer)
			ex['ex_valid'] = ex_valid
			if ex_valid:
				ex['sql_res'] = predicted_answer
		elif mode == 'recheck':
			v = validate(ex,new_query,predicted_answer,automatic_validation)
			return v
	except QuitException:
		raise QuitException



def check_ex(mode,dataset,content,ex,id,word2vec):
	if mode == 'recheck' and ex['ex_valid']==False:
		return True

	query = ex['final_sql']
	query = preprocess_query(query)
	csv_path = '../data/tables/'+dataset+'/transposed_csvs/'+id.__str__()+'.csv'

	try:
		# print(query)
		new_query = replace_tilde_operator_and_words(query,operator='=')
		# print('lkajhntgiosrhgois')
		# print(new_query)
		query_res = sql_tables.testQuery(new_query,csv_path,verbose=False)
		v = False
		if query_res:
			v = check_or_recheck(mode,ex,query_res,dataset,content,id,' '.join(ex['question_parsed']),query,new_query,ex['short_a'])
		else:
			new_query = replace_tilde_operator_and_words(query,operator='LIKE',like_clause_type='hard')
			query_res = sql_tables.testQuery(new_query,csv_path,verbose=False)
			if query_res:
				v = check_or_recheck(mode,ex,query_res,dataset,content,id,' '.join(ex['question_parsed']),query,new_query,ex['short_a'])
			else:
				new_query = replace_tilde_operator_and_words(query,operator='LIKE',like_clause_type='medium')
				query_res = sql_tables.testQuery(new_query,csv_path,verbose=False)
				if query_res:
					v = check_or_recheck(mode,ex,query_res,dataset,content,id,' '.join(ex['question_parsed']),query,new_query,ex['short_a'])
				else:
					new_query = replace_tilde_operator_and_words(query,operator='LIKE',like_clause_type='easy')
					query_res = sql_tables.testQuery(new_query,csv_path,verbose=False)
					if query_res:
						v = check_or_recheck(mode,ex,query_res,dataset,content,id,' '.join(ex['question_parsed']),query,new_query,ex['short_a'])
					else:
						new_query = get_new_query_by_replacing_tilde_words_with_new_words(dataset,content,ex,id,query,csv_path,word2vec)
						if new_query:			
							query_res = sql_tables.testQuery(new_query,csv_path,verbose=False)
							v = check_or_recheck(mode,ex,query_res,dataset,content,id,' '.join(ex['question_parsed']),query,new_query,ex['short_a'])
						else:
							question = ' '.join(ex['question_parsed'])
							print('id: %s\nquestion: %s\nsql tilde operator: %s\ngenerated sql: unable to generate a SQL query that returns something.\n\nExample automatically rejected.'%(id,question,ex['final_sql']))
							ex['ex_valid'] = False
							add_note(ex)
		return v
	except QuitException:
		raise QuitException

def print_bad_result_when_validating(expected,got,query):
	print('Excepted:')
	print(expected)
	print('Got:')
	print(got)
	print('Query executed:')
	print(query)

def validate(ex,query,query_res,automatic_validation=False):
	if automatic_validation and not query_res :
		return False
	if query_res == False:
		print_bad_result_when_validating(ex['sql_res'],False,query)
		return False
	query_res = [list(a) for a in query_res]
	print(query_res)
	query_res_unicode = list()
	for sublist in query_res:
		query_res_unicode.append([elt.decode('utf-8') for elt in sublist])
	if automatic_validation:
		return query_res_unicode == ex['sql_res']
	else:
		if query_res_unicode == ex['sql_res']:
			return True
		else:
			print_bad_result_when_validating(ex['sql_res'],query_res,query)
			return False


def read_last_id_checked():
	with open('last_id_checked.txt','r') as f:
		last_id_checked = int(f.read())
	return last_id_checked

def main(dataset,word2vec,table_type=None,recheck_previous_ex = True):
	print('table_type')
	print(table_type)
	# print('word2vec')
	# print(word2vec)

	f =  open('sayhearfall2018_'+dataset+'.json', 'r')
	content = json.load(f)
	f.close()

	id = -1

	all_previously_validaed_ex_are_OK = True
	first_new_ex = True

	for ex in content:
		# print(ex['id'])
		cond = True
		if table_type and (ex['table_type'] != int(table_type)):
			cond = False
		if cond:
			try:
				id = ex['id']
				# print(id)
				if id > read_last_id_checked():

					## if it's the first new example we re checking, print message about previous examples (if they are all OK)
					if recheck_previous_ex:
						if first_new_ex and all_previously_validaed_ex_are_OK:
							print('\n-------------------------------------------------------')
							print('\nAll previously validated examples are still working :-D\n')
							print('-------------------------------------------------------\n')
							first_new_ex  = False
					else:
						if first_new_ex:
							print('\n-------------------------------------------------------')
							print('\n /!\\ Quick pass: did NOT recheck previous examples!! /!\\ \n')
							print('-------------------------------------------------------\n')
							first_new_ex  = False


					_ = check_ex('first_check',dataset,content,ex,id,word2vec)

					save(dataset,content,id)
					print('\n')

				else:
					# pass
					if recheck_previous_ex:
						recheck_value = check_ex('recheck',dataset,content,ex,id,word2vec)
						if recheck_value == False:
							all_previously_validaed_ex_are_OK = False
							text = raw_input('----- WARNING: Example %d does not work anymore. Want to continue? (y/n)\n'%id)
							if text == 'N' or text == 'n':
								return


			except QuitException:
				return

if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='Manually check the whole dataset.')
	parser.add_argument('dataset', metavar='dataset', type=str, help='train or test')
	parser.add_argument('--table_type', metavar='table_type', nargs='?', const='none', type=str, help='Pass table type (1 or 2) if you want to focus on a particular one.')
	args = parser.parse_args()
	word2vec = pfct.load_model("../select-clause-pb/features/nb-of-col-and-word-vectors-features/GoogleNews-vectors-negative300.bin")
	main(args.dataset,word2vec,args.table_type)