#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, sys, re, json, xmltodict

from Argumental.Argue import Argue

if os.path.dirname(sys.argv[0]) == '.':
	sys.path.insert(0, '..')

from Spanners.Squirrel import Squirrel

args = Argue()


@args.command(single=True)
class SquirrelCommand(Squirrel):

	@args.attribute(short='v', flag=True)
	def verbose(self): return False

	def __init__(self):
		super().__init__()
		return

	@args.operation
	def get(self, name):
		'''
		get a KMS key

		'''
		return super().get(name)  #.rstrip('\r').rstrip('\n')

	@args.operation
	@args.parameter(name='replace', short='r', flag=True)
	def put(self, name, value, replace=False):
		'''
		put a KMS name,value key

		'''
		if replace: super().delete(name)
		return super().put(name, value)

	@args.operation
	def delete(self, name):
		'''
		delete a KMS name
		'''
		return super().delete(name)

	@args.operation
	def list(self):
		'''
		list the KMS names

		'''
		return list(super().list())


if __name__ == '__main__':
	result = args.execute()
	if result:
		if type(result) == list:
			print('\n'.join(result))
		else:
			print(result)

