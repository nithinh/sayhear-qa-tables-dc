import csv
import re
import os
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
import sys
 
def preprocess(header, contents, include_header = False, include_contents = True):
	raw_data = []
	if include_header:
		raw_data.append(header)
	if include_contents:
		raw_data += contents
	data = []
	for item in raw_data:
		words = re.split(r'[^0-9a-zA-Z]', item)
		for word in words:
			if word not in ["", None]:
				data.append(word)
	stop_words = set(stopwords.words('english'))
	data = [word for word in data if word not in stop_words]
	ps = PorterStemmer()
	data = [ps.stem(word) for word in data]
	return data


def load_tables(table_path):
	with open(table_path, encoding="utf8") as f:
		reader = csv.reader(f)
		table_name = next(reader)
		headers = next(reader)
		rows = []
		for row in reader:
			rows.append(row)
		columns = []
		for col_index in range(len(rows[0])):
			columns.append([])
			for row in rows:
				if row[col_index]=="":
					continue
				columns[col_index].append(row[col_index])
	return columns, headers

def process_column(table_directory, table_index, include_header = False, include_contents = True):
	columns, headers = load_tables(table_directory + "{}.csv".format(table_index))
	column_words_bag_list = [preprocess(headers[i], columns[i], include_header, include_contents) for i in range(len(columns))]
	return column_words_bag_list



if __name__ == "__main__":

    tables_dir = sys.argv[1]
    output_filename = sys.argv[2]
    
    tables_list = os.listdir(tables_dir)
    csvfile = open(output_filename, 'w')
    average_cell_length_feature = csv.writer(csvfile, delimiter=',',lineterminator='\n')
    average_cell_length_feature.writerow(["id question","col_header","average_cell_length"])
    
    for table_file in tables_list:
        
        table_index = int(table_file.split('.')[0])
        
        table_filename = tables_dir + str(table_index) + ".csv"
        table = open(table_filename, 'r', encoding="utf8")
        
        reader = csv.reader(table)
        table_name = next(reader)
        header_list = next(reader)
        num_of_row = sum(1 for row in reader)

        column_header_list = process_column(tables_dir, table_index, include_header = False, include_contents = True)
        column_header_list = np.array(column_header_list)
        
        for i in range(len(column_header_list)):           
            list_d = column_header_list[i]
            total_length = len(list_d)
            average_length = float(total_length)/num_of_row

            average_cell_length_feature.writerow([table_index, header_list[i], average_length])               
    csvfile.close()
