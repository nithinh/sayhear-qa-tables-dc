	
import sys
import argparse
import requests
import csv
import json

	
if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	# ap.add_argument("-j", "--json", required=False,
	# 	help="path for json data to parse")

	ap.add_argument("-q", "--questions", required=False,
		help="path for  questions.csv to parse")

	ap.add_argument("-o", "--output", required=False,
		help="path for output csv")

	args = vars(ap.parse_args())
	question_filename = args["questions"]#"train_question.txt"
	questions = open(question_filename, 'r',encoding="utf8").readlines()

	types = ["NUM","HUM","ENTY","LOC","ABBR","SQ","DESC","date","count","period","money"];
	row1 = ["id question"] + types
	results = []
	results.append(row1)
	for row in questions:
		r = row.split(',')
		mj_type = r[1].strip()
		mi_type = r[2].strip()
		index = r[0]
		if(index == "id question"):
			continue

		new_row = []
		new_row.append(index)
		for ty in types:
			if(ty == mj_type or ty == mi_type):
				new_row.append("1")
			else:
				new_row.append("0")
		results.append(new_row)

	# print(results)


	with open(args["output"],"w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(results)