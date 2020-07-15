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


table_features_train = load_table_feature("features/table_features_train.csv", True)
table_features_test = load_table_feature("features/table_features_dev.csv", False)
table_features_tfidf_train = load_table_feature("features/table_features_train_tfidf.csv", True)
table_features_tfidf_test = load_table_feature("features/table_features_dev_tfidf.csv", False)
table_features_soft_train = load_table_feature("features/table_features_soft_train.csv", True)
table_features_soft_test = load_table_feature("features/table_features_soft_dev.csv", False)
row_question_hard_train = load_row_feature("features/row_question_hard_train.csv")
row_question_hard_test = load_row_feature("features/row_question_hard_test.csv")
column_header_question_hard_train = load_column_header_feature("features/column_header_question_hard_train.csv")
column_header_question_hard_test = load_column_header_feature("features/column_header_question_hard_test.csv")
column_header_question_soft_train = load_column_header_feature("features/column_header_question_soft_train.csv")
column_header_question_soft_test = load_column_header_feature("features/column_header_question_soft_test.csv")
row_header_question_hard_train = load_row_header_feature("features/row_header_question_hard_train.csv")
row_header_question_hard_test = load_row_header_feature("features/row_header_question_hard_test.csv")
# cell_qf_sim_train = load_cell_qf_sim_feature("features/cell_qf_sim_train.csv")
# cell_qf_sim_test = load_cell_qf_sim_feature("features/cell_qf_sim_test.csv")
# cell_sim_train = load_cell_sim_feature("features/cell_sim_train.csv")
# cell_sim_test = load_cell_sim_feature("features/cell_sim_test.csv")
# col_qtype_sim_train = load_col_qtype_sim_feature("features/col_qtype_sim_train.csv")
# col_qtype_sim_test = load_col_qtype_sim_feature("features/col_qtype_sim_test.csv")

correct_cells_train = load_correct_cells(True)
correct_cells_test = load_correct_cells(False)

def prepare_data_train():
    start_id = 0
    end_id = 238
    features = {}
    labels = {}
    for question_id in range(start_id, end_id):
        for table_id in range(start_id, end_id):
            with open("tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
                reader = csv.reader(f)
                table_name = next(reader)
                headers = next(reader)
                for row_id, row in enumerate(reader):
                    for column_id, cell in enumerate(row):
                        # Load Features
                        feature = []
                        feature.append(table_features_train[(question_id, table_id)])
                        feature.append(table_features_tfidf_train[(question_id, table_id)])
                        feature.append(table_features_soft_train[(question_id, table_id)])
                        feature.append(row_question_hard_train[(question_id, table_id, row_id)])
                        feature.append(column_header_question_hard_train[(question_id, table_id, column_id)])
                        feature.append(column_header_question_soft_train[(question_id, table_id, column_id)])
                        feature.append(row_header_question_hard_train[(question_id, table_id)])
                        # try:
                        #     feature.append(cell_qf_sim_train[(question_id, table_id, column_id, row_id)])
                        # except:
                        #     feature.append(0.0)
                        # try:
                        #     feature.append(cell_sim_train[(question_id, table_id, column_id, row_id)])
                        # except:
                        #     feature.append(0.0)
                        # try:
                        #     feature.append(col_qtype_sim_train[(question_id, table_id, column_id)])
                        # except:
                        #     feature.append(0.0)
                        features[(question_id, table_id, row_id, column_id)] = feature

                        # Load Label
                        label = 0
                        if question_id == table_id:
                            if cell in correct_cells_train[question_id]:
                                label = 1
                        labels[(question_id, table_id, row_id, column_id)] = label
    return features, labels

def prepare_data_test():
    start_id = 238
    end_id = 302
    features = {}
    labels = {}
    for question_id in range(start_id, end_id):
        for table_id in range(start_id, end_id):
            with open("tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
                reader = csv.reader(f)
                table_name = next(reader)
                headers = next(reader)
                for row_id, row in enumerate(reader):
                    for column_id, cell in enumerate(row):
                        # Load Features
                        feature = []
                        feature.append(table_features_test[(question_id, table_id)])
                        feature.append(table_features_tfidf_test[(question_id, table_id)])
                        feature.append(table_features_soft_test[(question_id, table_id)])
                        feature.append(row_question_hard_test[(question_id, table_id, row_id)])
                        feature.append(column_header_question_hard_test[(question_id, table_id, column_id)])
                        feature.append(column_header_question_soft_test[(question_id, table_id, column_id)])
                        feature.append(row_header_question_hard_test[(question_id, table_id)])
                        # try:
                        #     feature.append(cell_qf_sim_test[(question_id, table_id, column_id, row_id)])
                        # except:
                        #     feature.append(0.0)
                        # try:
                        #     feature.append(cell_sim_test[(question_id, table_id, column_id, row_id)])
                        # except:
                        #     feature.append(0.0)
                        # try:
                        #     feature.append(col_qtype_sim_test[(question_id, table_id, column_id)])
                        # except:
                        #     feature.append(0.0)
                        features[(question_id, table_id, row_id, column_id)] = feature

                        # Load Label
                        label = 0
                        if question_id == table_id:
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
    # if label == 0:
    #     if i % 17940 != 0:
    #         continue
    train_features_np.append(feature)
    train_labels_np.append(label)

train_features_np = np.array(train_features_np)
train_labels_np = np.array(train_labels_np)

# Normalize
# mean = np.mean(train_features_np, axis = 0)
# std = np.std(train_features_np, axis = 0)
# train_features_np = (train_features_np - mean) / std


# Handle imbalance data
# sm = SMOTE()
# train_features_np_balanced, train_labels_np_balanced = sm.fit_resample(train_features_np, train_labels_np)
# cnn = CondensedNearestNeighbour()
# train_features_np, train_labels_np = cnn.fit_resample(train_features_np, train_labels_np)


# PCA
from sklearn.decomposition import PCA
print("PAC...")
pca = PCA(n_components = 2)
pca.fit(train_features_np)
x_new = pca.transform(train_features_np)
print(x_new.shape)
print(train_labels_np.shape)
np.save("x", x_new)
np.save("y", train_labels_np)
exit()


classifier = LogisticRegression(class_weight = "balanced")
# classifier = tree.DecisionTreeClassifier()
# classifier = SVC()
# classifier = RandomForestClassifier(n_estimators=100, max_depth=2)
classifier.fit(train_features_np_balanced, train_labels_np_balanced)


test_features_np = []
test_labels_np = []
for i, key in enumerate(test_features.keys()):
    feature = test_features[key]
    label = test_labels[key]
    test_features_np.append(feature)
    test_labels_np.append(label)
test_features_np = np.array(test_features_np)
test_labels_np = np.array(test_labels_np)

# Normalize
# mean = np.mean(test_features_np, axis = 0)
# std = np.std(test_features_np, axis = 0)
# test_features_np = (test_features_np - mean) / std

pred_y = classifier.predict(train_features_np_balanced)

l1p1 = 0
l1p0 = 0
l0p1 = 0
l0p0 = 0
for i in range(len(train_labels_np_balanced)):
    if train_labels_np_balanced[i] == 1:
        if pred_y[i] == 1:
            l1p1 += 1
        else:
            l1p0 += 1
    else:
        if pred_y[i] == 1:
            l0p1 += 1
        else:
            l0p0 += 1
print()
print("Training set")
print("l1p1: {}".format(l1p1))
print("l1p0: {}".format(l1p0))
print("l0p1: {}".format(l0p1))
print("l0p0: {}".format(l0p0))

















































