import csv
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import nltk
import io
import pickle
import os
from progress.bar import Bar
import numpy as np 


q2t = {}
with open("../seeded_question_train.json") as f:
    json_data = json.load(f)
for item in json_data:
    question_id = item["question_id"]
    table_id = item["table_id"]
    q2t[question_id] = table_id
with open("../seeded_question_dev.json") as f:
    json_data = json.load(f)
for item in json_data:
    question_id = item["question_id"]
    table_id = item["table_id"]
    q2t[question_id] = table_id


def load_vectors(fname):
    # if os.path.exists("word2vec.pickle"):
    #     with open("word2vec.pickle", "rb") as f:
    #         return pickle.load(f)
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    bar = Bar('Loading Word Embeddings...', max = 100)
    for i, line in enumerate(fin):
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = list(map(float, tokens[1:]))
        if i % 10000 == 0:
            bar.next()
    bar.finish()
    # with open("word2vec.pickle", "wb") as f:
    #     pickle.dump(data, f)
    return data

def get_question(question_id, exclude_focus):
    idx = question_id
    if question_id >= 1320:
        idx -= 1320
        json_file = ("../seeded_question_dev.json")
    else:
        json_file = ("../seeded_question_train.json")
    with open(json_file) as f:
        json_data = json.load(f)
    question = [word for word in json_data[idx]["question_parsed"] if word != ""]
    if exclude_focus == False:
        return question
    pos_tag_question = nltk.pos_tag(question)
    question = [tup[0] for tup in pos_tag_question if tup[1][0] != "W"]
    return question


def get_ratio_hard_version(question_words, source_words):
    ps = PorterStemmer()
    question_stems = [ps.stem(word) for word in question_words if word != ""]
    source_stems = [ps.stem(word) for word in source_words if word != ""]
    cnt = 0.0
    for stem in source_stems:
        if stem in question_stems:
            cnt += 1.0
    if len(source_stems) == 0:
        return 0.0
    return cnt / float(len(source_stems))

word_vectors = load_vectors("../wiki-news-300d-1M.vec")

def cosine_similarity(vec1, vec2):
    return np.sum(vec1 * vec2) / (np.sqrt(np.sum(np.square(vec1))) * np.sqrt(np.sum(np.square(vec2))))

def max_sim(wi, S2):
    res = 0.0
    vec1 = np.array(word_vectors[wi])
    for wj in S2:
        vec2 = np.array(word_vectors[wj])
        sim = cosine_similarity(vec1, vec2)
        res = max(res, sim)
    return res



def get_ratio_soft_version(question_words, source_words):
    question_stems = [word.lower() for word in question_words if word != "" and word.lower() in word_vectors]
    source_stems = [word.lower() for word in source_words if word != "" and word.lower() in word_vectors]
    score = 0.0
    for wi in source_stems:
        score += max_sim(wi, question_stems)
    if len(source_stems) == 0:
        return 0.0
    return score / float(len(source_stems))




def row_question_score(question_id, table_id, exclude_focus):
    res = {}
    question_words = get_question(question_id, exclude_focus)
    with open("../tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        table_name = next(reader)
        headers = next(reader)
        for row_id, r in enumerate(reader):
            row = []
            for cell in r:
                if "http" in cell:
                    continue
                words = re.split(r'[^0-9a-zA-Z]', cell)
                words = [word for word in words if word != ""]
                row += words
            score = get_ratio_hard_version(question_words, row)
            res[row_id] = score
    return res

def row_question_score_soft(question_id, table_id, exclude_focus):
    res = {}
    question_words = get_question(question_id, exclude_focus)
    with open("../tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
        reader = csv.reader(f)
        table_name = next(reader)
        headers = next(reader)
        for row_id, r in enumerate(reader):
            row = []
            for cell in r:
                if "http" in cell:
                    continue
                words = re.split(r'[^0-9a-zA-Z]', cell)
                words = [word for word in words if word != ""]
                row += words
            score = get_ratio_soft_version(question_words, row)
            res[row_id] = score
    return res

def row_question_features(train, exclude_focus, filename):
    start_id = 0 if train else 1320
    end_id = 1320 if train else 1721
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["question_id", "table_id", "row_id", "score"])
        bar = Bar('Generating Features...', max = end_id - start_id)
        for question_id in range(start_id, end_id):
            table_id = q2t[question_id]
            scores = row_question_score(question_id, table_id, exclude_focus)
            for row_id in scores.keys():
                score = scores[row_id]
                writer.writerow([question_id, table_id, row_id, score])
            bar.next()
        bar.finish()

def row_question_features_soft(train, exclude_focus, filename):
    start_id = 0 if train else 1320
    end_id = 1320 if train else 1721
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["question_id", "table_id", "row_id", "score"])
        bar = Bar('Generating Features...', max = end_id - start_id)
        for question_id in range(start_id, end_id):
            table_id = q2t[question_id]
            scores = row_question_score_soft(question_id, table_id, exclude_focus)
            for row_id in scores.keys():
                score = scores[row_id]
                writer.writerow([question_id, table_id, row_id, score])
            bar.next()
        bar.finish()

def row_header_features(train, filename):
    start_id = 0 if train else 1320
    end_id = 1320 if train else 1721
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["question_id", "table_id", "score"])
        bar = Bar('Generating Features...', max = end_id - start_id)
        for question_id in range(start_id, end_id):
            question_words = get_question(question_id, exclude_focus = False)
            table_id = q2t[question_id]
            with open("../tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
                reader = csv.reader(f)
                table_name = next(reader)
                headers = next(reader)
                header_row = []
                for cell in headers:
                    words = re.split(r'[^0-9a-zA-Z]', cell)
                    words = [word for word in words if word != "" and word.lower() != "url"]
                    header_row += words
                score = get_ratio_hard_version(question_words, header_row)
                writer.writerow([question_id, table_id, score])
            bar.next()
        bar.finish()

def row_header_features_soft(train, filename):
    start_id = 0 if train else 1320
    end_id = 1320 if train else 1721
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["question_id", "table_id", "score"])
        bar = Bar('Generating Features...', max = end_id - start_id)
        for question_id in range(start_id, end_id):
            question_words = get_question(question_id, exclude_focus = False)
            table_id = q2t[question_id]
            with open("../tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
                reader = csv.reader(f)
                table_name = next(reader)
                headers = next(reader)
                header_row = []
                for cell in headers:
                    words = re.split(r'[^0-9a-zA-Z]', cell)
                    words = [word for word in words if word != "" and word.lower() != "url"]
                    header_row += words
                score = get_ratio_soft_version(question_words, header_row)
                writer.writerow([question_id, table_id, score])
            bar.next()
        bar.finish()

def column_header_features(train, filename):
    start_id = 0 if train else 1320
    end_id = 1320 if train else 1721
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["question_id", "table_id", "column_id", "score"])
        bar = Bar('Generating Features...', max = end_id - start_id)
        for question_id in range(start_id, end_id):
            question_words = get_question(question_id, exclude_focus = False)
            table_id = q2t[question_id]
            with open("../tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
                reader = csv.reader(f)
                table_name = next(reader)
                headers = next(reader)
                header_row = []
                for column_id, cell in enumerate(headers):
                    words = re.split(r'[^0-9a-zA-Z]', cell)
                    words = [word for word in words if word != ""]
                    score = get_ratio_hard_version(question_words, words)
                    writer.writerow([question_id, table_id, column_id, score])
            bar.next()
        bar.finish()

def column_header_features_soft(train, filename):
    start_id = 0 if train else 1320
    end_id = 1320 if train else 1721
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["question_id", "table_id", "column_id", "score"])
        bar = Bar('Generating Features...', max = end_id - start_id)
        for question_id in range(start_id, end_id):
            question_words = get_question(question_id, exclude_focus = False)
            table_id = q2t[question_id]
            with open("../tables/{}.csv".format(table_id), encoding="ISO-8859-1") as f:
                reader = csv.reader(f)
                table_name = next(reader)
                headers = next(reader)
                header_row = []
                for column_id, cell in enumerate(headers):
                    words = re.split(r'[^0-9a-zA-Z]', cell)
                    words = [word for word in words if word != ""]
                    score = get_ratio_soft_version(question_words, words)
                    writer.writerow([question_id, table_id, column_id, score])
            bar.next()
        bar.finish()
            

if __name__ == "__main__":
    # column_header_features(train = False, filename = "column_header_question_hard_test.csv")
    # column_header_features(train = True, filename = "column_header_question_hard_train.csv")
    # row_header_features(train = False, filename = "row_header_question_hard_test.csv")
    # row_header_features(train = True, filename = "row_header_question_hard_train.csv")
    # row_question_features(train = False, exclude_focus = False, filename = "row_question_hard_test.csv")
    # row_question_features(train = True, exclude_focus = False, filename = "row_question_hard_train.csv")
    
    # column_header_features_soft(train = False, filename = "column_header_question_soft_test.csv")
    # column_header_features_soft(train = True, filename = "column_header_question_soft_train.csv")

    # word2vec = load_vectors("../wiki-news-300d-1M.vec")

    row_header_features_soft(train = False, filename = "row_header_question_soft_test.csv")
    row_header_features_soft(train = True, filename = "row_header_question_soft_train.csv")
    row_question_features_soft(train = False, exclude_focus = False, filename = "row_question_soft_test.csv")
    row_question_features_soft(train = True, exclude_focus = False, filename = "row_question_soft_train.csv")













