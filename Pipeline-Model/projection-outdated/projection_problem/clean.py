import json
import csv


# f  = open('train.json','r')
# data = json.load(f)
# Data cleanign 1917 to 1788
# count=0
# empty_indices=[]
# for x in data:
#     for i,ch in enumerate(x['question_parsed']):
#         if ch=="":
#             empty_indices.append(count)
#         count+=1
# empty_indices=set(empty_indices)
# basicfile = open('basic.csv','r')
# reader = csv.reader(basicfile)
# ner_file = open('ner_features.csv','r')
# reader_ner = csv.reader(ner_file)
# pos_file = open('pos_features.csv','r')
# reader_pos = csv.reader(pos_file)
# basicfile_new = open('basic_new.csv','w+')
# merged_file = open('merged_features.csv','w+')
# writer_basic_new = csv.writer(basicfile_new)
# writer_merged = csv.writer(merged_file)
# ner_rows= [x[2:] for x in reader_ner]
# pos_rows = [x[2:] for x in reader_pos]
# j=0
# for i,line in enumerate(reader):
#     if i not in empty_indices:
#         writer_basic_new.writerow(line)
#         writer_merged.writerow(line+ner_rows[j]+pos_rows[j])
#         j+=1
#
# print i
# print reader
# print count