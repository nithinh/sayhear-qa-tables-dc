
# Dataset

The dataset is splitted into a train set of 238 examples and a test set of 64 examples.

The json files contain a list of the examples, and for each example:

* `question_parsed` contains the NL question that has been parsed as a list of words.
* `new_sql` is SQL query (rewrote by Anthony) that has been parsed as a list of words.
* `short_a` is the short answer to the question (the expected output of the SQL query).
* `long_a` is a NL sentence that answers the NL question.
* `directory` is the name of the directory in which you'll find the csv with the table as well as some `.txt` files containing the DOM tree of the page from which the table was extracted (see below).
* `id` is a unique ID for each example.
* `table_type` is the type of the table: 1 is for entity-instance tables, 2 is for key-value tables. 
* `final_sql` is the SQL after we transposed the type 2 tables in type 1 tables.

The zip forlders contain:

* `html.txt` / `xxx_domxml.txt` <sup>(1)</sup> contains a copy of the html code on the labeled page.
* `dominfo.txt` / `xxx_dominfo.txt` <sup>(1)</sup> contains a json description of the labeled page (based on the dom tree of the page).
* `wrapper.txt` / `xxx_wrapper.txt` <sup>(1)</sup> contains json code with:
	* labeler andrew ID,
	* NL question,
	* SQL query,
	* if the page was labeled with SmartWrap, a SmartWrap table.
* `updload.txt` / `xxx.csv` <sup>(1)</sup> contains the table labeled with import.io.
* `table.csv` file. This file was generated during the preprocessing of the dataset (see [Download and preprocess, step 4](https://github.com/CMU-RERC-APT/smartwrap_v2/tree/master/data) for details). The csv file contains:
	* the name of the table (first row),
	* the column headers (second row),
	* the table.

<sup>(1)</sup>: As we kept improving SmartWrap while we built the dataset, the data is saved with different formats:
* Before approx. April 3rd 2018, we separately uploaded all the files. The name pattern was: `page_labelerAndrewID_date@time_filename.ext` (with `filename.ex` = `domxml.txt` / `dominfo.txt` / `wrapper.txt` / `.csv`)
* After approx. April 3rd 2018, we uploaded zipfiles containing all the files. The name pattern for the folder is: `page_labelerAndrewID_date@time` (where the `/` are replaced by `_` in _page_). Names of the files are: `html.txt`, `dominfo.txt`, `wrapper.txt` and `upload.txt`.

__WARNING__: One example has no `dominfo.txt` and no `html.txt` (#290).

# Test questions

`test.json` contains test questions. 

In `test.json`, you'll find a dictionary with 2 keys:
- `questions_on_tables` contains questions that have their answer in a table from our dataset. Those questions were written while looking at the table, but without knowing the turker's question. For each question, you have:
	- `folder`: the path to the folder with the table and the html code of the page is was extracted from.
	- `question_turker`: the question the turker asked that lead us to collect that table.
	- `question_lucile`: the question Lucile wrote looking only at the table.
	- `question_MSstudent`: the question one of the previous MS students wrote looking only at the table.
- `questions_on_whatever` are questions that were written by Lucile and the MS students **not** looking at any table (i.e. we don't know whether we have the answer in our dataset or not).

*Note: some of the tables that contain answers to questions in `questions_on_tables` may **NOT** be included in the dataset used this fall.*