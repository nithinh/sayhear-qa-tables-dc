import csv

def print_dict(a):
	for key in a:
		print(key,",",a[key])

def main():
	fh = open('seeeded_questions.csv', 'r')
	csv_reader = csv.reader(fh, delimiter=',')

	table_coverage = {}
	annotator_coverage = {}
	question_type = {}
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			
			line_count += 1
		else:
			table_id = int(row[0])
			table_email =  row[1]

			if table_id not in table_coverage:
				table_coverage[table_id] = 0
			if table_email not in annotator_coverage:
				annotator_coverage[table_email] = 0

			table_coverage[table_id] += 1
			annotator_coverage[table_email] += 1

			if(row[4]):
				qtypes = [x.strip() for x in row[4].split(",")]
			else:
				qtypes = ["None"]

			for tid in qtypes:
				if tid not in question_type:
					question_type[tid] = 0
				question_type[tid] += 1

			line_count += 1

	uncovered_tables = []

	for i in range(0,302):
		if i not in table_coverage:
			uncovered_tables.append(i)

	print_dict(table_coverage)
	print_dict(annotator_coverage)
	print_dict(question_type)
	print(uncovered_tables)

if __name__ == '__main__':
	main()