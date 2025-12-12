#!/usr/bin/env python3

import os, re, sys, requests, hashlib, shutil, io, urllib3, logging, arrow

from urllib.parse import quote_plus, urlparse
from bs4 import BeautifulSoup as BS

from Baubles.Logger import Logger

logger = Logger()
logger.setLevel(logging.INFO)

others = [
	'boto3.resources.action',
	'boto3.resources.factory',
	'botocore.auth',
	'botocore.client',
	'botocore.configprovider',
	'botocore.credentials',
	'botocore.endpoint',
	'botocore.hooks',
	'botocore.httpsession',
	'botocore.loaders',
	'botocore.loaders',
	'botocore.parsers',
	'botocore.region',
	'botocore.regions',
	'botocore.retryhandler',
	'botocore.utils',
]

for other in others:
	logging.getLogger(other).setLevel(logging.WARNING)

# todo: https://stackoverflow.com/questions/22894211/how-to-resume-file-download-in-python

#_____________________________________________________________________________
class Downloader(object):
	'''
	cached download manager
	'''

	def __init__(self, cacheDir='.cache', fresh=False, resumable=False):
		#urllib3.disable_warnings()
		self.cacheDir = cacheDir
		self.fresh = fresh
		self.resumable = resumable
		logger.debug('cacheDir='+self.cacheDir)


	def download(self, url, file=None, username=None, password=None):
		'''
		read from disk before downloading
		'''
		logger.debug('url='+url)

		if not file:
			parts = urlparse(url)

			query = ''
			if len(parts.query):
				logger.debug('query=%s'%parts.query)
				md = hashlib.md5()
				md.update(quote_plus(parts.query).encode('utf8'))
				query = '.%s'%md.hexdigest()

			# fake file for dir like path
			paths = parts.path.split('/')
			if '.' not in paths[-1]:
				paths.append('.html')

			file = '%s/%s%s%s'%(
				self.cacheDir,
				parts.netloc,
				'/'.join(paths),
				query
			)

		logger.debug('file='+file)

		dirName = os.path.dirname(file)
		if dirName and not os.path.isdir(dirName):
			os.makedirs(dirName)

		data = None

		resume_byte_pos = 0
		if self.resumable and os.path.isfile(file):
			stat = os.stat(file)
			resume_byte_pos=stat.st_size #+1 ?
			logger.info('resume_byte_pos=%d'%resume_byte_pos)

		if self.fresh or self.resumable or not os.path.isfile(file):
			logger.info('to cache '+file)
			if username and password:
				auth=(username,password)
			else:
				auth=None

			resume_header = { 'Range': 'bytes=%d-' % resume_byte_pos}

			response = requests.get(url, verify=True, headers=resume_header, stream=True, auth=auth, allow_redirects=True)
			if not ('%d'%response.status_code).startswith('2'):
				file = '%s=%s'%(file,response.status_code)
				logger.warning('url=%s, code=%s'%(url, response.status_code))
			with open(file,'ab') as output:
				response.raw.decode_content = True
				#output.write(response.raw.read())
				shutil.copyfileobj(response.raw, output)

		else:
			logger.info('from cache '+file)

		with open(file, 'rb') as input:
			data = io.BytesIO(input.read())

		return data.getvalue()


#_____________________________________________________________________________
def main():
	downloader = Downloader(fresh=False, resumable=True)
	#now = arrow.now()
	if len(sys.argv) == 1:
		sys.stderr.write('usage: [<url>*]\n')
	else:
		for file in sys.argv[1:]:
			html = downloader.download(sys.argv[1])



#_____________________________________________________________________________
if __name__ == '__main__': main()

