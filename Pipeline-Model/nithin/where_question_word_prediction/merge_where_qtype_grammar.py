import pandas as pd
import sys
import argparse


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-a", "--csv1", required=True,
		help="path for csv file 1 ")
	ap.add_argument("-b", "--csv2", required=True,
		help="path for csv file 1 ")

	ap.add_argument("-o", "--output", required=True,
		help="path for output csv")
	args = vars(ap.parse_args())


	a = pd.read_csv(args["csv1"])
	b = pd.read_csv(args["csv2"])
	merged=a.merge(b, left_on=['q_id','w_id'], right_on = ['id question','word index'],
                 how='left', suffixes=('_x', ''))
	col_to_drop = ["NUM","HUM_x","ENTY_x","LOC_x","ABBR_x","SQ_x","DESC_x","PERSON_x","LOCATION_x","DATETIME_x","QUANTITY_x","ORGANISATION_x","NONE_x","ADV_x","VERB_x","DET_x","ADJ_x","PROPN_x","ADP_x","PART_x","NOUN_x","NUM.1","PRON_x","INTJ_x","CCONJ_x","acl_x","advcl_x","advmod_x","amod_x","appos_x","aux_x","case_x","cc_x","ccomp_x","clf_x","compound_x","conj_x","cop_x","csubj_x","dep_x","det_x","discourse_x","dislocated_x","expl_x","fixed_x","flat_x","goeswith_x","iobj_x","list_x","mark_x","nmod_x","nsubj_x","nummod_x","obj_x","obl_x","orphan_x","parataxis_x","punct_x","reparandum_x","root_x","vocative_x","xcomp_x","id question","date","count","period","money","word","word index","is_stop"]
	merged = merged.drop(col_to_drop,axis=1)
	merged.to_csv(args["output"],index=None)

