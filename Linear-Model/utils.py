import csv
import json
import numpy as np 

def question2table():
	q2t = {}
	with open("seeded_question_train.json") as f:
	    json_data = json.load(f)
	for item in json_data:
	    question_id = item["question_id"]
	    table_id = item["table_id"]
	    q2t[question_id] = table_id
	with open("seeded_question_dev.json") as f:
	    json_data = json.load(f)
	for item in json_data:
	    question_id = item["question_id"]
	    table_id = item["table_id"]
	    q2t[question_id] = table_id
	return q2t

def load_row_feature(filepath):
    res = {}
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            question_id = int(row[0])
            table_id = int(row[1])
            row_id = int(row[2])
            score = float(row[3])
            res[(question_id, table_id, row_id)] = score
    return res

def load_column_header_feature(filepath):
    res = {}
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            question_id = int(row[0])
            table_id = int(row[1])
            column_id = int(row[2])
            score = float(row[3])
            res[(question_id, table_id, column_id)] = score
    return res

def load_row_header_feature(filepath):
    res = {}
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            question_id = int(row[0])
            table_id = int(row[1])
            score = float(row[2])
            res[(question_id, table_id)] = score
    return res

def load_cell_qf_sim_feature(filepath):
    res = {}
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            question_id = int(row[0])
            table_id = int(row[1])
            column_id = int(row[2])
            row_id = int(row[3])
            score = float(row[4])
            res[(question_id, table_id, column_id, row_id)] = score
    return res

def load_cell_sim_feature(filepath):
    res = {}
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            question_id = int(row[0])
            table_id = int(row[1])
            column_id = int(row[2])
            row_id = int(row[3])
            score = float(row[4])
            res[(question_id, table_id, column_id, row_id)] = score
    return res

def load_col_qtype_sim_feature(filepath):
    res = {}
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            question_id = int(row[0])
            table_id = int(row[1])
            column_id = int(row[2])
            score = float(row[3])
            res[(question_id, table_id, column_id)] = score
    return res

def load_correct_cells(train):
    def load_correct_cell(question_id, train=True):
        if train:
            with open("seeded_question_train.json") as f:
                json_data = json.load(f)
        else:
            question_id -= 1320
            with open("seeded_question_dev.json") as f:
                json_data = json.load(f)
        label = []
        label_data = json_data[question_id]
        for row in label_data["rows"]:
            for col in label_data["columns"]:
                label.append((row, col))
        return label
    start_id = 0 if train else 1320
    end_id = 1320 if train else 1721
    res = {}
    for question_id in range(start_id, end_id):
        res[question_id] = load_correct_cell(question_id, train)
    return res

