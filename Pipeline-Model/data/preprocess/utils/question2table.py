import json
import csv
import os
from texttable import Texttable
import argparse

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-j", "--json", required=True,
		help="path for json data to parse")
	ap.add_argument("-d", "--data", required=True,
		help="path for data directory that contains directories containing table.csv")
	args = vars(ap.parse_args())

	with open(args["json"], "r") as file:#"../../data/sayhearfall2018_train.json"
			load_content = json.load(file)
	while True:
		s = input(">> Please input indexs of the questions (seperated by comma): ")
		show_table = input(">> Show table?(y/n): ") == "y"
		print(">>")
		question_indexs_list = str(s).split(",")
		for index in question_indexs_list:
			question_parsed = load_content[int(index)]["question_parsed"]
			question = ""
			for q in question_parsed:
				question += "{} ".format(q)
			print(">> Question {}: {}".format(index.replace(" ", ""), question))
			if show_table:
				try:
					table_path = os.path.join(args["data"], load_content[int(index)]["directory"], "table.csv")#"../../data/sayhearfall2018_train/"
					with open(table_path) as f:
						reader = csv.reader(f)
						table_name = next(reader)
						# headers = next(reader)
						x = Texttable(100)
						for row in reader:
							x.add_row(row[:10])
					print(x.draw())
				except:
					print(">> Oop! Failed to print the table")
					print(">> The table path is {}".format(table_path))
					input()
			print(">>")