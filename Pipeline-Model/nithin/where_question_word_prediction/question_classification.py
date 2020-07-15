import sys
import argparse
import requests
import csv
import json

def classify_question(question):

	payload = {
		"auth": "skhf33kjj9",
		"question" : question
	}
	url = "http://qcapi.harishmadabushi.com/?"

	r = requests.get(url, params=payload)
	try:
		data = r.json()
		print(data)
		if(data["status"] == "Success"):
			result = [data["major_type"],data["minor_type"]];
		else:
			result = ["unknown","unknown"]
	except ValueError:
		result = ["unknown","unknown"]
	
	if(result[1] != "unknown"):
		return result
	
	if ("how much" in question):
		result = ["NUM","money"]

	elif ("how many" in question):
		result = ["NUM","count"]
	elif ("how large" in question) or \
	("how big" in question) or \
	("how tall" in question) or \
	("how high" in question) or \
	("how far" in question) or \
	("how deep" in question) or \
	("how long" in question):
		result = ["NUM","dist"]
	elif ("how often" in question) or \
	("how old" in question):
		result = ["NUM","period"]
			
	elif ("when" in question) or \
	("what time" in question) or \
	("which time" in question) or \
	("what year" in question) or \
	("which year" in question) or \
	("what month" in question) or \
	("which month" in question) or \
	("what day" in question) or \
	("which day" in question):
		result = ["NUM","date"]
		
	elif ("where" in question) or \
	("what location" in question) or \
	("which location" in question) or \
	("what place" in question) or \
	("which place" in question) or \
	("what address" in question) or \
	("which address" in question):
		result = ["LOC","others"]

	elif ("what" in question) or ("which" in question):
		result = ["DESC","others"]

	elif ("who" in question):
		result = ["HUM","ind"]

	elif (" how " in question) or (question[0:4] == "how "):
		result = ["DESC","manner"]
	
	else:
		result = ["SQ","yesno"]

	return result

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	# ap.add_argument("-j", "--json", required=False,
	# 	help="path for json data to parse")

	ap.add_argument("-q", "--questions", required=False,
		help="path for  questions.txt to parse")
	ap.add_argument("-j", "--json", required=False,
		help="path for  sayhear_data.json to parse")

	ap.add_argument("-o", "--output", required=False,
		help="path for output csv")
	# ap.add_argument("-oh", "--onehot", required=False,
	# 	help="path for output csv as onehot vector")

	args = vars(ap.parse_args())
	# prs = QuestionPreprocessor(json_file_path = args["json"])


	# original_question_list = prs.load_questions()
	# preprocessed_question_list = [prs.preprocess( False, False) for question in original_question_list]

	results = []
	res = ["id question","major_type","minor_type"]
	results.append(res)

	if "json" in args:
		f  = open(args["json"],'r')
		data = json.load(f)
		for x in data:
			question = ' '.join([ch for ch in x['question_parsed'] if ch!="" and not ch.isspace()])
			if 'id' in x:
				index = x['id']
			elif 'question_id' in x:
				index = x['question_id']
			question = question.strip().lower()
			result = classify_question(question)
			results.append([index] + result)

	elif "question" in args:
		question_filename = args["questions"]#"train_question.txt"
		questions = open(question_filename, 'r',encoding="utf8").readlines()
		for question in questions:
			index = question.split(":")[0].split(" ")[1]
			question = question.strip('\n').split(":")[1].strip().lower()
		
			result = classify_question(question)
			results.append([index] + result)

	
	
	with open(args["output"],"w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(results)




	

	
