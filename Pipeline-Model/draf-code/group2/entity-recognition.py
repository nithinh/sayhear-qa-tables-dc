# -*- coding: utf-8 -*-

import spacy

nlp = spacy.load('en_core_web_sm')
f = open('questions.txt', 'r')
lines = f.readlines()
keywords = []
for line in lines:
    inp = line.decode('UTF-8')[:-1]
    doc = nlp(inp)
    temp=[]
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
              token.shape_, token.is_alpha, token.is_stop)
    # spacy.displacy.serve(doc, style='dep')
        if token.pos_==u'NOUN' or token.pos_==u'ADJ' or token.pos_==u'ADV':
            temp.append(token.text)
    keywords.append(temp)

out = open('keywords.txt','w+')
for line in keywords:
    out.write(' '.join(line)+'\n')
out.close()