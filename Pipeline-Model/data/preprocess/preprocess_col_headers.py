import csv
import os
import argparse


def preprocess_csv(csv_path):
	f = open(csv_path,'r')
	new_csv = list()
	csv_reader = csv.reader(f)
	for i,row in enumerate(csv_reader):
		if i ==1 :
			new_headers = [h.replace(' ','_') for h in row]
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
	parser.add_argument('dataset', metavar='dataset', type=str, help='train or test')
	args = parser.parse_args()

	main(args.dataset)