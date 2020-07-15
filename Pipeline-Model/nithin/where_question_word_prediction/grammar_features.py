import sys
import argparse
import requests
import csv
import spacy
import json

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-j", "--json", required=True,
		help="path for json data to parse")

	ap.add_argument("-a", "--all", action='store_true',required=False,
		help="include pos,ner and dependency data (defualt)")

	ap.add_argument("-p", "--pos", action='store_true',required=False,
		help="include pos data")
	ap.add_argument("-n", "--ner", action='store_true',required=False,
		help="include ner data")
	ap.add_argument("-d", "--dep", action='store_true',required=False,
		help="include dependency tag data")

	ap.add_argument("-o", "--output", required=True,
		help="path for output csv")

	args = vars(ap.parse_args())
	print(args)

	f  = open(args["json"],'r')
	data = json.load(f)

	nlp = spacy.load('en_core_web_sm')
	results = []
	res = ["id question","word","word index"]
	NER = ["PERSON","LOCATION","DATETIME","QUANTITY","ORGANISATION","NONE"]

	def labelToNER(label):
		temp = []
		if label =="PERSON":
			# print token.text,entities[token.text]
			temp = [1,0,0,0,0,0]
		elif (label=="GPE" or label=="LOC"):
			# print token.text, entities[token.text]
			temp = [0,1,0,0,0,0]
		elif (label=="DATE" or label=="TIME"):
			# print token.text, entities[token.text]
			temp = [0,0,1,0,0,0]
		elif (label=="ORDINAL" or label=="QUANTITY"):
			# print token.text, entities[token.text]
			temp = [0,0,0,1,0,0]
		elif token.text in entities and entities[token.text]=="ORG":
			temp = [0, 0, 0, 0, 1, 0]
		else:
			# print token.text
			temp = [0,0,0,0,0,1]
		return temp
	POS = ["ADV","VERB","DET","ADJ","PROPN","ADP","PART","NOUN","NUM","PRON","INTJ","CCONJ"]
	deptypes = ["acl",	"advcl"	,"advmod",	"amod",	"appos","aux","case","cc","ccomp",	"clf",	"compound",	"conj","cop","csubj","dep","det","discourse","dislocated","expl","fixed","flat"	,"goeswith",	"iobj",	"list","mark","nmod","nsubj","nummod","obj","obl","orphan","parataxis","punct","reparandum"	,"root"	,"vocative",	"xcomp"	];
	d = {"ADV":0,"VERB":1,"DET":2,"ADJ":3,"PROPN":4,"ADP":5,"PART":6,"NOUN":7,"NUM":8,"PRON":9,"INTJ":10,"CCONJ":11}

	all_features = (args['pos'] and args['ner'] and args['dep']) or (not args['pos'] and not args['ner'] and not args['dep'] or args['all'])
	if(all_features):
		results.append(res + NER + POS + deptypes + ["is_stop"])
	else:
		types = res
		if(args['ner']):
			types += NER
		if(args['pos']):
			types += POS
		if(args['dep']):
			types += deptypes
		results.append(types + + ["is_stop"])


	for x in data:
		question = ' '.join([ch for ch in x['question_parsed'] if ch!="" and not ch.isspace()])
		if 'id' in x:
			index = x['id']
		elif 'question_id' in x:
			index = x['question_id']
	
		result = nlp(question)
		temps = [(token.text,token.label_) for token in result.ents]
		entities = {}
		for text,label in temps:
			words = text.split()
			for word in words:
				entities[word] = label
		
		word_index = 0
		for idx,token in enumerate(result):
			for i,word in enumerate(x['question_parsed']):
				if(word == token.text and i>= word_index):
					word_index = i
					break
			word_tags =[]
			for dt in deptypes:
				if(token.dep_.lower() == dt):
					word_tags.append(1)
				else:
					word_tags.append(0)
			if token.pos_ not in d:
				d[token.pos_] = 13
			pos = [1 if j==d[token.pos_] else 0 for j in range(12)]
			if token.text not in entities:
				entities[token.text] = "NONE"

			is_stop = 0
			if(token.is_stop):
				is_stop = 1 
			if(all_features):
				results.append([index] + [token.text,word_index] + labelToNER(entities[token.text]) + pos + word_tags + [is_stop])
			else:
				types = [index] + [word_index]
				if(args['ner']):
					types += labelToNER(entities[token.text])
				if(args['pos']):
					types += pos
				if(args['dep']):
					types += word_tags
				results.append(types + [is_stop])
			word_index+=1

	with open(args["output"],"w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(results)