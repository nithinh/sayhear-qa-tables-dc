import pandas as pd
import sys


if __name__ == '__main__':

	file1 = sys.argv[1]
	file2 = sys.argv[2]
	out = sys.argv[3]

	q_type = pd.read_csv(file1,encoding="latin-1")
	result = pd.read_csv(file2,encoding="latin-1")

	merged = pd.merge(q_type,result,how="left",on="q_id")

	merged.to_csv(out,encoding="utf-8")