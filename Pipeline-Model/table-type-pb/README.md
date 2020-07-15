# Table type problem

Objective: Find out id the table is entity-instance (type 1) or key-value (type 2).

## Featurizing 

Run :
```shell
python feature_eng_table_type.py train
python feature_eng_table_type.py test
```

It will output a `train.csv` and a `test.csv` files that can then be used for ML.

## Features
The csv contains:
* id of example
* table type

+ features:

1.	Number of culumns
2.	Number of columns when ignoring link columns
3.	"key" or "property" in colmun header
4.	Variation of centent length (normalized): is the length of the content of each cell in one column similar? averaged over the number of columns. If 0, all cells from each columns have the same lenght (number of words).
5.	Varation of presence of digits (normalized): Do the cells in one column all countain digits or not? If 0: of each column, none of the cells _or_ all the cells contain digits. The higher the score is, the more random the presence of digits in cells from the same column is.


## Stats

### Train set:

	136 type 1 tables
	102 type 2 tables

	Average number of columns for type 1 tables:6.33
	Average number of columns for type 2 tables:2.70

	When ignoring link columns: average number of columns for type 1 tables:4.66
	When ignoring link columns: average number of columns for type 2 tables:2.13

	2 type 1 tables with "key" in column header
	98 type 2 tables  with "key" in column header

	Average variation in content length for type 1 tables:0.0841
	Average variation in content length for type 2 tables:0.2036

	Average variation in presence of digits for type 1 tables:0.0729
	Average variation in presence of digits for type 2 tables:0.2788

### Test set

	38 type 1 tables
	26 type 2 tables

	Average number of columns for type 1 tables:6.24
	Average number of columns for type 2 tables:2.73

	When ignoring link columns: average number of columns for type 1 tables:4.97
	When ignoring link columns: average number of columns for type 2 tables:2.00

	0 type 1 tables with "key" in column header
	26 type 2 tables  with "key" in column header

	Average variation in content length for type 1 tables:0.1004
	Average variation in content length for type 2 tables:0.1752

	Average variation in presence of digits for type 1 tables:0.0899
	Average variation in presence of digits for type 2 tables:0.2287


## Finding table type

Run:
```shell
python table_type.py train.csv test.csv
```

## Results on table type problem

	Logistic regression:
	Error on training set:0.021097
	Error on test set:0.000000

	Logistic regression when ignoring column header:
	Error on training set:0.118143
	Error on test set:0.238095

	Ad hoc classification:
	Error on train set:0.025316
	Error on test set:0.000000

	Decision tree classification:
	Error on train set:0.016878
	Error on train set:0.000000

	Decision tree classification when ignoring column header:
	Error on train set:0.071730
	Error on train set:0.190476

	KNN classification:
	Error on train set:0.016878
	Error on train set:0.000000

	KNN classification when ignoring column header:
	Error on train set:0.075949
	Error on train set:0.190476