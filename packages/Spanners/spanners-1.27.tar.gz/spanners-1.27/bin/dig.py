#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, re, sys, xmltodict, pandas
from collections import deque, OrderedDict

#sys.path.insert(0,'..')

from Argumental.Argue import Argue
from Spanners.Digger import Digger

args = Argue()

@args.command(single=True)
class Normaliser:
	'''
	Tool to convert spreadsheets into outlines

	| A   | B	 | C	 |
	|:----|:------|:------|
	| one | two   | four  |
	| one | two   | five  |
	| one | three | six   |
	| one | three | seven |

	'''

	@args.operation
	@args.parameter(name='file', help='the excel file to normalise')
	def normalise(self, file):
		'''
		normalize groupd content from left to right,
		expects repeated row column values to indicate that it is from the same group as above
		the output is created renaming .xls* to .opml
		'''

		if not re.compile('.*.xlsx*').match(file):
			sys.stderr.write(f' not an excel file ? {file}\n')
			return

		opml = re.sub('.xlsx*$', '.opml', file, flags=re.IGNORECASE)

		digger = Digger(file=file)
		digger.dig()
		digger.save(opml)


	@args.operation
	@args.parameter(name='file', help='the excel file')
	def markdown(self, file):
		'''
		excel 2 markdown format
		'''

		if not re.compile('.*.xlsx*').match(file):
			sys.stderr.write(f' not an excel file ? {file}\n')
			return

		md = re.sub('.xlsx*$', '.md', file, flags=re.IGNORECASE)

		df = pandas.read_excel(file)
		df.to_markdown(md, index=False)


if __name__ == '__main__': args.execute()
