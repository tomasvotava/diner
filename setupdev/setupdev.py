#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  setupdev.py
#  
#  Copyright 2018 Tomáš Votava <info@tomasvotava.eu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#
#	Setup the environment for development purposes
#

eline = "#################################"

import os
import json
import sys

FIRST_RUN = False

VALID_VALID		= 0
VALID_NONEMPTY	= 1
VALID_NUMBER	= 2
VALID_FLOAT		= 4
VALID_LIST		= 8


PFORMAT_ATTRIBUTES = {
	"red":		"\033[91m",
	"-":		"\033[0m\033[39m\033[49m",
	"bold":		"\033[1m",
	"dim":		"\033[2m",
	"black":	"\033[30m",
	"green":	"\033[92m",
	"yellow":	"\033[93m",
	"blue":		"\033[94m",
	"magenta":	"\033[95m",
	"cyan":		"\033[96m",
	"white":	"\033[97m",
	"bblack":	"\033[40m",
	"bred":		"\033[41m",
	"bgreen":	"\033[42m",
	"bwhite":	"\033[107m",
	"normal":	"\033[0m"
}

def pformat(string):
	for att in PFORMAT_ATTRIBUTES:
		string = string.replace(":%s:"%att,PFORMAT_ATTRIBUTES[att])
	return (string+PFORMAT_ATTRIBUTES["-"])

def pprint(string):
	print(pformat(string))

def pinput(prompt):
	return input(pformat(prompt))

def get_config(prompt,default=None,validation=VALID_VALID,options=[]):
	e = VALID_VALID
	done = False
	i = ""
	while not done:
		if (e & VALID_NONEMPTY):
			pprint(":bwhite::red:Cannot be empty.")
		if (e & VALID_NUMBER):
			pprint(":bwhite::red:Integer numbers only.")
		if (e & VALID_FLOAT):
			pprint(":bwhite::red:Floating point numbers only.")
		if (validation & VALID_LIST) and len(options)>0:
			dstring = options[0]+("/".join(options[1:]))
		elif (validation & VALID_LIST) and len(options)==1:
			dstring = options[0]
		else:
			dstring = default if default!= None else ""
		pprompt = ":cyan:%s :-::bold:[%s]: "%(prompt,(dstring))
		i = pinput(pprompt).strip()
		if validation & VALID_VALID: return i
		if (validation & VALID_NONEMPTY) and (i==""):
			e = VALID_NONEMPTY
			continue
		if (validation & VALID_NUMBER):
			try: int(i)
			except ValueError:
				e = VALID_NUMBER
				continue
		if (validation & VALID_FLOAT):
			try: float(i)
			except ValueError:
				e = VALID_FLOAT
				continue
		done = True
		break
	if (i==""): i = default
	return i


if (not os.path.exists("config.json")):
	FIRST_RUN = True
	pprint(":bold:We will need to set few things up a little at the begining.")
	settings_return = True
	#DB settings
	pprint(":green:"+eline)
	pprint(":bold::green:#DB Settings#")
	pprint(":green:"+eline)
	db_host = get_config("Database host","localhost")
	db_user = get_config("Database user name",None,VALID_NONEMPTY)
	db_pass = get_config("Database password","")
	db_name = get_config("Database name","dme")
	
	conf_store = get_config("Do you want to store these settings? Password will be stored unencrypted :red:!INSECURE!:-:",None,VALID_LIST,["Y","N"])

	if (db_host==""): db_host = "localhost"
