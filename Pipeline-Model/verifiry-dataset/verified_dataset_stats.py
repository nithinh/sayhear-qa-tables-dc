import json
import argparse
import check_all_dataset as check
import sql_tables

def read_last_id_checked():
	with open('last_id_checked.txt','r') as f:
		last_id_checked = int(f.read())
	return last_id_checked

def test_with_only_similarities(dataset,content,ex,word2vec):
	id = ex['id']
	query = ex['final_sql']
	query = check.preprocess_query(query)
	csv_path = '../data/tables/'+dataset+'/transposed_csvs/'+id.__str__()+'.csv'
	new_query = check.get_new_query_by_replacing_tilde_words_with_new_words(dataset,content,ex,id,query,csv_path,word2vec)	
	if new_query:			
		query_res = sql_tables.testQuery(new_query,csv_path,verbose=False)
		v = check.check_or_recheck('recheck',ex,query_res,dataset,content,id,' '.join(ex['question_parsed']),query,new_query,ex['short_a'],automatic_validation=True)
		return v
	return False

def print_stats(working,not_working):
	total = working + not_working
	print('%d examples have been verified:\n%d (%.2f%%) are valid (working),\n%d (%.2f%%) are not.'%(total,working,float(working)*100/total,not_working,float(not_working)*100/total))


def main(dataset,word2vec):

	f =  open('sayhearfall2018_'+dataset+'.json', 'r')
	content = json.load(f)
	f.close()

	n_OK = 0
	n_not_OK = 0
	n_OK_only_sim = 0
	n_not_OK_only_sim = 0
	not_ok = list()

	for ex in content:
		id = ex['id']
		if id > read_last_id_checked():
			break

		else:
			if ex['ex_valid']:
				n_OK += 1
				v = test_with_only_similarities(dataset,content,ex,word2vec)
			else:
				n_not_OK += 1
				not_ok.append(ex)
				v = False
			if v:
				n_OK_only_sim += 1
			else:
				n_not_OK_only_sim += 1

	print('\n\nSTATS:\n')
	print_stats(n_OK,n_not_OK)
	print('\nIf we use only word vector similarities (strategy 4) and none of the other heuristics we usually apply bfore using similarity scores:')
	print_stats(n_OK_only_sim,n_not_OK_only_sim)

	print('\n\nExamples not working:')
	for ex in not_ok:
		print('\n%d'%ex['id'])
		print('Question: %s'%' '.join(ex['question_parsed']))
		print('SQL: %s'%ex['final_sql'])
		print('Expected answer: %s'%ex['short_a'])
		if 'note' in ex.keys():
			print('Note: %s'%ex['note'])


if __name__ == '__main__':


	parser = argparse.ArgumentParser(description='Manually check the whole dataset.')
	parser.add_argument('dataset', metavar='dataset', type=str, help='train or test')
	parser.add_argument('--table_type', metavar='table_type', nargs='?', const='none', type=str, help='Pass table type (1 or 2) if you want to focus on a particular one.')
	args = parser.parse_args()

	main(args.dataset)