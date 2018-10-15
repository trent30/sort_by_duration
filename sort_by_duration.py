#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from stat import *
import subprocess
import mimetypes
import copy
from optparse import OptionParser

if subprocess.Popen("which mediainfo".split()).wait() != 0:
	print("You have to install mediainfo")
	exit(0)
	
sorted_path = "/sort_by_duration/"
cmd = 'mediainfo --Inform="Video;%Duration%___%Duration/String5%___" '
current_path = os.environ['PWD'] + "/"
output_path  = current_path + sorted_path
mimetypes.init()

try:
	os.mkdir(output_path)
except:
	sys.stderr.write("Directory %s already exist\n" % output_path)

def AccessError( filename ):
	sys.stderr.write("Can't acces to file %s\n" % filename)

def ldir( path, rec=True, ret=[] ):
	try:
		os.listdir(path)
	except:
		AccessError(path)
	else:
		for f in os.listdir(path):
			if path[-1] == "/":
				ff = path + f
			else:
				ff = path + "/" + f
			try :
				mode = os.lstat(ff).st_mode
			except:
				AccessError(ff)
			else:
				if S_ISDIR( mode ):
					if rec:
						if os.path.basename(ff) != sorted_path.replace("/", ""):
							ret = ldir(ff + "/" )
				else:
					file_type = mimetypes.guess_type( ff )[0]
					if file_type is not None:
						if 'video' in file_type:
							ret.append( ff )
	return ret

def new_filename(old_name, duration):
	SEP = "___"
	ms = duration.split(SEP)[0].rjust(10, '0')
	if "." in ms:
		ms = ms.split(".")[0].rjust(10, '0')
	dur = duration.split(SEP)[1].split(' ')[1]
	return ms + SEP + dur + SEP + os.path.basename(old_name)

def get_links(path):
	ret = []
	for f in os.listdir(path):
		ff = output_path + "/" + f
		try :
			mode = os.lstat(ff).st_mode
		except:
			AccessError(ff)
		else:
			if S_ISLNK( mode ):
				ret.append( os.readlink(ff) )
	return ret

if __name__ == "__main__":
	
	parser = OptionParser()
	parser.add_option("-R", "--no-recursion", default=0, action="store_const", const=1, dest="REC", help="Read only current path, disable recursion.")
	(options, args) = parser.parse_args()
	
	if options.REC == 0:
		rec=True
	else:
		rec=False
	
	FILES = ldir( current_path, rec )
	LINKS = get_links( output_path )
	
	for i in FILES:
		if i not in LINKS:
			print i
			duration = os.popen(cmd + '"' + i + '"').read()
			if duration != '______\n' and duration != '\n':
				os.symlink(i, output_path + new_filename(i, duration))
		else:
			print "ALREADY DONE", i
