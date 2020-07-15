# -*- coding: utf-8 -*-
from __future__ import division
import gensim.models as gm
import json,glob
from sklearn.metrics.pairwise import cosine_similarity
from numpy import dot,inner
from numpy.linalg import norm
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

import numpy as np

# Data Fetching & Pre-processing




def clean_data(data):
    i=0
    final=[]
    flag=0
    done = set()
    while i < len(data):
        # if "<" in data[i] and flag==0:
        #     flag=1
        #     continue
        # elif ">" in data[i] and flag==1:
        #     flag=0
        #     continue
        if flag==0 and len(data[i])<15 and data[i].encode('ascii','ignore').isalpha():
                final.append(data[i].encode('ascii','ignore').lower().encode('utf-8'))
                done.add(data[i].encode('ascii','ignore').lower().encode('utf-8'))


        i+=1
    return final,done







path = 'data-for-ml-approach/*.json'
files = glob.glob(path)
question2id = []
docs = []
docdict=[]
for filename in files:
    f = open(filename,'r')
    data = json.load(f)
    question= clean_data(data["question"])[0]
    # question = question[:2+int(len(question)/2)]
    x,y=clean_data(data["answer"])
    docs.append(x)
    docdict.append(y)
    question2id.append(question*5)

print len(question2id)


# dataset = api.load("text8")
# dct = Dictionary(docs)
# dct2 = Dictionary(question2id)# fit dictionary
# print len(dct2)
# corpus = [dct.doc2bow(line) for line in docs]# convert corpus to BoW format
# corpus2 = [dct2.doc2bow(line) for line in question2id]# convert corpus to BoW format
#
# tfidf = TfidfModel(corpus,id2word=dct)  # fit model
# tfidf2 = TfidfModel(corpus2,id2word=dct2)  # fit model
#
# low_value = 0.0
# low_value2 = 0
# low_value_words = []
# low_value_words2 = []
#
# for bow in corpus:
#     low_value_words += [id for id, value in tfidf[bow] if value < low_value]
# for bow in corpus2:
#     low_value_words2 += [id for id, value in tfidf2[bow] if value < low_value2]
#
# dct.filter_tokens(bad_ids=low_value_words)
# dct2.filter_tokens(bad_ids=low_value_words2)
#
# print len(dct)
# print len(dct2)
# dct=dict(dct)
# setdct = set(dct.values())
# dct2=dict(dct2)
# setdct2 = set(dct2.values())
# for i,d in enumerate(docs):
#     docs[i] = [word for word in d if word in setdct]
#     print "in"
#     print docs[i]
# for i,q in enumerate(question2id):
#     question2id[i] = [word for word in q if word in setdct2]
#     print "in"
#     print question2id[i]


documents = [gm.doc2vec.TaggedDocument(doc, [str(id_)]) for id_,doc in enumerate(docs)]

# # Model Training :
#
# max_epochs = 60
# vec_size = 20
# alpha = 0.025
#
# model = gm.doc2vec.Doc2Vec(size=vec_size,alpha=alpha,min_alpha=0.002,min_count=1,dm =0)
#
# model.build_vocab(documents)
#
# for epoch in range(max_epochs):
#     print('iteration {0}'.format(epoch))
#     model.train(documents,total_examples=model.corpus_count,epochs=model.iter)
#     model.alpha -= 0.0002
#     model.min_alpha = model.alpha
#     vector = model.infer_vector(question2id[0])
#     most_sim = model.docvecs.most_similar([vector])[0]
#     print most_sim, 0
#
# model.save("sayhear_d2v.model")

# Testing

model = gm.doc2vec.Doc2Vec.load("doc2vec.bin")
print("MODEL LOADED")
test_questions = [(i,list(model.infer_vector(query))) for i,query in enumerate(question2id)]
test_docs = [(j,list(model.infer_vector(doc))) for j,doc in enumerate(docs)]

count1=0
count2=0
print("infered")
for j,quest in enumerate(test_questions):
    maxsims = []
    docs_to_check =[]
    for word in set(question2id[j]):
        for k,doc in enumerate(docs):
            if word in docdict[k] and test_docs[k] not in docs_to_check:
                docs_to_check.append(test_docs[k])
    for i,doc in enumerate(docs_to_check):
        # if dot(quest[1], doc[1])/(norm(quest[1])*norm(doc[1]))>maxsims[1]:
        maxsims.append((doc[0],dot(quest[1], doc[1])/(norm(quest[1])*norm(doc[1]))))
    maxsims.sort(reverse=True,key = lambda x:x[1])
    if j==maxsims[0][0]:
        count1+=1
print(count1/(j+1))


    # print most_sim,i

