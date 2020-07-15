import sys
sys.path.insert(0, '../select-clause-pb/features/nb-of-col-and-word-vectors-features/tools/')
# import tools
# import helper_functions as helper
import proximity_fct as pfct
sys.path.insert(0, '../data/transpose-tables/')
# import sql_tables as sql
# import check_all_dataset as check
import verified_dataset_stats as stats

word2vec = pfct.load_model("../select-clause-pb/features/nb-of-col-and-word-vectors-features/GoogleNews-vectors-negative300.bin")

stats.main('test',word2vec)

