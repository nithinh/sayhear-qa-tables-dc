import json
import os
import csv
from itertools import izip
import pandas as pd
import re
import csv
import time
import shutil

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()

        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


with open('test_annotated.json') as json_data:
    d_list = json.load(json_data)
    #print(d)
kv_tables = []
e_t = []
for dic in d_list:
	if dic['table_type'] == 2:
		kv_tables.append(dic['id'])
	else:
		e_t.append(dic['id'])


tables_set = os.listdir('tables/test/original_tables')
print kv_tables

#time.sleep(20)

i = 0
for tab in kv_tables:
	header = []
	subjects = []
	tablename = ""
	inpfile = "tables/test/original_tables/" + str(tab) + ".csv"
	print inpfile
	outputfile = "tables/test_transposed/" + str(tab) + ".csv"
	with open(inpfile,"r") as input:
		tablename = input.readline()
		
	current_df = pd.read_csv(inpfile, header=1)
	if 'url' in current_df:
		change_df = current_df.drop(['url'], axis=1)
	else:
		change_df = current_df
	col = change_df.columns[0]
	#print change_df
	print change_df.T
	n = len(change_df.columns)
		
	change_df.T.to_csv(outputfile,header=False)

	df = pd.read_csv(outputfile)
	df = df.drop(col, axis=1)
	df.to_csv(outputfile,index=False)
	line_prepender(outputfile,tablename)
		

for tab in e_t:
	inpfile = "tables/test/original_tables/" + str(tab) + ".csv"
	
	outputfile = "tables/test_transposed/" + str(tab) + ".csv"

	shutil.copy(inpfile,outputfile)


