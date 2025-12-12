#!/usr/bin/env python3

import os,re,sys

from time import sleep
from functools import wraps

#_________________________________________________
def getRoot(fn):
	#print 'fn=', fn, ', name=', fn.__name__
	while hasattr(fn,'func_closure') and fn.func_closure:
		#print 'fn.func_closure=', fn.func_closure
		if len(fn.func_closure) == 0:
			break
		fn = fn.func_closure[0].cell_contents
	return fn

#_________________________________________________
class Executor(object):
	'''
	execution helpers:
	executor = Executor()
	'''

	def retry(self, *oargs, **okwargs):
		'''
		retry the enclosed function:

		@executor.retry(timeout=5, retries=3)
		def fnToRetry():
			raise Exception('fail')
		'''

		#print(oargs,okwargs)

		def _wrapit(fn):
			fn = getRoot(fn)

			@wraps(fn)
			def _wrapper(*args, **kwargs):

				timeout = okwargs.get('timeout', 5)
				retries = okwargs.get('retries', 3)
				#print(f'{timeout=} {retries=}')

				# execution
				while retries > 0:
					try:
						return fn(*args,**kwargs)
						break
					except:
						sys.stderr.write(f'{retries}: {sys.exc_info()[0]}\n')
						retries -= 1
						sleep(timeout)

			return _wrapper

		def _actualWrapper(fn): return _wrapit(fn)

		return _actualWrapper

def main():
	executor = Executor()

	@executor.retry(timeout=1) #, retries=2)
	def awooga():
		print('try')
		raise Exception('fail')

	awooga()

	return

if __name__ == '__main__': main()
