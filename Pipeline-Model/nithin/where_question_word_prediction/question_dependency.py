import sys
import argparse
import requests
import csv
import spacy
import json

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-j", "--json", required=False,
		help="path for json data to parse")

	# ap.add_argument("-q", "--questions", required=False,
	# 	help="path for  questions.txt to parse")

	ap.add_argument("-o", "--output", required=False,
		help="path for output csv")

	args = vars(ap.parse_args())
	# prs = QuestionPreprocessor(json_file_path = args["json"])


	# original_question_list = prs.load_questions()
	# preprocessed_question_list = [prs.preprocess( False, False) for question in original_question_list]

	# if("questions" in args):
	# 	question_filename = args["questions"]#"train_question.txt"
	# 	questions = open(question_filename, 'r',encoding="utf8").readlines()


	f  = open(args["json"],'r')
	data = json.load(f)

	nlp = spacy.load('en_core_web_sm')
	results = []
	res = ["id","word","word index"]
	deptypes = ["acl",	"advcl"	,"advmod",	"amod",	"appos","aux","case","cc","ccomp",	"clf",	"compound",	"conj","cop","csubj","dep","det","discourse","dislocated","expl","fixed","flat"	,"goeswith",	"iobj",	"list","mark","nmod","nsubj","nummod","obj","obl","orphan","parataxis","punct","reparandum"	,"root"	,"vocative",	"xcomp"	];
	results.append(res + deptypes)

	for x in data:
		question = ' '.join([ch for ch in x['question_parsed'] if (ch!="" and not ch.isspace())])
		index = x['id']
	# for question in questions:
	# 	index = question.split(":")[0].split(" ")[1]
	# question = question.strip('\n').split(":")[1].strip().lower()
		result = nlp(question)
		# word_index = 0;
		for word_index,token in enumerate(result):
			if(token.text.isspace()):
				continue
			# results.append([index] + [token.text,token.dep_]);
			word_tags =[]
			for dt in deptypes:
				if(token.dep_.lower() == dt):
					word_tags.append(1)
				else:
					word_tags.append(0)
			results.append([index] + [token.text,word_index] + word_tags)
			word_index+=1

	with open(args["output"],"w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(results)