import spacy
import csv
import json

def consolidate_question_type(infile,outfile):
	fh = open(infile,"r")
	csv_reader = csv.reader(fh, delimiter=',')

	questions = {}

	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		else:
			index = int(row[0])
			mj_type = row[1]
			mi_type = row[2]

			questions[index] = {"major":mj_type,"minor":mi_type}

			line_count += 1

	results = []
	res = ["question_id","major_type","minor_type"]
	results.append(res)
	for i in range(238,302):
		results.append([str(i),questions[i]["major"],questions[i]["minor"]])

	with open(outfile,"w+") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(results)

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

def write_tuples(tuples,name):
	with open(name + ".csv",'w+') as out:
	    csv_out=csv.writer(out)
	    # csv_out.writererow(['name','num'])
	    for row in tuples:
	        csv_out.writerow(row)
	
def main():
	#load_question_type("../question_classification/qtcsv.csv","test_q_type.csv")

	nlp_mod = spacy.load("model/en_vectors_wiki_lg")


	results = []
	res = ["question_id","table_id","column_id","sim_score"]
	results.append(res)
	questions = load_question_type("train_q_type.csv")

	table_path = "../../data/tables/train/transposed_csvs/"
	table_ids = sorted(questions.keys())

	top_cols = {}
	for table_id in table_ids:
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
						if qtype not in top_cols:
							top_cols[qtype] = {}

						# print(row[col],qtype)
						doc2 = nlp_mod(qtype)
						val = [str(question_id), str(table_id),str(col),str(doc1.similarity(doc2))]
						# print(val)
						top_cols[qtype][row[col]] = doc1.similarity(doc2)


				line_count += 1
		print("completed table " + str(table_id))

	tuples_nc = sorted(top_cols["number count"].items(), key=lambda kv: kv[1],reverse=True)
	tuples_np = sorted(top_cols["number period"].items(), key=lambda kv: kv[1],reverse=True)
	tuples_ep = sorted(top_cols["entity other"].items(), key=lambda kv: kv[1],reverse=True)
	tuples_hi = sorted(top_cols["human ind"].items(), key=lambda kv: kv[1],reverse=True)
	tuples_lo = sorted(top_cols["location other"].items(), key=lambda kv: kv[1],reverse=True)
	tuples_nm = sorted(top_cols["number money"].items(), key=lambda kv: kv[1],reverse=True)
	tuples_nd = sorted(top_cols["number date"].items(), key=lambda kv: kv[1],reverse=True)


	write_tuples(tuples_nc,"number_count")
	write_tuples(tuples_np,"number_period")
	write_tuples(tuples_nm,"number_money")
	write_tuples(tuples_nd,"number_date")
	write_tuples(tuples_ep,"entity_other")
	write_tuples(tuples_hi,"human_ind")
	write_tuples(tuples_lo,"location_other")
	# print(top_cols["number count"])
	# print(top_cols["number period"])
	# print(top_cols["entity other"])
	# print(top_cols["human ind"])
	# print(top_cols["location other"])

	# with open("test_col_qtype_sim.csv","w+") as my_csv:
	# 		csvWriter = csv.writer(my_csv,delimiter=',')
	# 		csvWriter.writerows(results)

# doc2 = nlp_mod(u"Mangoes and bananas")

if __name__ == '__main__':
	main()
