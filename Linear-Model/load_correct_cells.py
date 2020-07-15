import csv
import json

def load_correct_cells(train):
    def load_correct_cell(question_id, train=True):
        if train:
            with open("sayhearfall2018_train.json") as f:
                json_data = json.load(f)
            directory = json_data[question_id]["directory"]
            with open("train_cells.json") as f:
                label_data = json.load(f)
        else:
            question_id -= 238
            with open("sayhearfall2018_test.json") as f:
                json_data = json.load(f)
            directory = json_data[question_id]["directory"]
            with open("test_cells.json") as f:
                label_data = json.load(f)
        label = []
        for value in label_data.values():
            if directory in value["dirname"]:
                for item in value["query_execution"]["result"]:
                    label.append(item[0])
                break
        return label
    start_id = 0 if train else 238
    end_id = 238 if train else 302
    res = {}
    for question_id in range(start_id, end_id):
        res[question_id] = load_correct_cell(question_id, train)
        if len(res[question_id]) > 1:
        	print(question_id)
        	print(res[question_id])
    return res


load_correct_cells(True)