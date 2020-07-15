import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pickle
import sys
import argparse

class QuestionPreprocessor():
	def __init__(self, json_file_path):
		self.json_file_path = json_file_path

	def load_questions(self):
		with open(self.json_file_path, "r") as file:
			load_content = json.load(file)
		return [item["question_parsed"] for item in load_content]

	def stop_words_filter(self, question):
		stop_words = set(stopwords.words('english'))
		return [word for word in question if not word in stop_words]

	def stemming_words_filter(self, question):
		ps = PorterStemmer()
		return [ps.stem(word) for word in question]

	def preprocess(self, question, stop_words = True, stemming_words = True):
		filtered_question = question
		if stop_words:
			filtered_question = self.stop_words_filter(filtered_question)
		if stemming_words:
			filtered_question = self.stemming_words_filter(filtered_question)
		return filtered_question

	def run_and_save(self, save_path, stop_words = True, stemming_words = True):
		original_question_list = self.load_questions()
		preprocessed_question_list = [self.preprocess(question, stop_words, stemming_words) for question in original_question_list]
		with open(save_path, "wb") as f:
			pickle.dump(preprocessed_question_list, f)
		return preprocessed_question_list



if __name__ == "__main__":
	# path = sys.argv[1] #"../../data/sayhearfall2018_train.json"
	# outpath = sys.argv[2] #preprocessed_train_question_list.pkl

	ap = argparse.ArgumentParser()
	ap.add_argument("-j", "--json", required=True,
		help="path for json data to parse")
	ap.add_argument("-o", "--out", required=True,
		help="path for output pkl file")
	args = vars(ap.parse_args())
	processor = QuestionPreprocessor(json_file_path = args["json"])
	preprocessed_question_list = processor.run_and_save(args["out"])
	print(preprocessed_question_list)
	print(len(preprocessed_question_list))
	
		
	