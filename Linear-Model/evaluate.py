import csv
import json
import numpy as np 
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import CondensedNearestNeighbour
from sklearn.ensemble import RandomForestClassifier
import pickle


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

row_question_hard_train = load_row_feature("seeded_features/row_question_hard_train.csv")
row_question_hard_test = load_row_feature("seeded_features/row_question_hard_test.csv")
row_question_soft_train = load_row_feature("seeded_features/row_question_soft_train.csv")
row_question_soft_test = load_row_feature("seeded_features/row_question_soft_test.csv")
column_header_question_hard_train = load_column_header_feature("seeded_features/column_header_question_hard_train.csv")
column_header_question_hard_test = load_column_header_feature("seeded_features/column_header_question_hard_test.csv")
column_header_question_soft_train = load_column_header_feature("seeded_features/column_header_question_soft_train.csv")
column_header_question_soft_test = load_column_header_feature("seeded_features/column_header_question_soft_test.csv")
row_header_question_hard_train = load_row_header_feature("seeded_features/row_header_question_hard_train.csv")
row_header_question_hard_test = load_row_header_feature("seeded_features/row_header_question_hard_test.csv")
row_header_question_soft_train = load_row_header_feature("seeded_features/row_header_question_soft_train.csv")
row_header_question_soft_test = load_row_header_feature("seeded_features/row_header_question_soft_test.csv")
col_qtype_sim_train = load_col_qtype_sim_feature("seeded_features/seeded_train_col_qtype_sim.csv")
col_qtype_sim_test = load_col_qtype_sim_feature("seeded_features/seeded_dev_col_qtype_sim.csv")

correct_cells_train = load_correct_cells(True)
correct_cells_test = load_correct_cells(False)

def prepare_data_train():
    start_id = 0
    end_id = 1320
    features = {}
    labels = {}
    for question_id in range(start_id, end_id):
        table_id = q2t[question_id]
        with open("tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
            reader = csv.reader(f)
            table_name = next(reader)
            headers = next(reader)
            for row_id, row in enumerate(reader):
                for column_id, _ in enumerate(row):
                    cell = (row_id, column_id)
                    # Load Features
                    feature = []
                    feature.append(row_question_hard_train[(question_id, table_id, row_id)])
                    feature.append(row_question_soft_train[(question_id, table_id, row_id)])
                    feature.append(column_header_question_hard_train[(question_id, table_id, column_id)])
                    feature.append(column_header_question_soft_train[(question_id, table_id, column_id)])
                    feature.append(row_header_question_hard_train[(question_id, table_id)])
                    feature.append(row_header_question_soft_train[(question_id, table_id)])
                    try:
                        feature.append(col_qtype_sim_train[(question_id, table_id, column_id)])
                    except:
                        feature.append(0.0)
                    features[(question_id, table_id, row_id, column_id)] = feature
                    # Load Label
                    label = 0
                    if cell in correct_cells_train[question_id]:
                        label = 1
                    labels[(question_id, table_id, row_id, column_id)] = label
    return features, labels

def prepare_data_test():
    start_id = 1320
    end_id = 1721
    features = {}
    labels = {}
    for question_id in range(start_id, end_id):
        table_id = q2t[question_id]
        with open("tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
            reader = csv.reader(f)
            table_name = next(reader)
            headers = next(reader)
            for row_id, row in enumerate(reader):
                for column_id, _ in enumerate(row):
                    cell = (row_id, column_id)
                    # Load Features
                    feature = []
                    feature.append(row_question_hard_test[(question_id, table_id, row_id)])
                    feature.append(row_question_soft_test[(question_id, table_id, row_id)])
                    feature.append(column_header_question_hard_test[(question_id, table_id, column_id)])
                    feature.append(column_header_question_soft_test[(question_id, table_id, column_id)])
                    feature.append(row_header_question_hard_test[(question_id, table_id)])
                    feature.append(row_header_question_soft_test[(question_id, table_id)])
                    try:
                        feature.append(col_qtype_sim_test[(question_id, table_id, column_id)])
                    except:
                        feature.append(0.0)
                    features[(question_id, table_id, row_id, column_id)] = feature

                    # Load Label
                    label = 0
                    if cell in correct_cells_test[question_id]:
                        label = 1
                    labels[(question_id, table_id, row_id, column_id)] = label
    return features, labels

train_features, train_labels = prepare_data_train()
test_features, test_labels = prepare_data_test()

train_features_np = []
train_labels_np = []
for i, key in enumerate(train_features.keys()):
    feature = train_features[key]
    label = train_labels[key]
    train_features_np.append(feature)
    train_labels_np.append(label)

train_features_np = np.array(train_features_np)
train_labels_np = np.array(train_labels_np)

test_features_np = []
test_labels_np = []
for i, key in enumerate(test_features.keys()):
    feature = test_features[key]
    label = test_labels[key]
    test_features_np.append(feature)
    test_labels_np.append(label)

test_features_np = np.array(test_features_np)
test_labels_np = np.array(test_labels_np)


# Handle imbalance data
sm = SMOTE()
train_features_np, train_labels_np = sm.fit_resample(train_features_np, train_labels_np)


classifier = LogisticRegression()
# classifier.fit(train_features_np, train_labels_np)
# pickle.dump(classifier, open("seeded_model.pkl", 'wb'))
classifier = pickle.load(open("seeded_model.pkl", 'rb'))

pred_result = {}
for i, key in enumerate(test_features.keys()):
    feature = np.array([test_features[key]])
    pred = classifier.predict(feature)[0]
    question_id = key[0]
    if pred == 1:
        if question_id not in pred_result:
            pred_result[question_id] = [(key[2], key[3])]
        else:
            pred_result[question_id].append((key[2], key[3]))

label_cell = {}
for i, key in enumerate(test_labels.keys()):
    if test_labels[key] == 1:
        question_id = key[0]
        if question_id not in label_cell:
            label_cell[question_id] = [(key[2], key[3])]
        else:
            label_cell[question_id].append((key[2], key[3]))


all_precision = 0.0
all_recall = 0.0
all_f1 = 0.0
cnt = 0.0
save_json_data = []
for question_id in label_cell.keys():
    save_data = {}
    recall = 0.0
    precision = 0.0
    try:
        pred = pred_result[question_id]
    except:
        pred = []
    true = label_cell[question_id]
    for tup in pred:
        if tup in true:
            precision += 1.0
    for tup in true:
        if tup in pred:
            recall += 1.0
    if len(pred) != 0:
        precision /= len(pred)
    else:
        precision = 0.0
    if len(true) != 0:
        recall /= len(true)
    else:
        recall = 0.0
    all_precision += precision
    all_recall += recall
    f1 = 2 * precision * recall / (precision + recall) if precision + recall != 0.0 else 0.0
    all_f1 += f1
    cnt += 1.0

print("Number of quesionts: {}".format(cnt))
print("Precision: {}".format(all_precision / cnt))
print("Recall: {}".format(all_recall / cnt))
print("F1: {}".format(all_f1 / cnt))

















































