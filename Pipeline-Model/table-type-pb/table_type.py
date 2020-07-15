import csv
import argparse
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score,recall_score, precision_score


def predict_ad_hoc(example):
	if example[0,2] == 1:
		return 2
	else :
		return 1

def read_dataset(dataset):
	M = list()
	col_indexes = dict()
	with open(dataset,'r') as f:
		csv_reader = csv.reader(f)
		for i,row in enumerate(csv_reader):
			if i >0 :
				new_row = list()
				for elt in row:
					new_row.append(float(elt))
				M.append(new_row)
	matrix_of_examples = np.matrix(M)
	return matrix_of_examples

def get_X_Y(dataset):
	matrix_of_examples = read_dataset(dataset)
	Y = matrix_of_examples[1:,1].getA1()
	X = matrix_of_examples[1:,2:]
	return X,Y

def get_X_Y_type1_tables(dataset):
	M = read_dataset(dataset)
	M = np.array(M)
	M = M[M[:,1]==1]
	M = np.matrix(M)
	Y = M[1:,1].getA1()
	X = M[1:,2:]
	return X,Y	

def logistic_regression(X_train,Y_train,X_test,Y_test):

	lr_classifier = LogisticRegression()
	lr_classifier.fit(X_train,Y_train)
	# print(X,Y)
	err = error(X_train,Y_train,lr_classifier.predict)
	print('Error on training set:%.6f'%err)
	err = error(X_test,Y_test,lr_classifier.predict)
	print('Error on test set:%.6f'%err)


def ad_hoc_classification(X_train,Y_train,X_test,Y_test):
	err = error(X_train,Y_train,predict_ad_hoc)
	print('Error on train set:%.6f'%err)
	err = error(X_test,Y_test,predict_ad_hoc)
	print('Error on test set:%.6f'%err)

def decision_tree(X_train,Y_train,X_test,Y_test):
	## get best max depth using cross-validation
	n_row, n_col = X_train.shape
	err_list = list()
	for depth in range(1,n_col):
		n_folds = 10
		k = n_row / n_folds
		err_list_cv = list()
		j = 0
		for i in range(n_folds):
			if j == 0:
				## first fold
				X_train_cv, Y_train_cv = X_train[j+k:,:], Y_train[j+k:]
				X_cv, Y_cv = X_train[j:j+k,:], Y_train[j:j+k]
			if (j+k) >n_row:
				## last fold
				X_train_cv, Y_train_cv = X_train[0:j,:], Y_train[0:j]
				X_cv, Y_cv = X_train[j:,:], Y_train[j:]
			else:
				X_train_cv, Y_train_cv = np.concatenate((X_train[0:j,:],X_train[j+k:,:])), np.concatenate((Y_train[0:j],Y_train[j+k:]))
				X_cv, Y_cv = X_train[j:j+k], Y_train[j:j+k]

			dt_classifier = DecisionTreeClassifier(criterion='entropy',max_depth=depth)
			dt_classifier.fit(X_train_cv,Y_train_cv)
			err = error(X_cv,Y_cv,dt_classifier.predict)
			err_list_cv.append(err)
			j += k
		err_list.append(np.average(np.array(err_list_cv)))

	# print(err_list)
	# print(best_depth)

	best_depth = err_list.index(min(err_list)) + 1

	## retrain on all train set and get error
	dt_classifier = DecisionTreeClassifier(criterion='entropy',max_depth=best_depth)
	dt_classifier.fit(X_train,Y_train)
	err = error(X_train,Y_train,dt_classifier.predict)
	print('Error on train set:%.6f'%err)
	err = error(X_test,Y_test,dt_classifier.predict)
	print('Error on train set:%.6f'%err)

def KNN(X_train,Y_train,X_test,Y_test):
	n_row, n_col = X_train.shape
	err_list = list()
	for neighbors in range(1,n_row/2):
		n_folds = 10
		k = n_row / n_folds
		err_list_cv = list()
		j = 0
		for i in range(n_folds):
			if j == 0:
				## first fold
				X_train_cv, Y_train_cv = X_train[j+k:,:], Y_train[j+k:]
				X_cv, Y_cv = X_train[j:j+k,:], Y_train[j:j+k]
			if (j+k) >n_row:
				## last fold
				X_train_cv, Y_train_cv = X_train[0:j,:], Y_train[0:j]
				X_cv, Y_cv = X_train[j:,:], Y_train[j:]
			else:
				X_train_cv, Y_train_cv = np.concatenate((X_train[0:j,:],X_train[j+k:,:])), np.concatenate((Y_train[0:j],Y_train[j+k:]))
				X_cv, Y_cv = X_train[j:j+k], Y_train[j:j+k]

			knn_classifier = KNeighborsClassifier(n_neighbors=neighbors)
			knn_classifier.fit(X_train_cv,Y_train_cv)
			err = error(X_cv,Y_cv,knn_classifier.predict)
			err_list_cv.append(err)
			j += k
		err_list.append(np.average(np.array(err_list_cv)))

	best_n_neighbors = err_list.index(min(err_list)) + 1

	knn_classifier = KNeighborsClassifier(n_neighbors = best_n_neighbors)
	knn_classifier.fit(X_train,Y_train)
	err = error(X_train,Y_train,knn_classifier.predict)
	print('Error on train set:%.6f'%err)
	err = error(X_test,Y_test,knn_classifier.predict)
	print('Error on train set:%.6f'%err)


def error(X,Y,prediction_function):
	n_row, n_col = X.shape
	n_ex_OK = 0
	for i in range(n_row):
		ex = X[i]
		prediction = prediction_function(ex)
		if prediction == Y[i]:
			n_ex_OK += 1
	err = float(n_row - n_ex_OK) / n_row
	return err

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Predicts the type of table.')
	parser.add_argument('train_set', metavar='train_set', type=str, help='Path to the CSV of the train set.')
	parser.add_argument('test_set', metavar='test_set', type=str, help='Path to the CSV of the test set.')
	parser.add_argument('--word2vec_model', metavar='word2vec_model', nargs='?', const='false', type=str, help='Pass a word2vec model if needed.')
	
	args = parser.parse_args()

	X_train,Y_train = get_X_Y(args.train_set)
	X_test,Y_test = get_X_Y(args.test_set)
	# print('error:%.4f'%error(M,col_indexes))

	print('Logistic regression:')
	logistic_regression(X_train,Y_train,X_test,Y_test)

	X_train_ignoring_col_headers, X_test_ignoring_col_headers = np.delete(X_train,2,1), np.delete(X_test,2,1)
	print('\nLogistic regression when ignoring column header:')
	logistic_regression(X_train_ignoring_col_headers,Y_train,X_test_ignoring_col_headers,Y_test)

	print('\nAd hoc classification:')
	ad_hoc_classification(X_train,Y_train,X_test,Y_test)

	print('\nDecision tree classification:')
	decision_tree(X_train,Y_train,X_test,Y_test)

	print('\nDecision tree classification when ignoring column header:')
	decision_tree(X_train_ignoring_col_headers,Y_train,X_test_ignoring_col_headers,Y_test)

	print('\nKNN classification:')
	KNN(X_train,Y_train,X_test,Y_test)

	print('\nKNN classification when ignoring column header:')
	KNN(X_train_ignoring_col_headers,Y_train,X_test_ignoring_col_headers,Y_test)
