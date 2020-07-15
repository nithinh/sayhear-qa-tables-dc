from DocProcessor import DocProcessor

import sys
if __name__ == '__main__':
	path = sys.argv[1]
	prs = DocProcessor()
	print prs.process_html(path)