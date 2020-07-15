# Manually checking the dataset

Objective: Check that all SQL queries execute and return the expected answer.

General idea: 
1) The script checks that all previously validated examples still execute. This allows to safely change the code of the ~ operator and always make sure these changes do not affect those examples.
2) For each not-yet-validated example, the script tries to execute the SQL query with the current implementation of the ~ operator. It then asks the user to check whether the retrieved answer corresponds to the expected answer. If not, the user is given the opportunity to add a note. All those verifications / notes are automatically saved. 
3) If the user quits after checking example # i, the next one she will the presented with will be example # i+1 nest time she runs the script.

## Usage

Run in a python interpreter:
```python
import sys
sys.path.insert(0, '../select-clause-pb/features/nb-of-col-and-word-vectors-features/tools/')
# import tools
# import my_tokenize as tk
# import helper_functions as helper
# import proximity_fct as pfct
sys.path.insert(0, '../data/transpose-tables/')
# import sql_tables as sql
import check_all_dataset as check

word2vec = pfct.load_model("../select-clause-pb/features/nb-of-col-and-word-vectors-features/GoogleNews-vectors-negative300.bin")

check.main('train',word2vec)
```
## ~ operator

As of Monday, October 22 4pm, this is the list of the strategies the ~ operator using. The strategies are applied in this order. If one is not working, we try the next one. 

For reference, this is what the query looks like: `SELECT "column1" FROM "table1" WHERE "column2" ~ "key_word"`.

1) replace `~` operator with `=`.
2) replace `~` with `LIKE`, imposing:
	* `key_word` is the 1st word of the cell OR
	* `key_word` is the last word of the cell OR
	* `key_word` is preceded and followed by a space.
3) replace `~` with `LIKE "%key_word%`; i.e. key_word can be preceeded and followed by any other character(s)/word(s).
4) replace `key_word` with the content of the cell that is the most similar to `key_word`. How get the most similar cell: 
	* We get the vector `v1` for `key_word` from pre-trained word2vec (or the average of the vectors of the words in `key_word`, if `key_word` has several words), as well as the (average) vector `v2` for the word(s) in a cell and get the cosine similarity score of `v1` ans `v2`.
	* We compute this score for each cell of `column2` and return the cell that has the highest similarity.

## Verified examples

Statistics computed with the `verified_dataset_stats.py` dataset. Usage (python interpreter):
```python
import sys
sys.path.insert(0, '../select-clause-pb/features/nb-of-col-and-word-vectors-features/tools/')
# import tools
# import helper_functions as helper
# import proximity_fct as pfct
sys.path.insert(0, '../data/transpose-tables/')
# import sql_tables as sql
# import check_all_dataset as check
import verified_dataset_stats as stats

word2vec = pfct.load_model("../select-clause-pb/features/nb-of-col-and-word-vectors-features/GoogleNews-vectors-negative300.bin")

stats.main('train',word2vec)
```

The script will output error messages while running: it's OK, don't pay attention to them. It might also stop at some point with an error message and ask you if you want to continue, just answer `y`, then `n` to `Do you want to add a note to this example? (y/n)`.

See [stats.md](https://github.com/CMU-RERC-APT/sayhear-fall2018/blob/lucile/projection/verifiry_dataset/stats.md) for the stats. Sum up:

### Train set

	STATS:

	238 examples have been verified:
	191 (80.25%) are valid (working),
	47 (19.75%) are not.

	If we use only word vector similarities (strategy 4) and none of the other heuristics we usually apply bfore using similarity scores:
	238 examples have been verified:
	182 (76.47%) are valid (working),
	56 (23.53%) are not.

### Test set

	STATS:

	64 examples have been verified:
	47 (73.44%) are valid (working),
	17 (26.56%) are not.

	If we use only word vector similarities (strategy 4) and none of the other heuristics we usually apply bfore using similarity scores:
	64 examples have been verified:
	46 (71.88%) are valid (working),
	18 (28.12%) are not.

## Modifications I made to the SQL so that the queries work and other notes...

See [modifications.md](https://github.com/CMU-RERC-APT/sayhear-fall2018/blob/lucile/projection/verifiry_dataset/modifications.md).

