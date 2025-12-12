#!/usr/bin/env python3

import os,re,sys

_region = 'ap-southeast-2'
def region():
	'''
	the AWS credstash region
	'''
	return _region

_table = 'credential-store'
def table():
	'''
	the AWS DynamoDB credstash table name
	'''
	return _table

#________________________________________________________________________________________
class SquirrelBase(object):
	'''
	place holder to be substitided with the most efficient credstash implememtation available
	'''

	def __init__(self):
		pass

	def get(self,name):
		raise NotImplementedError()

	def put(self,name,value):
		raise NotImplementedError()

	def delete(self,name):
		raise NotImplementedError()

	def list(self):
		raise NotImplementedError()

Squirrel = SquirrelBase

try:

	#____________________________________________________________________________________
	import keychain, dialogs

	class KeyChainSquirrel(SquirrelBase):
		'''
		pythonista usage of the credstash API
		'''

		def __init__(self):
			super(KeyChainSquirrel,self).__init__()

		def get(self,name):
			value = keychain.get_password(
				table(),
				name
			)
			if not value:
				value = dialogs.text_dialog('%s ?'%name)
				self.put(name,value)
			return value

		def put(self,name,value):
			keychain.set_password(
				table(),
				name,
				value
			)

		def delete(self,name):
			keychain.delete_password(
				table(),
				name
			)
			return

		def list(self):
			return list()

	Squirrel = KeyChainSquirrel

except:

	try:
		#________________________________________________________________________________
		import credstash
		from credstash import ItemNotFound

		class SecretSquirrel(SquirrelBase):
			'''
			class to demonstrate the usage of the credstash API
			'''

			def __init__(self):
				super(SecretSquirrel,self).__init__()

			def get(self,name):
				try:
					value = credstash.getSecret(
						name,
						region=region(),
						table=table()
					)
					return value
				except ItemNotFound:
					sys.stderr.write('cant find credstash value for key "%s"\n'%name)
					sys.exit(1)

			def put(self,name,value):
				return credstash.putSecret(
					name,value,
					region=region(),
					table=table()
				)

			def delete(self,name):
				return credstash.deleteSecrets(
					name,
					region=region(),
					table=table()
				)

			def list(self):
				values = credstash.listSecrets(
					region=region(),
					table=table()
				)
				return map(lambda x:x['name'], values)

		Squirrel = SecretSquirrel

	except:
		#________________________________________________________________________________
		from subprocess import Popen, PIPE

		class SecretAgent(SquirrelBase):

			def __init__(self):
				super(SecretAgent,self).__init__()

			def execute(self,command):
				process = Popen('credstash --table %s --region=%s %s'%(table(), region(), command),shell=True,stdout=PIPE)
				results = process.stdout.readlines()
				del process
				results = map(lambda x: x.rstrip('\r').rstrip('\n'), results)
				return results

			def setup(self):
				return '\n'.join(self.execute('setup'))

			def get(self,name):
				value = '\n'.join(self.execute('get \'%s\''%name))
				return value

			def put(self,name,value):
				return '\n'.join(self.execute('put \'%s\' \'%s\''%(name,value)))

			def delete(self,name):
				return '\n'.join(self.execute('delete \'%s\''%name))

			def list(self):
				p = re.compile('^(.*\S)\s+--\sversion\s\d+$')
				items = []
				for item in self.execute('list'):
					m = p.match(item)
					if m:
						items.append(m.group(1))
				return items

		Squirrel = SecretAgent

