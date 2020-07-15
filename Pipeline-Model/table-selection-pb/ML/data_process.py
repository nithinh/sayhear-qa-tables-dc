import os
import json
from bs4 import BeautifulSoup
import string
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
import spacy

nlp = spacy.load("en")

output_folder = "output"

def expand_query(line):
	line=line.lower()
	
 	word_tokens = word_tokenize(line)
 	filtered_sentence = [w for w in word_tokens if not w in stop_words]

	synonyms=[]

	count=0
	for x in filtered_sentence:
        
		for syn in wordnet.synsets(x):
			for l in syn.lemmas() :
				if(count<3):
					if l.name() not in synonyms:
						synonyms.append(l.name())
						count+=1
                        
		count=0
        
	synonyms_string=' '.join(synonyms)
	new_line=" ".join([str(line),synonyms_string]).encode('utf-8').strip()

	return new_line


stop_words=set(stopwords.words("english"))
final_dict = {}

folders = os.listdir("sayhearfall2018_train")
for folder in folders:
	curr_folder = os.path.join(os.path.abspath("sayhearfall2018_train"), folder)
	print curr_folder
	out_fname = curr_folder.split('/')[6]
	
	if os.path.isdir(curr_folder):
		files = os.listdir(curr_folder)
		for f in files:
			print f 
			if "wrapper" in f:
				#print f
				f = curr_folder+"/"+f
				with open(f) as json_data:
					d=json.load(json_data)
   					question = d['question']
   					question = expand_query(question)
   					tokens = nltk.word_tokenize(question)
   					final_dict['question'] = tokens
   				json_data.close()
   			elif "domxml" in f or "html" in f:
   				f=curr_folder+"/"+f
				with open(f) as fil:
					file_data = fil.read()
				soup = BeautifulSoup(file_data,"lxml")
				for script in soup(["script", "style"]):
					script.extract()    # rip it out
				text = soup.get_text()
				#images = soup.findAll('img')
				text = os.linesep.join([s for s in text.splitlines() if s])
				text = text.strip()
				tokens = nltk.word_tokenize(text)
				final_dict['answer'] = tokens
			#outfile = output_folder+"/"+out_fname+".json"

			elif 'table.csv' in f:
				f=curr_folder+"/"+f
				with open(f) as fil:
					file_data = fil.read()

				print file_data

			#with open(outfile, 'w') as file:
			#	file.write(json.dumps(final_dict))
			#print final_dict
		break

   	

	
