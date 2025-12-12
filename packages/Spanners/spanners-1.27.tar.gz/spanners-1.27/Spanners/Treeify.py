#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import io, sys, os, json, xmltodict, yaml

from collections import OrderedDict as OD
from collections import deque
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_LIGHT, BOX_BLANK
from io import StringIO, IOBase

from Baubles.Colours import Colours
from Perdy.pretty import prettyPrintLn, Style
from Perdy.parser import doParse
from Argumental.Argue import Argue

args = Argue()

@args.command(single=True)
class Treeify(object):

	@args.property(short='c', flag=True, help='output in colour')
	def colour(self): return False


	@args.property(short='a', flag=True, help='ascii instead of boxes')
	def ascii(self): return False


	_oneof = OD([(x, 'input as %s' % x) for x in ['json', 'xml', 'yaml']])


	@args.property(oneof=_oneof, short=True, flag=True, default=list(_oneof.keys())[0])
	def format(self): return


	def __init__(self, colour=False, ascii=False):
		if colour: self.colour = True
		if ascii: self.ascii = True
		self.fundamentals = [str, str, int, float, bool]
		self.collections = [list, dict, OD]
		self.colours = Colours(colour=self.colour)


	def treeFix(self, node):
		if not node:
			return dict()
		if type(node) in self.fundamentals:
			return {''.join([self.colours.Purple, str(node), self.colours.Off]): dict()}
		if type(node) is list:
			new = OD()
			for n in range(len(node)):
				key = ''.join(['[', self.colours.Teal, str(n), self.colours.Off,']'])
				new[key] = self.treeFix(node[n])
			return new
		if type(node) in [dict, OD]:
			for key in list(node.keys()):
				tipe = type(node[key])
				value = self.treeFix(node[key])
				del node[key]
				if len(key) and key[0] in ['@', '#']:
					node[''.join([self.colours.Green, key, self.colours.Off])] = value
				else:
					if tipe in self.fundamentals:
						parts = [self.colours.Green]
					else:
						parts = [self.colours.Teal]
					parts += [key, self.colours.Off]
					if self.format == 'xml':
						parts = ['<'] + parts + ['>']
					node[''.join(parts)] = value
		return node


	def process(self, input, output=sys.stdout):
		if type(input) in self.collections:
			o = input
		elif isinstance(input, IOBase) or isinstance(input, StringIO):
			input = input.read()
		if type(input) in [str]:
			if self.format == 'xml':
				o = xmltodict.parse(input)
			elif self.format == 'yaml':
				o = yaml.safe_load(input)
			else: # == 'json'
				o = json.loads(input)
		if self.ascii:
			tr = LeftAligned()
		else:
			tr = LeftAligned(draw=BoxStyle(
				label_space=0,
				gfx=BOX_LIGHT,
				horiz_len=1
			))

		output.write(tr(self.treeFix(o)))


	@args.operation
	@args.parameter(name='files', short='f', nargs='*', metavar='file')
	@args.parameter(name='output', short='o')
	def bark(self, files=[], output=None):
		_output = sys.stdout
		if output:
			_output = open(output(), 'w')
		if len(files) == 0:
			self.process(sys.stdin, _output)
		else:
			for file in files:
				with open(file) as _input:
					self.process(_input, _output)
		if output:
			_output.close()
		return


	@args.operation
	def test(self):

		h = '\n' + '_' * 47

		j = {
			'one': {
				'one_one': {
					'one_one': [{
						'#text': '_1_1_1'
					}, {
						'#text': '_1_1_2'
					}]
				},
				'one_two': {
					'@attr': '_1_2',
					'#text': '_1_2_1'
				}
			}
		}

		j['one']['two'] = list(set(['x', 1, True]))

		print(h)
		prettyPrintLn(j)
		print(h)

		f = '../test/treeify.json'
		with open(f,'w') as output:
			json.dump(j, output)
		self.bark([f])
		print(h)

		#self.ascii = True
		self.colour = True
		self.process(StringIO(json.dumps(j)), sys.stdout)
		print(h)

		x = xmltodict.unparse(j)
		doParse(StringIO(str(x)), sys.stdout, colour=True)
		print(h)
		self.format = 'xml'
		self.process(StringIO(str(x)), sys.stdout)
		print(h)

		sio = StringIO()
		prettyPrintLn(j, output=sio, style=Style.YAML, colour=False)
		y = sio.getvalue()
		sio.close()
		#print y
		y = y.replace('#text', '"#text"')
		y = y.replace('@attr', '"@attr"')
		#print y
		prettyPrintLn(j, output=sys.stdout, style=Style.YAML, colour=True)
		print(h)
		self.format = 'yaml'
		self.process(StringIO(y), sys.stdout)

		return


if __name__ == '__main__': args.execute()



