# Preprocessing: getting bag of words 

These scripts are used tp process the tables, questions and html into bag-of-words files in the <a href="https://docs.python.org/3/library/pickle.html">pickle</a> format.

The preprocessing steps include:

* Stopwords removal
* Stemming
* Convert into a bag of words structure

Those bag of words are used in particular for solve the [source-select problem with the information retrieval approach](https://github.com/CMU-RERC-APT/sayhear-fall2018/tree/master/source-select/IR).


## Installation for pre-processing

Install python3.
On Mac, I ran,
```shell
brew install python3
```
Just run the instructions in the install script install.sh or run it directly
```shell
sh install.sh
```

Unzip `sayhearfall2018_train.zip` and `sayhearfall2018_test.zip`.

## Preprocessing tables

Usage:
```shell
table_preprocess.py [-h] -j JSON -d DATA -o OUT
```

Optional arguments:
```
-h, --help            show this help message and exit
-j JSON, --json JSON  path for json data to parse
-d DATA, --data DATA  path for data directory that contains directories
                      containing table.csv
-o OUT, --out OUT     path for output pkl file
```

For example, from this directory:

```shell
python3 table_preprocess.py -j ../sayhearfall2018_train.json -d ../sayhearfall2018_train/ --out preprocessed_train_table_list.pkl
python3 table_preprocess.py -j ../sayhearfall2018_test.json -d ../sayhearfall2018_test/ --out preprocessed_test_table_list.pkl
```

## Preprocessing questions

Usage:
```
question_preprocess.py [-h] -j JSON -o OUT
```

Optional arguments:
```
-h, --help            show this help message and exit
-j JSON, --json JSON  path for json data to parse
-o OUT, --out OUT     path for output pkl file
```

For example, from this directory:
```
python3 question_preprocess.py --json ../sayhearfall2018_train.json --out preprocessed_train_question_list.pkl
python3 question_preprocess.py --json ../sayhearfall2018_test.json --out preprocessed_test_question_list.pkl
```

## Preprocessing html pages

Usage: 
```
html_preprocess.py [-h] -j JSON -d DATA -o OUT
```

Optional arguments:
```
-h, --help            show this help message and exit
-j JSON, --json JSON  path for json data to parse
-d DATA, --data DATA  path for data directory that contains directories
                      containing html.txt file or *_domxml.txt
-o OUT, --out OUT     path for output pkl file
```

For example, from this directory:
```
python3 html_preprocess.py -j ../sayhearfall2018_train.json -d ../sayhearfall2018_train/ --out preprocessed_train_html_list.pkl
python3 html_preprocess.py -j ../sayhearfall2018_test.json -d ../sayhearfall2018_test/ --out preprocessed_test_html_list.pkl
```

