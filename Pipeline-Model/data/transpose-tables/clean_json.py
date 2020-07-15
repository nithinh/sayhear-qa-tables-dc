import json
import argparse

def main(dataset):
	with open (dataset,'r') as f:
		content = json.load(f)
		for ex in content:
			# ex['table_type'] = ex['table_type']['final']
			ex.pop('sql_transpose', None)
	with open(dataset,'w') as f:
		json.dump(content,f,indent=1)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Clean useless json fields.')
	parser.add_argument('dataset', metavar='dataset', type=str, help='Path to json file.')
	args = parser.parse_args()

	main(args.dataset)
