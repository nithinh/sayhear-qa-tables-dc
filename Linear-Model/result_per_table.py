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

def load_table_feature(filepath, train):
    res = {}
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            table_id = int(row[0])
            if not train:
                table_id += 238
            question_id = int(row[1])
            if not train:
                question_id += 238
            score = float(row[2])
            res[(question_id, table_id)] = score
    return res

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
    return res

def load_n_rows_feature():
    res = {}
    for i in range(302):
        with open("tables/{}.csv".format(i)) as f:
            reader = csv.reader(f)
            table_name = next(reader)
            header = next(reader)
            n_row = 0
            for row in reader:
                n_row += 1
        res[i] = n_row
    return res


# table_features_train = load_table_feature("features/table_features_train.csv", True)
# table_features_test = load_table_feature("features/table_features_dev.csv", False)
# table_features_tfidf_train = load_table_feature("features/table_features_train_tfidf.csv", True)
# table_features_tfidf_test = load_table_feature("features/table_features_dev_tfidf.csv", False)
# table_features_soft_train = load_table_feature("features/table_features_soft_train.csv", True)
# table_features_soft_test = load_table_feature("features/table_features_soft_dev.csv", False)
row_question_hard_train = load_row_feature("features/row_question_hard_train.csv")
row_question_hard_test = load_row_feature("features/row_question_hard_test.csv")
row_question_soft_train = load_row_feature("features/row_question_soft_train.csv")
row_question_soft_test = load_row_feature("features/row_question_soft_test.csv")
column_header_question_hard_train = load_column_header_feature("features/column_header_question_hard_train.csv")
column_header_question_hard_test = load_column_header_feature("features/column_header_question_hard_test.csv")
column_header_question_soft_train = load_column_header_feature("features/column_header_question_soft_train.csv")
column_header_question_soft_test = load_column_header_feature("features/column_header_question_soft_test.csv")
row_header_question_hard_train = load_row_header_feature("features/row_header_question_hard_train.csv")
row_header_question_hard_test = load_row_header_feature("features/row_header_question_hard_test.csv")
row_header_question_soft_train = load_row_header_feature("features/row_header_question_soft_train.csv")
row_header_question_soft_test = load_row_header_feature("features/row_header_question_soft_test.csv")
# cell_qf_sim_train = load_cell_qf_sim_feature("features/cell_qf_sim_train.csv")
# cell_qf_sim_test = load_cell_qf_sim_feature("features/cell_qf_sim_test.csv")
# cell_sim_train = load_cell_sim_feature("features/cell_sim_train.csv")
# cell_sim_test = load_cell_sim_feature("features/cell_sim_test.csv")
col_qtype_sim_train = load_col_qtype_sim_feature("features/col_qtype_sim_train.csv")
col_qtype_sim_test = load_col_qtype_sim_feature("features/col_qtype_sim_test.csv")
n_rows = load_n_rows_feature()

correct_cells_train = load_correct_cells(True)
correct_cells_test = load_correct_cells(False)

def prepare_data_train():
    start_id = 0
    end_id = 238
    features = {}
    labels = {}
    for question_id in range(start_id, end_id):
        for table_id in range(start_id, end_id):
            if question_id != table_id:
                continue
            with open("tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
                reader = csv.reader(f)
                table_name = next(reader)
                headers = next(reader)
                for row_id, row in enumerate(reader):
                    for column_id, cell in enumerate(row):
                        # Load Features
                        feature = []
                        # feature.append(table_features_train[(question_id, table_id)])
                        # feature.append(table_features_tfidf_train[(question_id, table_id)])
                        # feature.append(table_features_soft_train[(question_id, table_id)])
                        feature.append(row_question_hard_train[(question_id, table_id, row_id)])
                        feature.append(row_question_soft_train[(question_id, table_id, row_id)])
                        feature.append(column_header_question_hard_train[(question_id, table_id, column_id)])
                        feature.append(column_header_question_soft_train[(question_id, table_id, column_id)])
                        feature.append(row_header_question_hard_train[(question_id, table_id)])
                        feature.append(row_header_question_soft_train[(question_id, table_id)])
                        # try:
                        #     feature.append(cell_qf_sim_train[(question_id, table_id, column_id, row_id)])
                        # except:
                        #     feature.append(0.0)
                        # try:
                        #     feature.append(cell_sim_train[(question_id, table_id, column_id, row_id)])
                        # except:
                        #     feature.append(0.0)
                        try:
                            feature.append(col_qtype_sim_train[(question_id, table_id, column_id)])
                        except:
                            feature.append(0.0)
                        feature.append(n_rows[table_id])
                        features[(question_id, table_id, row_id, column_id)] = feature

                        # Load Label
                        label = 0
                        if question_id == table_id:
                            if cell in correct_cells_train[question_id]:
                                label = 1
                        labels[(question_id, table_id, row_id, column_id)] = label
    features = per_table_normalization(features)
    return features, labels

def prepare_data_test():
    start_id = 238
    end_id = 302
    features = {}
    labels = {}
    for question_id in range(start_id, end_id):
        for table_id in range(start_id, end_id):
            if question_id != table_id:
                continue
            with open("tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
                reader = csv.reader(f)
                table_name = next(reader)
                headers = next(reader)
                for row_id, row in enumerate(reader):
                    for column_id, cell in enumerate(row):
                        # Load Features
                        feature = []
                        # feature.append(table_features_test[(question_id, table_id)])
                        # feature.append(table_features_tfidf_test[(question_id, table_id)])
                        # feature.append(table_features_soft_test[(question_id, table_id)])
                        feature.append(row_question_hard_test[(question_id, table_id, row_id)])
                        feature.append(row_question_soft_test[(question_id, table_id, row_id)])
                        feature.append(column_header_question_hard_test[(question_id, table_id, column_id)])
                        feature.append(column_header_question_soft_test[(question_id, table_id, column_id)])
                        feature.append(row_header_question_hard_test[(question_id, table_id)])
                        feature.append(row_header_question_soft_test[(question_id, table_id)])
                        # try:
                        #     feature.append(cell_qf_sim_test[(question_id, table_id, column_id, row_id)])
                        # except:
                        #     feature.append(0.0)
                        # try:
                        #     feature.append(cell_sim_test[(question_id, table_id, column_id, row_id)])
                        # except:
                        #     feature.append(0.0)
                        try:
                            feature.append(col_qtype_sim_test[(question_id, table_id, column_id)])
                        except:
                            feature.append(0.0)
                        feature.append(n_rows[question_id])
                        features[(question_id, table_id, row_id, column_id)] = feature

                        # Load Label
                        label = 0
                        if question_id == table_id:
                            if cell in correct_cells_test[question_id]:
                                label = 1
                        labels[(question_id, table_id, row_id, column_id)] = label
    features = per_table_normalization(features)
    return features, labels

def per_table_normalization(features):
    per_table_features = {}
    per_table_mean = {}
    per_table_std = {}
    for key in features.keys():
        table_id = key[1]
        if table_id not in per_table_features:
            per_table_features[table_id] = [features[key]]
        else:
            per_table_features[table_id].append(features[key])
    for table_id in per_table_features.keys():
        per_table_features[table_id] = np.array(per_table_features[table_id])
        per_table_mean[table_id] = np.mean(per_table_features[table_id], axis = 0)
        per_table_std[table_id] = np.std(per_table_features[table_id], axis = 0) + 1e-7
    for key in features.keys():
        table_id = key[1]
        features[key] = (features[key] - per_table_mean[table_id]) / per_table_std[table_id]
    return features

train_features, train_labels = prepare_data_train()
test_features, test_labels = prepare_data_test()

train_features_np = []
train_labels_np = []
for i, key in enumerate(train_features.keys()):
    feature = train_features[key]
    label = train_labels[key]
    # if label == 0:
    #     if i % 17940 != 0:
    #         continue
    train_features_np.append(feature)
    train_labels_np.append(label)

train_features_np = np.array(train_features_np)
train_labels_np = np.array(train_labels_np)

test_features_np = []
test_labels_np = []
for i, key in enumerate(test_features.keys()):
    feature = test_features[key]
    label = test_labels[key]
    # if label == 0:
    #     if i % 17940 != 0:
    #         continue
    test_features_np.append(feature)
    test_labels_np.append(label)

test_features_np = np.array(test_features_np)
test_labels_np = np.array(test_labels_np)

# Normalize
# mean = np.mean(train_features_np, axis = 0)
# std = np.std(train_features_np, axis = 0)
# train_features_np = (train_features_np - mean) / std


# Handle imbalance data
sm = SMOTE()
train_features_np, train_labels_np = sm.fit_resample(train_features_np, train_labels_np)
# cnn = CondensedNearestNeighbour()
# train_features_np, train_labels_np = cnn.fit_resample(train_features_np, train_labels_np)


classifier = LogisticRegression()
# classifier = tree.DecisionTreeClassifier()
# classifier = SVC()
# classifier = RandomForestClassifier(n_estimators=100, max_depth=2)
classifier.fit(train_features_np, train_labels_np)
# pickle.dump(classifier, open("original_model.pkl", 'wb'))
# classifier = pickle.load(open("original_model.pkl", 'rb'))
# classifier = pickle.load(open("seeded_model.pkl", 'rb'))
print(np.hstack((classifier.intercept_[:,None], classifier.coef_)))

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

# pred_result = {}
# for i, key in enumerate(train_features.keys()):
#     feature = np.array([train_features[key]])
#     pred = classifier.predict(feature)[0]
#     question_id = key[0]
#     if pred == 1:
#         if question_id not in pred_result:
#             pred_result[question_id] = [(key[2], key[3])]
#         else:
#             pred_result[question_id].append((key[2], key[3]))

# label_cell = {}
# for i, key in enumerate(train_labels.keys()):
#     if train_labels[key] == 1:
#         question_id = key[0]
#         if question_id not in label_cell:
#             label_cell[question_id] = [(key[2], key[3])]
#         else:
#             label_cell[question_id].append((key[2], key[3]))

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
    save_data["question_id"] = question_id
    save_data["table_id"] = question_id
    save_data["golden_cells"] = [tuple(item) for item in true]
    save_data["predict_cells"] = [tuple(item) for item in pred]
    save_data["precision"] = precision
    save_data["recall"] = recall
    save_data["f1"] = f1
    save_json_data.append(save_data)
with open("hovy_original_result.json", "w") as f:
    json.dump(save_json_data, f, sort_keys = True, indent = 4, separators = (',', ': '))


print("Precision: {}".format(all_precision / cnt))
print("Recall: {}".format(all_recall / cnt))
print("F1: {}".format(all_f1 / cnt))



# Normalize
# mean = np.mean(test_features_np, axis = 0)
# std = np.std(test_features_np, axis = 0)
# test_features_np = (test_features_np - mean) / std

















































