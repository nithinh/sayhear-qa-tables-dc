import spacy
import csv
import json

def create_table_info():
	results = []
	results.append(["table_id","table_name","columns","rows"])
	table_path = "../../data/tables/train/transposed_csvs/"
	

	for table_id in range(0,238):
		current_table = table_path + str(table_id) + ".csv"
		fh = open(current_table,"r")
		data = list(csv.reader(fh, delimiter=','))
		results.append([table_id,data[0],data[1],len(data)])

		

	with open("train_tables.csv","w+") as my_csv:
			csvWriter = csv.writer(my_csv,delimiter=',')
			csvWriter.writerows(results)

def load_table(table_id):
	path = "test"	
	if table_id < 238:
		path = "train"

	table_path = "../../data/tables/" + path + "/transposed_csvs/"
	current_table = table_path + str(table_id) + ".csv"
	fh = open(current_table,"r")
	data = list(csv.reader(fh, delimiter=','))
	return data

def main():
	#load_question_type("../question_classification/qtcsv.csv","test_q_type.csv")
	result = []

	fh = open("gqa - gqa.csv","r")
	csv_reader = csv.reader(fh, delimiter=',')
	line_count = 0
	current_table_id = -1
	current_table = None

	
	for row in csv_reader:
		try:
			if line_count == 0:
				result.append(row + ["retrieved_answers"])
				line_count += 1
			else:
				table_id = int(row[0])
				answer = row[3]

				if table_id != current_table_id:
					current_table = load_table(table_id)
					current_table_id = table_id

				answers = answer.split(",")
				ret = []

				for a in answers:
					items = a.split(":")
					r = int(items[0])-1
					c = int(items[1])-1
					# print(r,c,len(current_table),len(current_table[r]))
					ret.append(current_table[r][c])

				result.append(row + [",".join(ret)])

				line_count +=1
		except ValueError:
			print("not a proper value for row and column")
		except :
			print("something was wrong")

	
	with open("gqa_corrected.csv","w") as my_csv:
		csvWriter = csv.writer(my_csv,delimiter=',')
		csvWriter.writerows(result)
	
	

# doc2 = nlp_mod(u"Mangoes and bananas")

if __name__ == '__main__':
	main()
