import sys
sys.path.append("../")
import config
import pandas as pd
import numpy as np
import os
import nltk
from nltk import word_tokenize, pos_tag
import re
import numpy as np
import math
from collections import Counter


WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)




def levenshtein(seq1, seq2):  
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in xrange(size_x):
        matrix [x, 0] = x
    for y in xrange(size_y):
        matrix [0, y] = y

    for x in xrange(1, size_x):
        for y in xrange(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix[size_x - 1, size_y - 1])
    return (matrix[size_x - 1, size_y - 1])

 
train_tables = os.listdir(config.train_tables)
train_questions=config.data_root + "train_question.txt"
print train_questions
qsns = []
with open(train_questions) as f:
    lines = f.readlines()

for line in lines:
    line = line.split(':')[1].strip()
    qsns.append(line)

for i,table in enumerate(train_tables):
    index=table.split('.')[0] 
    csv_file = config.train_tables + table
    current_df = pd.read_csv(csv_file, header=1)
    cols = current_df.columns
    #print qsns[i]
    vector1 = text_to_vector(qsns[1])
    minDist = 99999
    maxDist = 0
    minAns = ""
    maxAns = ""
    sel_col = ""
    for row in current_df.iloc[2:].itertuples(index=False):
        #minDist = 99999
        #maxDist = 0
        #minAns = ""
        #maxAns = ""
        for c in range(len(row)):
            if cols[c]=="url":
                continue
            words = str(row[c])
            #words = re.sub('[^A-Za-z0-9-]+', ' ', words)
            #print words
            #vector2 = text_to_vector(words)
            #dist = get_cosine(vector1, vector2)
            #print ":DIST: ", dist
            dist = levenshtein(qsns[i],words)
            if dist < minDist:
                minDist = dist
                minAns = words
                sel_col = cols[c]
            if dist > maxDist:
                maxDist = dist
                maxAns = words
            #words = nltk.word_tokenize(words)
            #tags = pos_tag(words, tagset='universal')
            #print tags
    #print maxDist, maxAns
    print "Question ", index,": ", qsns[i]
    print "Answer: ", minAns
    print "Column selected: ", sel_col
    #break
