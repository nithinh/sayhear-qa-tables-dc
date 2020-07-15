# Transpose tables

Once the tables are annotated in the main json file as type 1 (entity instance) or type 2 (key value) tables, type 2 tables can be transposed to type 1.

The scripts are (and need to be run in this order):
* Bhavya's script
* `transpose_sql.py`: tranposes the SQL queries for type 2 tables. Uses the CSVs of the _not tranposed_ tables to get the exact column name to select from the term(s) specified in the ~ operator. Some of the original queries might be ambiguous (because of the ~ operator) and cannot be automatically transposed. The `id` of those queries as well as the different possibilities regarding the column to select will be outputed in the terminal. __You will need to transpose those queries manually.__
* `preprocess_csvs.py`: the standard preprocessing that has been applied to all CSVs. Needs to be run on new CSVs. (For details see the [Smartwrap README](https://github.com/CMU-RERC-APT/smartwrap_v2/tree/master/data).)
* `preprocess_sql.py`: the standard preprocessing that has been applied to all SQL queries. Needs to be run on new queries. (For details see the [Smartwrap README](https://github.com/CMU-RERC-APT/smartwrap_v2/tree/master/data).)
* `clean_json.py`: just removes useless dictionary entries (`sql_tranpose`) for each example.

Usage is:
```shell
python transpose_sql.py path_to_json_file
python preprocess_csvs.py path_to_csv_folder
python preprocess_sql.py path_to_json_file
python clean_json.py path_to_json_file
```