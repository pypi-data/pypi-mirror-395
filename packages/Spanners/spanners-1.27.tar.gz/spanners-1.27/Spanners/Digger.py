#!/usr/bin/env python3

import os, re, sys, xmltodict, pandas
from collections import deque, OrderedDict

class Digger:
	'''
	utility to recurse down into a parsed dataframe
	'''

	def __init__(self, dq=None, file=None, stack=None):
		'''
		class object used to create isolation between levels
		and copies the dataframe into a reduced set to remove global sharing issues
		'''

		if file:
			self.dq = pandas.read_excel(file)
			self.opml = OrderedDict([
				('opml', OrderedDict([
					('@version', '1.0'),
					('head', OrderedDict([
						('title', file),
						('expansionState', '0'),
					])),
					('body', OrderedDict([
					]))
				]))
			])
			self.stack = [ self.opml['opml']['body'] ]

		else:
			self.dq = dq.copy()
			self.stack = stack

	def pushd(self, value):
		self.putd(value)
		self.stack.append(
			self.stack[-1]['outline'][-1]
		)

	def putd(self, value):
		if 'outline' not in self.stack[-1].keys():
			self.stack[-1]['outline'] = []
		self.stack[-1]['outline'].append({
			'@text': value,
		})

	def popd(self):
		self.stack.pop()

	def dig(self, indent=''):
		columns = deque(self.dq.columns)
		if len(columns) == 0: return
		column = columns.popleft()

		for value in self.dq[column].unique():
			print(f'{indent}{value}')

			self.pushd(value)

			dqq = self.dq[self.dq[column] == value][columns]
			Digger(dq=dqq, stack=self.stack).dig(indent=f'\t{indent}')

			self.popd()

	def save(self, file):
		with open(file,'w') as output:
			print(f'\n{file}')
			xmltodict.unparse(self.opml, output, encoding='UTF8', pretty=True)


