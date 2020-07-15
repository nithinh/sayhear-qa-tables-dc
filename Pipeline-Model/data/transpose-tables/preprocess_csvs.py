import csv
import os
import argparse
import re

def replace_non_ascii(text):
	return ''.join([i if ord(i) < 128 else '_' for i in text])

def replace_consecutive_underscores(text):
	text = re.sub('_+','_',text)
	text = text[1:] if text[0] == '_' else text
	text = text[:-1] if text[-1] == '_' else text
	return text

def preprocess_csv(csv_path):
	f = open(csv_path,'r')
	new_csv = list()
	csv_reader = csv.reader(f)
	for i,row in enumerate(csv_reader):
		if i ==1 :
			new_headers = [h.replace(' ','_') for h in row]
			new_headers = [h.replace('"',' ') for h in row]
			new_headers = [h.replace('\n','_') for h in new_headers]
			new_headers = [h.replace('\r','_') for h in new_headers]
			new_headers = [h.replace('\'','_') for h in new_headers]
			new_headers = [h.strip() for h in new_headers]
			new_headers = [replace_non_ascii(h) for h in new_headers]
			new_headers = [replace_consecutive_underscores(h) for h in new_headers]
			new_csv.append(new_headers)
		else:
			new_csv.append(row)
	f.close()
	with open(csv_path,'w') as f:
		csv_writer = csv.writer(f)
		for row in new_csv:
			csv_writer.writerow(row)


def main(path):
	for file in os.listdir(path):
		preprocess_csv(path+file)

if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='Parse column headers.')
	parser.add_argument('path_to_csv_folder', metavar='path_to_csv_folder', type=str, help='Path to CSV folder')
	args = parser.parse_args()

	main(args.path_to_csv_folder)