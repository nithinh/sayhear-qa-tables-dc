import spacy
import csv
import json
import argparse

def load_question_type(file):
	question_type_map = {}

	substitutions = {"NUM" : "number", 
	"ENTY" : "entity", 
	"DESC" : "description", 
	"LOC":"location",
	"HUM":"human",
	"ABBR" : "abbreviation" 
	}

	fh = open(file,"r")
	csv_reader = csv.reader(fh, delimiter=',')
	line_count = 0
	tables = {}
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		else:
			index = int(row[0]) 
			mj_type = row[1]

			if mj_type in substitutions:
				mj_type = substitutions[mj_type]
			mi_type = row[2]
			table_id = row[3]
			question_type_map[index] = {"major":mj_type,"minor":mi_type,"table_id":table_id}

			if table_id not in tables:
				tables[table_id] = True

			line_count += 1
	return question_type_map,tables
	
def main(args):
	#load_question_type("../question_classification/qtcsv.csv","test_q_type.csv")

	nlp_mod = spacy.load("model/en_vectors_wiki_lg")


	results = []
	res = ["question_id","table_id","column_id","sim_score"]
	results.append(res)
	questions,tables = load_question_type(args["questiontype"])

	table_path = args["tablefolder"]
	question_ids = sorted(questions.keys())

	for table_id in tables:
		current_table = table_path + str(table_id) + ".csv"
		fh = open(current_table,"r")
		csv_reader = csv.reader(fh, delimiter=',')

		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				
				line_count += 1
			elif line_count == 1:
				for col in range(0,len(row)):
					doc1 = nlp_mod(row[col])
					for question_id in questions:
						qtype = questions[question_id]["major"] + " " + questions[question_id]["minor"]
						# print(row[col],qtype)
						doc2 = nlp_mod(qtype)
						val = [str(question_id), str(table_id),str(col),str(doc1.similarity(doc2))]
						# print(val)
						results.append(val)
				line_count += 1
		print("completed table " + str(table_id))

	with open(args["output"],"w+") as my_csv:
			csvWriter = csv.writer(my_csv,delimiter=',')
			csvWriter.writerows(results)

# doc2 = nlp_mod(u"Mangoes and bananas")

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	# ap.add_argument("-j", "--json", required=False,
	# 	help="path for json data to parse")

	ap.add_argument("-tf", "--tablefolder", required=True,
		help="path for  directory with csv files containing the tables to parse")
	ap.add_argument("-qt", "--questiontype", required=True,
		help="path for  generated question type csv (id question,major_type,minor_type)  per row format ")

	ap.add_argument("-o", "--output", required=True,
		help="path for output csv")

	args = vars(ap.parse_args())

	main(args)
