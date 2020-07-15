# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 21:58:28 2018

@author: Fan Hu
"""

import pickle
import math
import numpy as np
import argparse
import csv
import json 
from scipy.spatial import distance
    
def term_freq (document):
    dict_tf = dict()
    total_word = 0
    for word in document:
        if word.strip() != "": 
            total_word += 1
            if word not in dict_tf:
                dict_tf[word] = 1
            else:
                dict_tf[word] += 1
    for word in dict_tf:
        dict_tf[word] = dict_tf[word]/float(total_word)
    return dict_tf

def inverse_doc_freq (all_documents):
    dict_idf = dict()
    total_documents = len(all_documents)
    for document in all_documents:
        set_words = set()
        for word in document:
            if word.strip() != "":
                set_words.add(word)
        
        for word in set_words:        
            if word not in dict_idf:
                dict_idf[word] = 1
            else:
                dict_idf[word] += 1
    for word in dict_idf:
        dict_idf[word] = 1.0 + math.log(float(total_documents)/dict_idf[word])
    return dict_idf   
  
def cosine_sim (vector_q, vector_d):
    dot_product = np.dot(vector_q, vector_d)
    vector_q_norm = np.sqrt(np.dot(vector_q, vector_q))
    vector_d_norm = np.sqrt(np.dot(vector_d, vector_d))
    if vector_q_norm == 0.0:
        return 0.0
    elif vector_d_norm == 0.0:
        return 0.0
    else:
        return dot_product/(vector_q_norm*vector_d_norm)

def dot_product (vector_q, vector_d):
    dot_product = np.dot(vector_q, vector_d)

    return dot_product

def inverse_euclidean (vector_q, vector_d):
    dst = distance.euclidean(vector_q, vector_d)
    
    return 1.0/dst
    
    
def tf_idf (question, all_documents, mode = 'cosine_sim'):
    idf_dict = inverse_doc_freq(all_documents)

    tf_dict_q = term_freq(question)
    
    vector_q = []
    for word in question:
        if word.strip() != "":
            tf = tf_dict_q[word]
            if word in idf_dict:
                idf = idf_dict[word]
            else:
                idf = 0.0
            vector_q.append(tf*idf)

    score_array = []
    
    for document in all_documents:
        
        tf_dict_d = term_freq(document)
        vector_d = []
        for word in question:
            if word.strip() != "":
                if word in tf_dict_d:
                    tf = tf_dict_d[word]
                else:
                    tf = 0.0
                    
                if word in idf_dict:
                    idf = idf_dict[word]
                else:
                    idf = 0.0
                
                vector_d.append(tf*idf)
    
        if mode == 'cosine_sim':
            score = cosine_sim(vector_q, vector_d)
        elif mode == 'dot_product':
            score = dot_product(vector_q, vector_d)
        elif mode == 'inverse_euclidean':
            score = inverse_euclidean(vector_q, vector_d)
            
        score_array.append(score) 
    return np.array(score_array)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Generates accuracy information based tf-idf vectors and their cosine similarity")
    ap.add_argument("-tr", "--train_tables", required=True,
        help="path for the data in the training set tables in the pickle format")
    ap.add_argument("-qtr", "--train_question", required=True,
        help="path for data in the training set questions in the pickle format")
    ap.add_argument("-te", "--test_tables", required=True,
        help="path for the data in the tables in the pickle format")
    ap.add_argument("-qte", "--test_question", required=True,
        help="path for data in the questions in the pickle format")
    ap.add_argument("-o", "--out", required=False,
        help="path for output csv file")
    ap.add_argument("-res", "--results", required=False,
        help="path for output json file with results")

    args = vars(ap.parse_args())

    train_table_filename = args["train_tables"]#"preprocess/preprocessed_train_table_list.pkl"
    train_question_filename = args["train_question"]#"preprocess/preprocessed_train_question_list.pkl"
    
    test_table_filename = args["test_tables"]#"preprocess/preprocessed_test_table_list.pkl"
    test_question_filename = args["test_tables"]#"preprocess/preprocessed_test_question_list.pkl"
    
    with open(train_table_filename, 'rb') as f:
        train_tables = pickle.load(f)
        
    with open(train_question_filename, 'rb') as f:
        train_questions = pickle.load(f)

    with open(test_table_filename, 'rb') as f:
        test_tables = pickle.load(f)
        
    with open(test_question_filename, 'rb') as f:
        test_questions = pickle.load(f)


    all_tables = []
    all_questions = []

    res_p_at_10 = dict()
    
    for table in train_tables:
        all_tables.append(table)
    for table in test_tables:
        all_tables.append(table)        

    for question in train_questions:
        all_questions.append(question)
    for question in test_questions:
        all_questions.append(question)

   
    top_N = 1
    correct_cosine_sim = 0
    correct_dot_product = 0
    correct_inverse_euclidean = 0
 
    
    total = 0
    outA = [["id","rank_cs","rank_dp","rank_ie"]];
    for i in range(len(train_questions)):
        total += 1
        question = train_questions[i]

        res_p_at_10[i] = dict()

        cosine_sim_array = tf_idf(question, train_tables, 'cosine_sim')
        cosine_sim_array_sorted_idx = list(cosine_sim_array.argsort())
        cosine_sim_array_sorted_idx.reverse()
        res_p_at_10[i]['cosine_sim'] = [int(v) for v in cosine_sim_array_sorted_idx[0:9]]

        dot_product_array = tf_idf(question, train_tables, 'dot_product') 
        dot_product_array_sorted_idx = list(dot_product_array.argsort())
        dot_product_array_sorted_idx.reverse()
        res_p_at_10[i]['dot_product'] = [int(v) for v in dot_product_array_sorted_idx[0:9]]

        inverse_euclidean_array = tf_idf(question, train_tables, 'inverse_euclidean') 
        inverse_euclidean_array_sorted_idx = list(inverse_euclidean_array.argsort())
        inverse_euclidean_array_sorted_idx.reverse()
        res_p_at_10[i]['inverse_euclidean'] = [int(v) for v in inverse_euclidean_array_sorted_idx[0:9]]
  
        predicted_label_cosine_sim = cosine_sim_array.argsort()[-top_N:][::-1][0]
        print(predicted_label_cosine_sim)
        predicted_label_dot_product = dot_product_array.argsort()[-top_N:][::-1][0]
        predicted_label_inverse_euclidean = inverse_euclidean_array.argsort()[-top_N:][::-1][0]
        
        match_cosine_sim = False
        match_dot_product = False  
        match_inverse_euclidean = False 
        
        if i in cosine_sim_array.argsort()[-top_N:][::-1]:
            match_cosine_sim = True
        if i in dot_product_array.argsort()[-top_N:][::-1]:
            match_dot_product = True        
        if i in inverse_euclidean_array.argsort()[-top_N:][::-1]:
            match_inverse_euclidean = True
        
        table_cs = (-cosine_sim_array).argsort()
        table_dp = (-dot_product_array).argsort()
        table_ie = (-inverse_euclidean_array).argsort()
        # print(i,table_list)
        
        r_cs = 0
        r_dp = 0
        r_ie = 0
        j = 0
        for table_id in table_cs:
            if(i == table_id):
                r_cs = j+1
                #(i,",",position + 1)
                break
            j +=1
        j = 0
        for table_id in table_dp:
            if(i == table_id):
                r_dp = j+1
                #(i,",",position + 1)
                break
            j +=1
        j = 0
        for table_id in table_ie:
            if(i == table_id):
                r_ie = j+1
                #(i,",",position + 1)
                break
            j +=1
        outA.append([i,r_cs,r_dp,r_ie])

        if match_cosine_sim:
            correct_cosine_sim += 1
        if match_dot_product:
            correct_dot_product += 1
        if match_inverse_euclidean:
            correct_inverse_euclidean += 1
    # print(csv)
    if args["out"]:
        with open(args["out"], mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in outA:
                csv_writer.writerow(row)

    if args["results"]:
        # print(res_p_at_10)
        with open(args["results"], 'w') as json_file:
            json.dump(res_p_at_10,json_file,indent=1)


    print("Cosine Sim:")        
    print(float(correct_cosine_sim)/total)
    print("Dot Product:")        
    print(float(correct_dot_product)/total)
    print("Inverse Euclidean:")        
    print(float(correct_inverse_euclidean)/total)
                   
 