import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import pickle
import os
import csv
import re
import argparse

class TablePreprocessor():
	def __init__(self,json,data):
		self.json = json
		self.data = data

	def load_tables_path(self, question_json_file_path, root_path):
		with open(question_json_file_path, "r") as file:
			load_content = json.load(file)
		return [os.path.join(root_path, item["directory"], "table.csv") for item in load_content]

	def parse_csv_table(self, table_path, include_table_name = True, include_headers = True):
		with open(table_path) as f:
			reader = csv.reader(f)
			table_name = next(reader)
			headers = next(reader)
			cell_values = []
			for row in reader:
				cell_values += row
			if include_table_name:
				cell_values = table_name + cell_values
			if include_headers:
				cell_values = headers + cell_values
		return cell_values

	def parse_cell(self, value, ignore_url = False):
		ans = []
		if value.startswith("http") and ignore_url:
			return ans
		ans = re.split(r'[^0-9a-zA-Z]', value)
		ans = [string for string in ans if string not in ["", None]]
		
		return ans

	def stop_words_filter(self, word_bags):
		stop_words = set(stopwords.words('english'))
		return [word for word in word_bags if not word in stop_words]

	def stemming_words_filter(self, word_bags):
		ps = PorterStemmer()
		return [ps.stem(word) for word in word_bags]

	def preprocess(self, word_bags, stop_words = True, stemming_words = True):
		filtered_word_bags = word_bags
		if stop_words:
			filtered_word_bags = self.stop_words_filter(filtered_word_bags)
		if stemming_words:
			filtered_word_bags = self.stemming_words_filter(filtered_word_bags)
		return filtered_word_bags

	def run_and_save(self, save_path, stop_words = True, stemming_words = True, include_table_name = True, 
					 include_headers = True, ignore_url = False):
		table_paths = self.load_tables_path(self.json,self.data)#"../../data/sayhearfall2018_train.json", "../../data/sayhearfall2018_train/")
		preprocessed_table_list = []
		for path in table_paths:
			cell_values = self.parse_csv_table(path, include_table_name, include_headers)
			word_bags = []
			for value in cell_values:
				word_bags += self.preprocess(processor.parse_cell(value, ignore_url), stop_words, stemming_words)
			preprocessed_table_list.append(word_bags)
		with open(save_path, "wb") as f:
			pickle.dump(preprocessed_table_list, f)
		return preprocessed_table_list

		

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-j", "--json", required=True,
		help="path for json data to parse")
	ap.add_argument("-d", "--data", required=True,
		help="path for data directory that contains directories containing table.csv")
	ap.add_argument("-o", "--out", required=True,
		help="path for output pkl file")

	args = vars(ap.parse_args())
	processor = TablePreprocessor(args["json"],args["data"])
	preprocessed_table_list = processor.run_and_save(args["out"])#"preprocessed_train_table_list.pkl"
	print(preprocessed_table_list)
	print(len(preprocessed_table_list))

