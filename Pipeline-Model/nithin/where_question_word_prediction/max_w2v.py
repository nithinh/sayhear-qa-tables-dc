import csv
import re
import os

import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import pickle
import os
import csv
import re
import argparse
import gensim.models.keyedvectors as word2vec
import sys
sys.path.append("../")
import config
import time
import pickle
import math
import numpy as np
from scipy.spatial import distance

from nltk import metrics, stem, tokenize

 

stemmer = stem.PorterStemmer()
 
def normalize(s):
    words = tokenize.wordpunct_tokenize(s.lower().strip())
    return ' '.join([stemmer.stem(w) for w in words])
 
def fuzzy_match(s1, s2, model1):
    x = 0.0
    if s1 in model1.wv.vocab and s2 in model1.wv.vocab:
        x = model1.similarity(s1,s2)
    elif s2 in model1.wv.vocab and s1 not in model1.wv.vocab:
        x = model1.similarity('##',s2)
    elif s1 in model1.wv.vocab and s2 not in model1.wv.vocab:
        x = model1.similarity(s1,'##')

    if x is None:
        x = - np.inf

    return x



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
	#stop_words = set(stopwords.words('english'))
	#data = [word for word in data if word not in stop_words]
	#ps = PorterStemmer()
	#data = [ps.stem(word) for word in data]
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
    #train_question_filename = "preprocessed_train_question_list.pkl"
    train_questions_file=config.data_root + "train_question.txt"  
    qsns = []
    with open(train_questions_file) as f:
        lines = f.readlines()

    for line in lines:
        line = line.split(':')[1].strip()
        qsns.append(line)
    #with open(train_question_filename, 'rb') as f:
    #    train_questions_processed = pickle.load(f)
    #print(qsns)
    
    #print(train_questions_processed)
    train_tables_list = os.listdir(config.train_tables)
    
    w2v_feature_train = csv.writer(open("w2v_col_q_pair_train_new.csv", 'w'), delimiter=',',lineterminator='\n')
    w2v_feature_train.writerow(["id question", "q_word", "w2v"])

    pathToBinVectors = 'GoogleNews-vectors-negative300.bin'

    print ("Loading the data file... Please wait...")
    model1 = word2vec.KeyedVectors.load_word2vec_format(pathToBinVectors, binary=True)
    
    # offset = qsns[0]
    
    for x,train_table in enumerate(train_tables_list):
        
        table_index = x #int(train_table.split('.')[0])
 
        train_table_filename = config.train_tables + str(table_index) + ".csv"
        train_table = open(train_table_filename, 'r', encoding="utf8")
        
        if True: #table_index == 40: #table_index != 221 and table_index != 24 and table_index != 77:
            reader = csv.reader(train_table)
            table_name = next(reader)
            header_list = next(reader)
            
            
            num_of_row = sum(1 for row in reader)

            column_header_list = process_column(config.train_tables, table_index, include_header = False, include_contents = True)
            column_header_list = np.array(column_header_list)
            #print(column_header_list)
            #question_processed = train_questions_processed[table_index]
            
            best_match_value = np.inf
            best_match_column_header = ""
            
            question_processed = qsns[x].split()
            print (question_processed)
            #time.sleep(50)
            for q in question_processed:
                #print (column_header_list)

                if True: #q not in list(['alexa', 'what', 'how', 'who', 'where', 'when','', 'i', 'the']):                                                  
                    for i in range(len(column_header_list)):  
                        list_d = column_header_list[i]
                        max_match_distance = 0.0
                        max_i_index = -1
                        if ("http" not in list_d) and ("https" not in list_d) and ("www." not in list_d):                           
                            for d in list_d:      
                                match_distance=0                
                                match_distance = fuzzy_match(d, q, model1)
                                if max_match_distance < match_distance:
                                    max_match_distance = match_distance
                w2v_feature_train.writerow([table_index, q, max_match_distance])
                print([table_index, q, max_match_distance])
                
            print ("-------------------")
        
                
