# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 21:58:28 2018

@author: Fan Hu
"""

import pickle
import math
import numpy as np
import json
import csv
import os
from texttable import Texttable
    
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
  
def cosine_sim (question, document):
    dot_product = np.dot(question, document)
    question_norm = np.sqrt(np.dot(question, question))
    document_norm = np.sqrt(np.dot(document, document))
    if question_norm == 0.0:
        return 0.0
    elif document_norm == 0.0:
        return 0.0
    else:
        return dot_product/(question_norm*document_norm)

def tf_idf (question, all_documents):
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

    cosine_sim_array = []
    
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
    
        cosine_sim_array.append(cosine_sim(vector_q, vector_d)) 
    return np.array(cosine_sim_array)
 
    
def print_vectors(question, all_documents, actual_index, predicted_index):
    
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
    
    predicted_table = train_tables[predicted_index]

    tf_dict_d_predicted = term_freq(predicted_table)
    vector_d_predicted = []
    for word in question:
        if word.strip() != "":
            if word in tf_dict_d_predicted:
                tf = tf_dict_d_predicted[word]
            else:
                tf = 0.0
                
            if word in idf_dict:
                idf = idf_dict[word]
            else:
                idf = 0.0
            
            vector_d_predicted.append(tf*idf)

    actual_table = train_tables[actual_index]

    tf_dict_d_actual = term_freq(actual_table)
    vector_d_actual = []
    for word in question:
        if word.strip() != "":
            if word in tf_dict_d_actual:
                tf = tf_dict_d_actual[word]
            else:
                tf = 0.0
                
            if word in idf_dict:
                idf = idf_dict[word]
            else:
                idf = 0.0
            
            vector_d_actual.append(tf*idf)
    
    length = len(vector_q)
    array_q = []
    for word in question:
        if word.strip()!="":
            array_q.append(word)
    
    result = ""
    for i in range(length):
        result = result + str(array_q[i])+"\t"+str("{0:.4f}".format(vector_q[i]))+"\t"+str("{0:.4f}".format(vector_d_predicted[i]))+"\t\t"+str("{0:.4f}".format(vector_d_actual[i]))+"\n"
       
    return result

def print_question(index):
    with open("../data/sayhearfall2018_train.json", "r") as file:
        load_content = json.load(file)

    question_parsed = load_content[index]["question_parsed"]
    question = ""
    for q in question_parsed:
        if q.strip()!="":
            question += "{} ".format(q.strip())
            
    return "Q"+str(index)+".\t"+question


if __name__ == '__main__':
    train_table_filename = "preprocess/preprocessed_train_table_list.pkl"
    train_question_filename = "preprocess/preprocessed_train_question_list.pkl"
    
    f_w = open('error_analysis.txt','w+')

    
    with open(train_table_filename, 'rb') as f:
        train_tables = pickle.load(f)
        
    with open(train_question_filename, 'rb') as f:
        train_questions = pickle.load(f)
    
    top_N = 1
    correct = 0
    wrong = 0

    for i in range(len(train_questions)):
        question = train_questions[i]

        cosine_sim_array = tf_idf(question, train_tables)    
  
        predicted_label = cosine_sim_array.argsort()[-top_N:][::-1][0]
                
        if i in cosine_sim_array.argsort()[-top_N:][::-1]:
            correct += 1
        else:
            wrong += 1
            f_w.write("\n--------------------------------------------------------------------\n\n")

            question_index = i
            table_index = predicted_label
            f_w.write(str(question_index) +"-->"+str(table_index)+"\n")
            
            question_actual = train_questions[question_index]
            question_predicted = train_questions[table_index]
            
            f_w.write("\n")
            f_w.write(print_question(question_index))
            f_w.write("\n")
            f_w.write(print_question(table_index))
            f_w.write("\n")
            f_w.write("\n")
                        
            f_w.write(print_vectors(question_actual, train_tables, question_index, table_index))
    f_w.close()

        
        

    
    
    