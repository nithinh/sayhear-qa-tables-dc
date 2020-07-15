import spacy
import csv
import json

def load_questions_json(question_filename):
	f  = open(question_filename,'r')
	qmap = {}
	data = json.load(f)
	for x in data:
		question = ' '.join([ch for ch in x['question_parsed'] if ch!="" and not ch.isspace()])
		index = x['id']
		question = question.strip().lower()
		qmap[index] = question

	return qmap

def load_questions(question_filename):
	# question_filename = args["questions"]#"train_question.txt"
	questions = open(question_filename, 'r',encoding="utf8").readlines()
	
	qmap = {}
	for question in questions:
		index = int(question.split(":")[0].split(" ")[1])
		question = question.strip('\n').split(":")[1].strip().lower()
	
		qmap[index] = question

	return qmap

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
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		else:
			index = int(row[0]) 
			mj_type = row[1]

			if mj_type in substitutions:
				mj_type = substitutions[mj_type]
			mi_type = row[2]

			question_type_map[index] = {"major":mj_type,"minor":mi_type}

			line_count += 1
	return question_type_map

nlp_mod = spacy.load("model/en_vectors_wiki_lg")

questions = load_question_type("test_q_type.csv")

# doc1 = nlp_mod(questions[0])
# question_id = 0
results = []
res = ["question_id","table_id","column_id","row_id","sim_score"]
results.append(res)

table_path = "../../data/tables/test/transposed_csvs/"
table_ids = sorted(questions.keys())

for table_id in table_ids:
	current_table = table_path + str(table_id) + ".csv"
	fh = open(current_table,"r")
	csv_reader = csv.reader(fh, delimiter=',')

	line_count = 0
	for row in csv_reader:
		if line_count == 0 or line_count == 1:
			
			line_count += 1
		else:
			for col in range(0,len(row)):
				doc1 = nlp_mod(row[col])
				for question_id in questions:
					qtype = questions[question_id]["major"] + " " + questions[question_id]["minor"]
					doc2 = nlp_mod(qtype)
					val = [str(question_id), str(table_id),str(col),str(line_count),str(doc1.similarity(doc2))]
					# pri	nt(val)
					results.append(val)
			line_count += 1
	print("completed table " + str(table_id))

with open("test_cell_qf_sim.csv","w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(results)

# doc2 = nlp_mod(u"Mangoes and bananas")
