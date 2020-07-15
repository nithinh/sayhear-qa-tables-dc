import csv
import random
import pickle
import os.path
import io
from os import listdir
from os.path import isfile, join

def load_table_info():
	table_info = {}
	fh = open("table_info.csv","r")
	csv_reader = csv.reader(fh, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		else:
			table_info[row[0]] = int(row[3])
			line_count +=1
	return table_info

def main():
	# table = random.randint(0,300)
	# file = "Responses:"+str(table) +".csv"
	# for i in range(tables):
	table_info = load_table_info();
	print(table_info)
	all_entries = []
	onlyfiles = [f for f in listdir('responses') if isfile(join('responses', f))]
	# onlyfiles = sorted(onlyfiles)
	for f in onlyfiles:
		file = f
		table = f.split(':')[1].split('.')[0]
		print(table)
		try:
			fh = open('responses/' + file, 'r')
			csv_reader = csv.reader(fh, delimiter=',')
			line_count = 0
			COLUMN_NAMES = {
				'Timestamp':[0], 
				'Email Address':[1], 
				'Question:':[2,6,10,14,18,22,26,30,34,38], 
				#'Row(s) that contain(s) the answer, separated by commas:':[3,7,11,15,19,23,27,31,35,39], 
				'Rows':[3,7,11,15,19,23,27,31,35,39], 
				'Answer Text:':[4,8,12,16,20,24,28,32,36,40], 
				'Question Type:':[5,9,13,17,21,25,29,33,37,41]
			}  
			
			for row in csv_reader:
				if line_count == 0:
					
					line_count += 1
				else:
					if not row[1]:
						continue
					print(str(table) + " " + row[1])
					table_id = str(table)
					email = row[1]

					item_row = [table_id,email]
					col = 0
					# print(row[COLUMN_NAMES['Question:'][0]])
					for index in COLUMN_NAMES['Question:']:
						col +=1
						cells = ""
						if row[index]:
							if table_info[table] == 3:
								cells = "3:" + str(col)
							else:
								rows = row[index + 1].split(",")
								for item in rows:
									if cells:
										cells += ","
									cells += item + ":"+str(col)
							all_entries.append(item_row + [row[index]] + [cells] + [row[index+2]] + [row[index + 3]])
							# print(row[index])	

					line_count += 1
		except IOError:
			print(file + " not found")
	all_entries = sorted(all_entries,key=lambda x: int(x[0]))
	all_entries.insert(0,['Table id','Email','Question','Cells(row:column)','Answer','QuestionType'])
	# print(all_entries)
	with open("generated_questions.csv","w") as out_csv:
		csvWriter = csv.writer(out_csv,delimiter=',')
		csvWriter.writerows(all_entries)
	# print('Processed {line_count} lines.')

if __name__ == '__main__':
	main()

