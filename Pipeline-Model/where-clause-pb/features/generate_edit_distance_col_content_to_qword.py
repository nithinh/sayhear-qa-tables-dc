import csv
import re
import os
import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle
import numpy as np
from nltk import stem, tokenize
from nltk.metrics import edit_distance
 
stemmer = stem.PorterStemmer()
 
def normalize(s):
    words = tokenize.wordpunct_tokenize(s.lower().strip())
    return ' '.join([stemmer.stem(w) for w in words])
 
def fuzzy_match(s1, s2):
    return edit_distance(normalize(s1), normalize(s2))

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
    question_filename = sys.argv[2]
    first_question_index = int(sys.argv[3])
    output_filename = sys.argv[4]
        
    with open(question_filename, 'rb') as f:
        questions_processed = pickle.load(f)

    tables_list = os.listdir(tables_dir)
    
    csvfile = open(output_filename, 'w')
    
    edit_distance_feature = csv.writer(csvfile, delimiter=',',lineterminator='\n')
    edit_distance_feature.writerow(["id question", "col_header", "q_word", "min_edit_distance_col_content_to_q"])
    
    for table_file in tables_list:
        
        table_index = int(table_file.split('.')[0])
 
        table_filename = tables_dir + str(table_index) + ".csv"
        table = open(table_filename, 'r', encoding="utf8")
        
        reader = csv.reader(table)
        table_name = next(reader)
        header_list = next(reader)
        num_of_row = sum(1 for row in reader)

        column_content_list = process_column(tables_dir, table_index, include_header = False, include_contents = True)
        column_content_list = np.array(column_content_list)

        question_processed = questions_processed[table_index-first_question_index]
        
        best_match_value = np.inf
        best_match_column_header = ""
        
        for q in question_processed:
            if q not in list(['alexa', 'what', 'how', 'who', 'where', 'when','', 'i', 'the']):                                                  
                for i in range(len(column_content_list)):  
                    list_d = column_content_list[i]
                    min_match_distance = np.inf
                    min_i_index = -1
                    if ("http" not in list_d) and ("https" not in list_d) and ("www." not in list_d):                           
                        for d in list_d:                        
                            match_distance = fuzzy_match(d, q)
                            if match_distance < min_match_distance:
                                min_match_distance = match_distance  
                    edit_distance_feature.writerow([table_index, header_list[i], q, min_match_distance])
    csvfile.close()
                                