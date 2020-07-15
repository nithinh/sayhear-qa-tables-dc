import argparse
import csv
import json

def append_table_id_to_question_type(file,id_to_table_map):
	results = [["id question","major_type","minor_type","table_id"]]
	fh = open(file,"r")
	csv_reader = csv.reader(fh, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		else:
			index = int(row[0])
			results.append(row + [id_to_table_map[index]])

			line_count += 1
	return results

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	# ap.add_argument("-j", "--json", required=False,
	# 	help="path for json data to parse")

	ap.add_argument("-j", "--json", required=True,
		help="path for  sayhear_data.json to parse")

	ap.add_argument("-qt", "--questiontype", required=True,
		help="path for  generated question type csv (id question,major_type,minor_type)  per row format ")

	ap.add_argument("-o", "--output", required=False,
		help="path for output csv")
	# ap.add_argument("-oh", "--onehot", required=False,
	# 	help="path for output csv as onehot vector")

	args = vars(ap.parse_args())
	# prs = QuestionPreprocessor(json_file_path = args["json"])


	# original_question_list = prs.load_questions()
	# preprocessed_question_list = [prs.preprocess( False, False) for question in original_question_list]

	map = {}

	if "json" in args:
		f  = open(args["json"],'r')
		data = json.load(f)
		index = -1
		table_id = -1
		for x in data:
			if 'id' in x:
				index = x['id']
			elif 'question_id' in x:
				index = x['question_id']

			if 'table_id' in x:
				table_id = x['table_id']
			elif 'id' in x:
				table_id = x['id']
			map[index] = table_id




	with open(args["output"],"w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(append_table_id_to_question_type(args["questiontype"],map))




	

	
