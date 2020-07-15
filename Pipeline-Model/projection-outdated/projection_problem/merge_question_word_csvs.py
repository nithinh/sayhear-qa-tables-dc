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
	merged=a.merge(b, how='left',on=['id question', 'index word from question'])
	merged.to_csv(args["output"],index=None)

