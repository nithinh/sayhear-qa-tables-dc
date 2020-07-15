import csv
import json
import numpy as np
import argparse

import sys
sys.path.insert(0, '../tools/')
import helper_functions as helper
import my_tokenize as tk


def main(dataset,word2vec=None):
	X = list()
	f = open('../../data/sayhearfall2018_'+dataset+'.json','r')
	content  = json.load(f)
	Y = list()
	for ex in content:
		# print(ex['id'])
		Y.append(ex['table_type'])


		x = list()

		##get id
		id = ex['id']
		table_file_path = '../../data/tables/'+dataset+'/original tables/'+id.__str__()+'.csv'
		x.append(id)
		x.append(ex['table_type'])

		with open(table_file_path, 'r') as ftable:

			content_lentgh = list()
			digit_in_cells = list()
			reader = csv.reader(ftable)
			for i,row in enumerate(reader):
				## check if key in column header
				if i == 1 :
					## number of rows
					x.append(len(row))

					## number of non link rows
					row_without_links = [h for h in row if ('url' not in h and 'link' not in h)]
					x.append(len(row_without_links))

					## are the works key of property in the hearders ?
					key_in_colheaders = 0
					row_tk = tk.tokenize(row)
					if ('key' in row_tk or 'keys' in row_tk or 'property' in row_tk or 'properties' in row_tk) :#or 'keys' in row_tk:
						key_in_colheaders = 1
					x.append(key_in_colheaders)

				if i >1 :
					## Get length of cell
					row_lengths = list()
					## Is digit in cell?
					row_digit_in_cells = list()
					for cell in row:
						row_lengths.append(len(cell.split()))
						row_digit_in_cells.append(helper.hasNumbers(cell))
					content_lentgh.append(row_lengths)
					digit_in_cells.append(row_digit_in_cells)


			## save data about variation of legnth of content
			content_lentgh_matrix = np.matrix(content_lentgh)
			n_rows, n_col = content_lentgh_matrix.shape
			normalized_variations = list()
			for i in range(n_col):
				col = content_lentgh_matrix[:,i]
				max_length = col.max()
				std_length = np.std(col) 
				normalized_var = float(std_length)/max_length if max_length>0 else 0
				normalized_variations.append(normalized_var) 
			avg_normalized_variation = np.average(np.array(normalized_variations))
			x.append(avg_normalized_variation)

			## save abaout about digit in cells
			digit_in_cells_matrix = np.matrix(digit_in_cells)
			digit_variations = list()
			for i in range(n_col):
				col = digit_in_cells_matrix[:,i]
				var = (float(np.average(col))-0.5)
				var = 1 - np.absolute(var)*2
				digit_variations.append(var)
			avg_digit_in_cell_variation = np.average(np.array(digit_variations))
			x.append(avg_digit_in_cell_variation)





		X.append(x)

	with open(dataset+'.csv', 'w') as f:
		csvwriter = csv.writer(f)
		csvwriter.writerow(['id','type','Number of culumns','Number of columns when ignoring link columns', 'key or property in colmun header', 'Variation of centent length', 'Varation of presence of digits'])
		for row in X:
			csvwriter.writerow(row)

	print(X)
	X = np.matrix(X)
	print(X.shape)
	print(X)
	key_in_colheaders_vec = X[:,2]
	# print('---------')
	# print(key_in_colheaders_vec)

	print('%d type 1 tables'%Y.count(1))
	print('%d type 2 tables\n'%Y.count(2))

	X1 = helper.get_sub_matrix(X,1,1)
	X0 = helper.get_sub_matrix(X,1,2)

	# print(X1)

	col = 2

	print('Average number of columns for type 1 tables:%.2f'%np.average(X1[:,col]))
	print('Average number of columns for type 2 tables:%.2f\n'%np.average(X0[:,col]))
	col += 1

	print('When ignoring link columns: average number of columns for type 1 tables:%.2f'%np.average(X1[:,col]))
	print('When ignoring link columns: average number of columns for type 2 tables:%.2f\n'%np.average(X0[:,col]))
	col += 1

	print('%d type 1 tables with "key" in column header'%(X1[:,col] == 1).sum())
	print('%d type 2 tables  with "key" in column header\n'%(X0[:,col] == 1).sum())
	col += 1 

	print('Average variation in content length for type 1 tables:%.4f'%(np.average(X1[:,col])))
	print('Average variation in content length for type 2 tables:%.4f\n'%(np.average(X0[:,col])))
	col += 1

	print('Average variation in presence of digits for type 1 tables:%.4f'%(np.average(X1[:,col])))
	print('Average variation in presence of digits for type 2 tables:%.4f\n'%(np.average(X0[:,col])))
	col += 1


if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='Generate CSV with feartures for ML.')
	parser.add_argument('dataset', metavar='dataset', type=str, help='Pass a word2vec model if needed.')
	parser.add_argument('--word2vec_model', metavar='word2vec_model', nargs='?', const='false', type=str, help='Pass a word2vec model if needed.')
	
	args = parser.parse_args()


	main(args.dataset)