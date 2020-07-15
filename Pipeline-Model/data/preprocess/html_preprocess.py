import json
from DocProcessor import DocProcessor
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import pickle
import os
import csv
import re
import argparse

class HTMLPreprocessor():
	def __init__(self,json,data):
		self.doc_processor = DocProcessor()
		self.json = json
		self.data = data

	def load_html_paths(self, question_json_file_path, root_path):
		with open(question_json_file_path, "r") as file:
			load_content = json.load(file)
		ans = []
		for item in load_content:
			if os.path.exists(os.path.join(root_path, item["directory"], "html.txt")):
				ans.append(os.path.join(root_path, item["directory"], "html.txt"))
			else:
				ans.append(os.path.join(root_path, item["directory"], "{}_domxml.txt".format(item["directory"])))
		return ans

	def process_html(self):
		html_paths = self.load_html_paths(self.json,self.data)#"../../data/sayhearfall2018_test.json", "../../data/sayhearfall2018_test/"
		preprocess_text_list = []
		for path in html_paths:
			if os.path.isfile(path):
				preprocess_text_list.append(self.preprocess(self.parse_line(self.doc_processor.process_html(path))))
			else:
				print('ERR: %s does not exist'%path)
		return preprocess_text_list
			

	def parse_line(self, line):
		ans = re.split(r'[^0-9a-zA-Z]', line)
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

	def run_and_save(self, save_path):
		preprocess_text_list = self.process_html()
		with open(save_path, "wb") as f:
			pickle.dump(preprocess_text_list, f)
		return preprocess_text_list





if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-j", "--json", required=True,
		help="path for json data to parse")
	ap.add_argument("-d", "--data", required=True,
		help="path for data directory that contains directories containing table.csv")
	ap.add_argument("-o", "--out", required=True,
		help="path for output pkl file")

	args = vars(ap.parse_args())
	processor = HTMLPreprocessor(args["json"],args["data"])
	preprocess_text_list = processor.run_and_save(args["out"]) #"preprocessed_test_text_list.pkl"
	print(len(preprocess_text_list))



