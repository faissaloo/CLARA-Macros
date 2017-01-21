#!/usr/bin/env python3
# -*- coding: utf-8 -*-
############################LICENCE###################################
# Copyright (c) 2017 Faissal Bensefia
# This file is part of CLARA.
#
# Yukko is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Yukko is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Yukko.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################
import sys
import os
import re

#Regexes
includeGetRe=re.compile("\$include\[(.*?)\]")
macroGetRe=re.compile("\$([A-Za-z0-9_]+)\[([^\]]*?)\]",re.MULTILINE)
macroGetDefsRe=re.compile("\$define[\W]+([A-Za-z0-9_]+)\[(.*?)\]([^\|]+)",re.MULTILINE)
macroRmDefsRe=re.compile("\$define[\W]+[A-Za-z0-9_]+\[(.*?)\][^\|]+\|",re.MULTILINE)

#Argparse
def verifyFile(fname,flags):
	if not os.path.isfile(fname):
		print('Error: File "'+fname+'" does not exist')
		exit(2)
	if not os.access(fname,flags):
		print('Error: Permission denied for file "'+fname+'"')
		exit(1)

def verifyDir(pname,flags):
	if pname=="":
		pname="."
	
	if not os.path.isdir(pname):
		print('Error: Path "'+pname+'" does not exist')
		exit(2)
	if not os.access(pname,flags):
		print('Error: Permission denied for directory "'+pname+'"')
		exit(1)
		
#Dealing with macros
class macro():
	def __init__(self,name,argv=None,txt=None):
		self.name=name
		if macroGetRe.findall(argv):
			print("Error: Cannot nest macros")
			exit(1)
		self.argv=argv.split(",")
		self.txt=txt
	
	def expand(self):
		global macroDict
		retTxt=macroDict[self.name].txt
		for i,j in enumerate(self.argv):
			retTxt=retTxt.replace(macroDict[self.name].argv[i],j)
		return retTxt
	
	def __repr__(self):
		return "$"+self.name+"["+"".join([(j+"," if i!=len(self.argv)-1 else j) for i,j in enumerate(self.argv)])+"]"

#Creates a list of macros (as macro objects)
def getMacros(string):
	global macroGetRe
	return [macro(*i) for i in macroGetRe.findall(string)]

#Finds all macro definitions in a string and creates a
#dictionary to search for a definition by its name
def getMacroDefs(string):
	global macroGetDefsRe
	retDict={}
	for i in macroGetDefsRe.findall(string):
		retDict[i[0]]=macro(*i)
	return retDict

#Creates a list of included files (as strings)
def getIncludes(string):
	global includeGetRe
	return includeGetRe.findall(string)

#Go through the parse cycle
def process(file):
	global macroDict
	with open(file,'r') as fMain:
		content=fMain.read()
		#Include files
		includes=getIncludes(content)
		#Repeat until we no longer have includes
		while includes:
			for i in includes:
				with open(i) as fIncluded:
					content=content.replace("$include["+i+"]",fIncluded.read())
			includes=getIncludes(content)
		#Get macro definitions
		macroDict=getMacroDefs(content)
		#Remove definitions now that we know them
		content=macroRmDefsRe.sub("",content)
		#Substitute macros
		macros=getMacros(content)
		#Repeat until all macros have been expanded
		while macros:
			for i in macros:
				content=content.replace(str(i),i.expand())
			macros=getMacros(content)
		return content

if __name__=="__main__":
	outFile="/dev/stdout"
	inFile=""
	#Get rid of the executable name, we don't need it
	sys.argv.pop(0)
	#Parse arguments
	while sys.argv:
		arg=sys.argv.pop(0)
		if arg=="-h" or arg=="--help":
			print("clarac.py [options] file\n"
				"    --help  Display this information\n"
				"    -o      Output file name (default is stdout)\n")
			exit(0)
		elif arg=="-o":
			if outFile=="/dev/stdout":
				outFile=sys.argv.pop(0)
				verifyDir(os.path.dirname(outFile),os.W_OK)
			else:
				print("Error: Multiple output files specified")
				exit(7)
		elif inFile=="":
			inFile=arg
			verifyFile(inFile,os.R_OK)
		else:
			print("Error: Multiple input files specified")
			exit(7)
	
	if inFile=="":
		print("Error: No input file")
		exit(1)
	
	#Write the result
	with open(outFile,'w') as f:
		f.write(process(inFile))
