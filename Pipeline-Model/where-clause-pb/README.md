# How to run generate_average_cell_length.py

The 1st argument: transposed table directory (e.g. data/tables/train/transposed_csvs/)

The 2nd argument: output file (3 columns, "question id","col header","average_cell_length")

## Example:

(1) python generate_average_cell_length.py data/tables/train/transposed_csvs/ average_cell_length_feature_train.csv

(2) python generate_average_cell_length.py data/tables/test/transposed_csvs/ average_cell_length_feature_test.csv



# How to run generate_edit_distance_col_content_to_qword.py

The 1st argument: transposed table directory (e.g. data/tables/train/transposed_csvs/)

The 2nd argument: the preprocessed question list in pickle file

The 3rd argument: first question's id (0 for train dataset, 238 for test dataset)

The 4th argument: output file (3 columns, "question id","col header","min_edit_distance_col_content_to_qword")

## Example:

(1) python generate_edit_distance_col_content_to_qword.py data/tables/train/transposed_csvs/ preprocessed_train_question_list.pkl 0 edit_distance_feature_train.csv

(2) python generate_edit_distance_col_content_to_qword.py data/tables/test/transposed_csvs/ preprocessed_test_question_list.pkl 238 edit_distance_feature_test.csv



# How to run WHERE_mlp.py

The 1st argument: train feature file name

The 2nd argument: test feature file name

The 3rd argument: number of epochs to run

The 4th argument: result file name

## Example:

python WHERE_mlp.py WHERE_train_features.csv WHERE_test_features.csv 1000 result.csv
