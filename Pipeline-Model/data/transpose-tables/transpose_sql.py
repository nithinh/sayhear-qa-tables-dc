import json
import argparse
import csv

def preprocess_likeword(s):
	s = s.replace('%',' ')
	s = s.replace('"', '')
	s = s.replace('_', ' ')
	s = s[:-1] if s[-1] == ';' else s
	s = s.strip()
	s = s.lower()
	return s

def get_like_word(sql):	
	like_word = False
	for i,elt in enumerate(sql):
		if elt == 'LIKE' or elt=='=':
			like_word = preprocess_likeword(sql[i+1])
			break
	return like_word

def get_table_name(sql):
	table_name = False
	for i,elt in enumerate(sql):
		if elt.lower() == 'from':
			table_name = sql[i+1]
			break
	return table_name


def main(dataset_json):

	f =  open(dataset_json, 'r')
	content = json.load(f)

	f_master =  open('master_json.json', 'r')
	content_master = json.load(f_master)


	for ex in content:
		if ex['table_type'] == 2:
			id = ex['id']
			sql_transpose = False

			ex_master = content_master[id.__str__()]
			preprocessed_query = ex_master['preprocessed_query'].split()
			like_word = get_like_word(preprocessed_query)
			table_name = get_table_name(preprocessed_query)
			if like_word and table_name:				

				like_header_list = list()
				dataset = 'test' if 'test' in dataset_json else 'train'
				with open('../data/tables/'+dataset+'/original tables/'+id.__str__()+'.csv', 'r') as f_csv:
					csv_reader = csv.reader(f_csv)
					for i,row in enumerate(csv_reader):
						if i == 1:
							j = 0
							while ('link' in row[j].lower() or 'url' in row[j].lower()):
								j += 1
						elif i >1 :
							if like_word in row[j].decode('utf-8').lower():
								like_header_list.append(row[j])

					if len(like_header_list) != 1 :
						# print('--------------- PROBLEM WITH !! ---------------')
						print(id,like_word,like_header_list)
					else:
						sql_transpose = 'SELECT "'+like_header_list[0]+'" FROM "'+table_name+'"'
						sql_transpose = sql_transpose.split()

			elif like_word:
				print('ERR id %d, no table name:%s'%(id,' '.join(preprocessed_query)))

			elif table_name:
				print('ERR id %d, no like or = clause.'%id)

			else:
				print('ERR id %d, no like or = clause and no table name.'%id)

		else:
			sql_transpose = ex['newsql']

		if sql_transpose:
			ex['sql_transpose'] = ' '.join(sql_transpose)

	f.close()

	with open(dataset_json, 'w') as fout:
		json.dump(content,fout,indent=1)


if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='Tranpose the SQL for type 2 to type 1 table.')
	parser.add_argument('dataset_json', metavar='dataset_json', type=str, help='Path to the json file for which to transform the queries.')	
	args = parser.parse_args()

	main(args.dataset_json)