#!/usr/bin/env python3

import errno, json

class Errors(object):

	def __init__(self):
		return

	def __str__(self):
		return json.dumps(errno.errorcode,indent=4)

def main():
	errors = Errors()
	print errors
	return

if __name__ == '__main__': main()
