from __future__ import print_function
import sqlite3
import csv
import json
import preprocess_sql
import sys
import os
import argparse



verbose = True

class SQLqueries():
	def __init__(self):
		self.create_query = 'CREATE TABLE '
		self.insert_query = 'INSERT INTO '
		self.drop_query = 'DROP TABLE '
		self.table_name = None

	def setTableName(self,tableName):
		self.create_query += "'"+tableName+"'"+'('
		self.insert_query += "'"+tableName+"'"+'('
		self.drop_query += "'"+tableName+"'"
		self.table_name = tableName


	def renameDuplicateHeaders(self,headers):
		headers = [h.lower() for h in headers]
		headers_wo_duplicates = set(headers)
		# print(headers_wo_duplicates)
		if headers == headers_wo_duplicates :
			return headers
		else:
			new_headers = list()
			seen = dict()
			for h in headers:
				# print(h,seen.keys())
				if h not in seen.keys():
					new_headers.append(h)
					seen[h] = 1
				else:
					seen[h] += 1
					new_headers.append(h+' '+seen[h].__str__())
			# print(new_headers)
			return new_headers



	def createQuery(self,csv_row):
		lrow = len(csv_row)
		for j, elt in enumerate(csv_row):
			self.create_query += "'"+elt+"'" + ''' TEXT'''
			self.insert_query += "'"+elt+"'"
			if j < lrow - 1:
				self.create_query += ', '
				self.insert_query += ', '
		self.insert_query += ') VALUES('
		for j in range(lrow-1):
			self.insert_query += '?,'
		self.insert_query += '?)'
		self.create_query += ' )'
		return self.create_query

	def paramsInsertQuery(self,csv_row,verbose):
		params = list()
		for elt in csv_row:
			try:
				params.append(elt.encode('utf-8'))
			except UnicodeDecodeError as e:
				if verbose:
					print('ERR, encoding error')
					print(e)
		return params

try:
	cursor.execute('''DROP TABLE mytable''')
	db.commit()
except:
	True

csvtable_path = 'output/http___locations_thecheesecakefactory_com_tx_austin-188_html_sayanc_20_4_2018@17_55_18/table.csv'
wrapper_path = 'output/http___locations_thecheesecakefactory_com_tx_austin-188_html_sayanc_20_4_2018@17_55_18/wrapper.txt'
questionsqueries_path = 'questions_queries.json'



def csv2sqlTable(db,cursor,sqlqueries,csvtable_path,verbose):

	try:
		with open(csvtable_path,'rb') as f:
			reader = csv.reader(f)
			for i, row in enumerate(reader):
				try:
					row =  [unicode(cell, 'utf-8') for cell in row]
				except UnicodeDecodeError:
					if verbose:
						print('ERR unicode')
						print(e)
				try:
					if i == 0:
						## table name
						sqlqueries.setTableName(row[0].lstrip())
					elif i == 1:
						## column headers
						row = sqlqueries.renameDuplicateHeaders(row)
						query = sqlqueries.createQuery(row)
						case = 1
						cursor.execute(query)
					else:
						## insert elements
						query = sqlqueries.insert_query
						case = 2
						try :
							cursor.execute(query,sqlqueries.paramsInsertQuery(row,False))
						except sqlite3.ProgrammingError as e:
							if verbose:
								print('ERR: table creation.')
								print(e)									
					db.commit()
				except sqlite3.OperationalError as e:
					if verbose:
						print('ERR: table creation.')
						print(e)
						if case == 1:
							print(query)
						else:
							print(query,sqlqueries.paramsInsertQuery(row))
	except IOError as e:
		if verbose:
			print('ERR open csv')
			print(e)



def executeQuery(cursor,sqlqueries,query,verbose=False):
	# if sqlqueries.table_name not in query:
	# 	query = replaceTablenameQuery(query)
	try:
		cursor.execute(query)
		# print(cursor)
		res = cursor.fetchall()
		# if verbose:
		# print('Res = ')
		# print(res)
		if len(res) == 0:
			return False
		else:
			return res
		# if res is not None:
		# 	return True
		# else: 
		# 	if verbose:
		# 		print("Result is None")
		# 	return None
		# print('QUERY')
		# print(query)
	except sqlite3.OperationalError as e:
		if verbose:
			print('\nERR query execution')
			print(e)
			# print(query)
		return False
	except sqlite3.Warning  as w:
		if verbose:
			print('\nERR query execution')
			# print(w)
			# print(query)
		return False


def dropLastTable(db,cursor,sqlqueries,verbose=False):
	try:
		cursor.execute(sqlqueries.drop_query)
		db.commit()
	except sqlite3.OperationalError as e:
		if verbose:
			print('ERR in drop tale')
			print(e)
			print(sqlqueries.drop_query)

def testQuery(query,csvtable_path,verbose=False):
	print(query, csvtable_path)
	if os.path.exists(csvtable_path):
		db = sqlite3.connect(':memory')
		db.text_factory = str
		cursor = db.cursor()

		sqlqueries = SQLqueries()

		csv2sqlTable(db,cursor,sqlqueries,csvtable_path,verbose)
		
		res =  executeQuery(cursor,sqlqueries,query,verbose)

		dropLastTable(db,cursor,sqlqueries)
		db.close()

	else:
		res = 'No CSV file'
	return res


def testLoop(db,cursor,save_errors_in=False,details=None):
	with open(questionsqueries_path) as qqf:

		content = json.load(qqf)

		c_exec_OK = 0

		num_err = 0
		no_csv = 0
		error_list = list()

		entry_num = len(content)
		error_writer = open("new_error.log","w")
		for i in range(entry_num):
			c = content[i.__str__()]
			query = c['query']
			short_a = c['short_a']
			csvtable_path = c['dirname'] + '/table.csv'
			print(csvtable_path)
			if os.path.exists(csvtable_path):

				sqlqueries = SQLqueries()

				# query = ''' select "Name", "2018_Population" from "Table_1"  where Name LIKE '%%Boston%%' '''
				csv2sqlTable(db,cursor,sqlqueries,csvtable_path,False)
				
				# preprocessed_query = preprocess_sql.replaceTablename(query,sqlqueries.table_name)
				preprocessed_query = preprocess_sql.preprocessQuery(query,csvtable_path)
				# print(preprocessed_query)

				if executeQuery(cursor,sqlqueries,preprocessed_query,False):
					c_exec_OK += 1
				else: 
					if not executeQuery(cursor,sqlqueries,query,False):
						num_err += 1
						error_list.append(i)
						print('\n\n ----- %d ------\n'%i)
						print('\nERR')
						print('Query = '+query)
						print('preprocessed_query = '+preprocessed_query+'\n')
						error_writer.write(str(i) +"\n")
						error_writer.write('Query = '+query.encode("utf-8") + "\n")
						error_writer.write('Preprocessed Query = '+ preprocessed_query.encode("utf-8") + "\n")

				dropLastTable(db,cursor,sqlqueries)

			else:
				print('\nERR: no CSV file.')
				no_csv += 1
				# num_err += 1

			sys.stdout.write('\rErrors: %d for number %d (Error rate = %.2f%%)'%(num_err,i+1,100*float(num_err)/(i+1)))
			sys.stdout.flush()

		print('\n\n--------------\n\n')
		print('Errors: %d in a total of %d entries (Error rate = %.2f%%)'%(num_err,entry_num+1,100*float(num_err)/(entry_num+1)))
		print('CSV files missing: %d in a total of %d entries (Error rate = %.2f%%)'%(no_csv,entry_num+1,100*float(no_csv)/(entry_num+1)))
		print('\nQuery properly executes and returns something for %d examples.'%c_exec_OK)

		if save_errors_in:
			print('\nSaving list of errors in '+str(save_errors_in))
			with open(save_errors_in,'w') as f:
				f.write(details+'\n')
				for i in error_list:
					f.write(i.__str__()+'\n')

def test(db,cursor):
	with open(questionsqueries_path) as qqf:

		content = json.load(qqf)


		c = content['135']
		query = c['query']
		short_a = c['short_a']
		csvtable_path = c['dirname'] + '/table.csv'

		sqlqueries = SQLqueries()

		print(query)
		csv2sqlTable(db,cursor,sqlqueries,csvtable_path,True)

		preprocessed_query = preprocess_sql.preprocessQuery(query,csvtable_path)
		# query = '''SELECT President FROM TABLE WHERE Date = (SELECT MAX(Date) FROM TABLE)'''
		preprocessed_query = 'SELECT  "Reduced_Quantity" FROM "To_make_1/3_of_a_recipe"  WHERE  "Quantity"  LIKE "%%1/4 cup%"'

		print(preprocessed_query)
		executeQuery(cursor,sqlqueries,preprocessed_query,True)

		dropLastTable(sqlqueries)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Tokenize a database')
	parser.add_argument('save_errors_in', metavar='save_errors_in', nargs='?', type=str, help='File in which you want to save the list of errors.')
	parser.add_argument('details', metavar='details', nargs='?', type=str, help='You can provide details about what you were testing when saving the list of errors.')

	args = parser.parse_args()


	db = sqlite3.connect(':memory')
	db.text_factory = str
	cursor = db.cursor()
	# testLoop(db,cursor,args.save_errors_in,args.details)

	testLoop(db,cursor)






