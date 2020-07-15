import sys
import argparse
import requests
import csv



def csvProcess(path):
	with open(path) as csv_file:
		headers = []
		rows = []
		columns = []
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				# print ("columns")
				# print('%s \t %s \t %s')%(row[0],row[1],row[2])
				for col in row:
					headers.append(col.strip())
					columns.append([])
				line_count += 1
			else:
				# print('%s \t %s \t %s')%(row[0],row[1],row[2])
				rows.append(row);
				line_count += 1
				col_index = 0
				for col in row:
					columns[col_index].append(col.strip())
					col_index +=1
		# print('Processed %d lines.') %line_count
		return headers,rows,columns
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
			result = [question,data["major_type"],data["minor_type"]];
		else:
			result = [question,"unknown","unknown"]
	except ValueError:
		result = [question,"unknown","unknown"]
	
	if(result[1] != "unknown"):
		return result
	
	if ("how much" in question):
		result = [question,"NUM","money"]

	elif ("how many" in question):
		result = [question,"NUM","count"]
	elif ("how large" in question) or \
	("how big" in question) or \
	("how tall" in question) or \
	("how high" in question) or \
	("how far" in question) or \
	("how deep" in question) or \
	("how long" in question):
		result = [question,"NUM","dist"]
	elif ("how often" in question) or \
	("how old" in question):
		result = [question,"NUM","period"]
			
	elif ("when" in question) or \
	("what time" in question) or \
	("which time" in question) or \
	("what year" in question) or \
	("which year" in question) or \
	("what month" in question) or \
	("which month" in question) or \
	("what day" in question) or \
	("which day" in question):
		result = [question,"NUM","date"]
		
	elif ("where" in question) or \
	("what location" in question) or \
	("which location" in question) or \
	("what place" in question) or \
	("which place" in question) or \
	("what address" in question) or \
	("which address" in question):
		result = [question,"LOC","others"]

	elif ("what" in question) or ("which" in question):
		result = [question,"DESC","others"]

	elif ("who" in question):
		result = [question,"HUM","ind"]

	elif (" how " in question) or (question[0:4] == "how "):
		result = [question,"DESC","manner"]
	
	else:
		result = [question,"SQ","yesno"]

	return result

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	# ap.add_argument("-j", "--json", required=False,
	# 	help="path for json data to parse")

	ap.add_argument("-q", "--questions", required=False,
		help="path for  questions.txt to parse")

	ap.add_argument("-qc", "--qcsv", required=False,
		help="path for  question.csv to parse")
	
	ap.add_argument("-c", "--columns", required=False,
		help="path for  columns.csv to parse")

	ap.add_argument("-o", "--output", required=False,
		help="path for output csv")

	args = vars(ap.parse_args())
	# prs = QuestionPreprocessor(json_file_path = args["json"])


	# original_question_list = prs.load_questions()
	# preprocessed_question_list = [prs.preprocess(question, False, False) for question in original_question_list]

	# question_filename = args["questions"]#"train_question.txt"
	# questions = open(question_filename, 'r',encoding="utf8").readlines()


	columns = open(args["columns"],'r',encoding="utf8").readlines()
	results = []
	res = ["id","major_type","minor_type"]
	results.append(res)

		# for question in questions:
		# 	index = question.split(":")[0].split(" ")[1]
		# 	question = question.strip('\n').split(":")[1].strip().lower()
		
		# 	result = classify_question(question)
		# 	results.append([index] + result)
	
	features_repeated = []
	features_repeated.append(res);
	qh,qr,qc = csvProcess(args["qcsv"]);
	offset = int(qr[0][0]);
	for column in columns:
		index = column.split(",")[0]
		if(index == "id question"):
			continue
		index = int(index)
		print(index,offset)
		features_repeated.append(qr[int(index-offset)]);

	# features_repeated = []
	# offset = results[1][0];

	# for column in column:
	# 	index = question.split(",")[0].split(" ")[1]
	# 	features_repeated.append(results[index+1-offset]);

	with open(args["output"],"w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(features_repeated)




	

	
