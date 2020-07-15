import csv
import json
import numpy as np
import argparse
import os

import sys
sys.path.insert(0, '../tools/')
import helper_functions as helper

def basic_csv(path_to_json,path_to_csv_directory,path_to_output_csv):

	f = open(path_to_json,'r')
	content  = json.load(f)

	X = list()

	for ex in content:
		
		id = ex['id']

		table_file_path = path_to_csv_directory + id.__str__()+'.csv'
		with open(table_file_path, 'r') as ftable:
			reader = csv.reader(ftable)

			## we need one example per column for one table.
			example_list = list()

			for i,row in enumerate(reader):
				if i == 1:

					## get select clause
					query = ex['final_sql'].encode('utf-8')
					query = helper.replace_star(id,query,row)
					select_clause = helper.get_select_clause(query)

					## check if we have duplicates col_headers
					duplicates_bool = helper.duplicates_in_list(row)
					if duplicates_bool:
						print('WARNING: we have duplicate column headers for example %d'%id)

					if select_clause:
						for header in row:
							## is header in SELCT ?
							header_in_select = 1 if header in select_clause else 0

							## new example
							x = list()
							x.append(id)
							x.append(header)
							x.append(header_in_select)

							X.append(x)

					else:
						print('ERROR: cannot find select clause for example %d.\nQuery is:%s\n'%(id,query))

	features = ['id question','col_header','col_header in select clause']


	with open(path_to_output_csv, 'w') as f:
		csvwriter = csv.writer(f)
		csvwriter.writerow(features)
		for row in X:
			csvwriter.writerow(row)
		print('Generated basic csv --> %d examples'%(len(X)))


def combine_csvs(path_to_basic_csv,path_to_feature_csvs_directoy):

	new_csv_dict = dict()

	path_to_output_csv = path_to_feature_csvs_directoy+'final_csv_projection.csv'
	if os.path.exists(path_to_output_csv):
		os.remove(path_to_output_csv)

	with open(path_to_basic_csv,'r') as f_basic:
		csv_reader = csv.reader(f_basic)
		for row in csv_reader:
			new_csv_dict[row[0],row[1]] = row


	csvs = [path_to_feature_csvs_directoy+f for f in os.listdir(path_to_feature_csvs_directoy) if os.path.isfile(path_to_feature_csvs_directoy+f) and (path_to_feature_csvs_directoy+f) != path_to_basic_csv]
	print('Will merge CSVS:')
	print(csvs)
	for csv_file_path in csvs:
		with open(csv_file_path,'r') as csv_f:
			csv_reader = csv.reader(csv_f)
			for row in csv_reader:
				key = row[0],row[1]
				if key not in new_csv_dict.keys():
					print('ERROR, element %s does not correspond to anything in basic CSV. The problem is coming from file %s.'%(key,csv_file_path))
					return
				else:
					r = list(row)
					new_csv_dict[key] = new_csv_dict[key] + r[2:]

	## Re order examples
	new_csv_list = list()
	with open(path_to_basic_csv,'r') as f_basic:
		csv_reader = csv.reader(f_basic)
		for row in csv_reader:
			new_csv_list.append(new_csv_dict[row[0],row[1]])
			

	with open(path_to_output_csv,'w') as f_out:
		csvwriter = csv.writer(f_out)
		for row in new_csv_list:
			csvwriter.writerow(row)
	print('\nWrote final CSV combining all features in %s --> %d examples'%(path_to_output_csv,len(new_csv_list)-1))
	print('Total number of features: %d'%(len(new_csv_list[0])-3))





if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='Generate CSV with feartures for ML.')
	parser.add_argument('path_to_json', metavar='path_to_json', type=str, help='Path to the json file of the dataset.')
	parser.add_argument('path_to_csv_tables_directory', metavar='path_to_csv_tables_directory', type=str, help='Path to the directory with the csv of the tables.')
	parser.add_argument('path_to_feature_csvs_directoy', metavar='path_to_feature_csvs_directoy', type=str, help='Path to the folder that contains the csv files with the features.')
	
	args = parser.parse_args()

	path_to_basic_csv = args.path_to_feature_csvs_directoy + 'basic.csv'

	basic_csv(args.path_to_json,args.path_to_csv_tables_directory,path_to_basic_csv)

	combine_csvs(path_to_basic_csv,args.path_to_feature_csvs_directoy)