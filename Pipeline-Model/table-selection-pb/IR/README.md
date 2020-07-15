## Installation for pre-processing

Install python3. 
On Mac, I ran,

```shell
brew install python3
```

Just run the instructions in the install script install.sh. Or run it directly
```shell
sh install.sh
```

The `tf_idf.py` script takes the pickle scripts generated in the pre-processing step to generate accuracy information based on
1) Cosine similarity
2) Dot product
3) Euclidean distance

The optional csv file gives the rank values of the original table from the computation.

```
usage: tf_idf.py [-h] -tr TRAIN_TABLES -qtr TRAIN_QUESTION [-te TEST_TABLES]
                 [-qte TEST_QUESTION] [-o OUT]

Generates accuracy information based tf-idf vectors and their cosine
similarity

optional arguments:
  -h, --help            show this help message and exit
  -tr TRAIN_TABLES, --train_tables TRAIN_TABLES
                        path for the data in the training set tables in the
                        pickle format
  -qtr TRAIN_QUESTION, --train_question TRAIN_QUESTION
                        path for data in the training set questions in the
                        pickle format
  -te TEST_TABLES, --test_tables TEST_TABLES
                        path for the data in the tables in the pickle format
  -qte TEST_QUESTION, --test_question TEST_QUESTION
                        path for data in the questions in the pickle format
  -o OUT, --out OUT     path for output csv file
  -res RESULTS, --results RESULTS
                        path for output json file with results
```

The csv `out` file will contain, for each example and for each method (cosine similarity, dot product, euclidian distance) the rank of the correct page.

The json `results` file will contain, for each example and for each method, the first ten pages (index of example). Once all the elements of the system are working, this file should be use to decide on which page to execute a SQL query.

For example:  
```shell
python3 tf_idf.py -tr ../../data/preprocess/preprocessed_train_table_list.pkl -qtr ../../data/preprocess/preprocessed_train_question_list.pkl -te ../../data/preprocess/preprocessed_test_table_list.pkl -qte ../../data/preprocess/preprocessed_test_question_list.pkl -o out.csv -res results.json
```