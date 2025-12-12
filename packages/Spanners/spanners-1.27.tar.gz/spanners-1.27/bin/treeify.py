#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import io, sys, os, json, xmltodict, yaml

from collections import OrderedDict as OD
from collections import deque
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_LIGHT, BOX_BLANK
from io import StringIO

from Baubles.Colours import Colours
from Perdy.pretty import prettyPrintLn, Style
from Perdy.parser import doParse
from Argumental.Argue import Argue

args = Argue()

_colour = False


@args.argument(short='c', flag=True, help='output in colour')
def colour():
	return _colour


_ascii = False


@args.argument(short='a', flag=True, help='ascii instead of boxes')
def ascii():
	return _ascii


_oneof = dict([(x, 'input as %s' % x) for x in ['xml', 'json', 'yaml']])
_format = 'json'


@args.argument(oneof=_oneof, short=True, flag=True, default=_format)
def format():
	return _format


@args.argument(positional=True, nargs='*', metavar='file')
def files():
	return []


@args.argument(short='o')
def output():
	return


@args.argument(name='test', short='T', flag=True, help='run the test harness')
def doTest():
	return False


args.parse()

fundamentals = [str, str, int, float, bool]
colours = Colours(colour=colour())


def treeFix(node):
	if not node:
		return dict()
	if type(node) in fundamentals:
		return {''.join([colours.Purple, str(node), colours.Off]): dict()}
	if type(node) is list:
		new = OD()
		for n in range(len(node)):
			new[''.join([colours.Teal, str(n), colours.Off])] = treeFix(node[n])
		return new
	if type(node) in [dict, OD]:
		for key in list(node.keys()):
			tipe = type(node[key])
			value = treeFix(node[key])
			del node[key]
			if key[0] in ['@', '#']:
				node[''.join([colours.Green, key, colours.Off])] = value
			else:
				if tipe in fundamentals:
					parts = [colours.Green]
				else:
					parts = [colours.Teal]
				parts += [key, colours.Off]
				if format() == 'xml':
					parts = ['<'] + parts + ['>']
				node[''.join(parts)] = value
	return node


def process(input, output):
	if format() == 'xml':
		o = xmltodict.parse(input.read())
	elif format() == 'yaml':
		o = yaml.load(input)
	else:
		o = json.load(input)

	if ascii():
		tr = LeftAligned()
	else:
		tr = LeftAligned(draw=BoxStyle(gfx=BOX_LIGHT, horiz_len=1))

	output.write(tr(treeFix(o)))


def main():
	_output = sys.stdout
	if output():
		_output = open(output(), 'w')
	if len(files()) == 0:
		process(sys.stdin, _output)
	else:
		for file in files():
			with open(file) as _input:
				process(_input, _output)
	if output():
		_output.close()
	return


def test():
	global _colour
	global _format
	global _ascii

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
	print(h)
	prettyPrintLn(j)
	print(h)

	#_ascii=True
	_colour = True
	process(StringIO(json.dumps(j)), sys.stdout)
	print(h)

	x = xmltodict.unparse(j)
	doParse(StringIO(str(x)), sys.stdout, colour=True)
	print(h)
	_format = 'xml'
	process(StringIO(str(x)), sys.stdout)
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
	_format = 'yaml'
	process(StringIO(y), sys.stdout)

	return


if __name__ == '__main__':
	if doTest():
		test()
	else:
		main()


