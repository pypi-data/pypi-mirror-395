#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

# https://www.google.com.au/maps/@-33.8317302,151.1956613,15z

# https://googlemaps.github.io/google-maps-services-python/docs

import os,sys,re,logging,json,googlemaps

from Argumental.Argue import Argue
from Perdy.pretty import prettyPrint
from Spanners.Squirrel import Squirrel

args = Argue()
squirrel = Squirrel()

for name in logging.Logger.manager.loggerDict.keys():
	logging.getLogger(name).setLevel(logging.ERROR)

#____________________________________________________________
@args.command(single=True)
class GoogleMaps(object):

	@args.property(short='u', default='david.edson@gmail.com')
	def username(self): return

	def __init__(self):
		key = squirrel.get('googlemaps:%s'%self.username)
		self.gmaps = googlemaps.Client(key=key)

	@args.operation
	@args.parameter(name='name', help='name to search')
	def places(self, name):
		return self.gmaps.places(query=name)

	@args.operation
	@args.parameter(name='id', help='place id')
	def place(self, id):
		return self.gmaps.place(place_id=id)

#____________________________________________________________
if __name__ == '__main__':
	#args.parse(['places','stibo systems australia'])
	results = args.execute()
	if results:
		print(json.dumps(results, indent=4))

