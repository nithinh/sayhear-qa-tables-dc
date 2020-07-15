import json
import csv
import spacy


######################
# Data cleaning


count=0
empty_indices=[]
f  = open('test.json','r')
data = json.load(f)
for x in data:
    for i,ch in enumerate(x['question_parsed']):
        if ch=="":
            empty_indices.append(count)
        count+=1
# empty_indices=set(empty_indices)
# basicfile = open('basic_test.csv','r')
# reader = csv.reader(basicfile)
# ner_file = open('ner_features_test.csv','r')
# reader_ner = csv.reader(ner_file)
# pos_file = open('pos_features_test.csv','r')
# reader_pos = csv.reader(pos_file)
# basicfile_new = open('basic_test_new.csv','w+')
# merged_file = open('merged_features_test.csv','w+')
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

# print i
# print reader
# print count

##########
#NER

# featuresfile = open('ner_features_test.csv','w+')
# writer = csv.writer(featuresfile)
# f  = open('test.json','r')
# data = json.load(f)

# writer.writerow(["id question","index word from question","PERSON","LOCATION","DATETIME","QUANTITY","ORGANISATION","NONE"])
# for x in data:
#     doc = nlp(' '.join([ch for ch in x['question_parsed'] if ch!=""]))
#     temps = [(token.text,token.label_) for token in doc.ents]
#     entities = {}
#     for text,label in temps:
#         words = text.split()
#         for word in words:
#             entities[word] = label
#     print entities
#     for i,token in enumerate(doc):
#         # temp = [0 for j in range(12)]
#         if token.text in entities and  entities[token.text]=="PERSON":
#             print token.text,entities[token.text]
#             temp = [1,0,0,0,0,0]
#         elif token.text in entities and  (entities[token.text]=="GPE" or entities[token.text]=="LOC"):
#             print token.text, entities[token.text]
#             temp = [0,1,0,0,0,0]
#         elif token.text in entities and (entities[token.text]=="DATE" or entities[token.text]=="TIME"):
#             print token.text, entities[token.text]
#             temp = [0,0,1,0,0,0]
#         elif token.text in entities and (entities[token.text]=="ORDINAL" or entities[token.text]=="QUANTITY"):
#             print token.text, entities[token.text]
#             temp = [0,0,0,1,0,0]
#         elif token.text in entities and entities[token.text]=="ORG":
#             temp = [0, 0, 0, 0, 1, 0]
#         else:
#             print token.text
#             temp = [0,0,0,0,0,1]

#         # temp[d[token.label_]]=1
#         # print token.label_,token.text
#         writer.writerow([x['id'],i]+temp)

##################
#POS TAGGING

featuresfile = open('pos_features_test.csv','w+')
writer = csv.writer(featuresfile)
f  = open('test.json','r')
data = json.load(f)
writer.writerow(["id question","index word from question","ADV","VERB","DET","ADJ","PROPN","ADP","PART","NOUN","NUM","PRON","INTJ","CCONJ"])
d = {"ADV":0,"VERB":1,"DET":2,"ADJ":3,"PROPN":4,"ADP":5,"PART":6,"NOUN":7,"NUM":8,"PRON":9,"INTJ":10,"CCONJ":11}
for x in data:
    question = ' '.join([ch for ch in x['question_parsed'] if ch!=""])
    doc = nlp(question)
    print(question,doc)
    for i,token in enumerate(doc):
        temp = [1 if j==d[token.pos_] else 0 for j in range(12)]


        # temp[d[token.label_]]=1
        # print token.label_,token.text
        writer.writerow([x['id'],i]+temp)
# print
# print counter