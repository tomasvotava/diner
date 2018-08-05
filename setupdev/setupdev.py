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

from pformat import pprint, pinput

FIRST_RUN = False

VALID_VALID		= 0
VALID_NONEMPTY	= 1
VALID_NUMBER	= 2
VALID_FLOAT		= 4
VALID_LIST		= 8

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
		if (e & VALID_LIST):
			pprint(":bwhite::red:Choose from list of values only.")
		if (validation & VALID_LIST) and len(options)>0:
			dstring = "/".join(options)
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
			if i=="": i = default
			try: int(i)
			except ValueError:
				e = VALID_NUMBER
				continue
		if (validation & VALID_FLOAT):
			try: float(i)
			except ValueError:
				e = VALID_FLOAT
				continue
		if (validation & VALID_LIST) and (i.lower() not in list(map(str.lower,options))):
			e = VALID_LIST
			continue
		done = True
		break
	if (i==""): i = default
	return i


if (not os.path.exists("config.json")):
	FIRST_RUN = True
	pprint(":bold:We will need to set a few things up a little at the begining.")
	conf_store = get_config("Do you want to store these settings? Passwords will be stored unencrypted :red:!INSECURE!:-:",None,VALID_LIST,["y","n"])
	settings_return = True
	pprint("\n")
	#DB settings
	pprint(":green:"+eline)
	pprint(":bold::green:#DB Settings#")
	pprint(":green:"+eline)
	db_host = get_config("Database host","localhost")
	db_user = get_config("Database user name",None,VALID_NONEMPTY)
	db_pass = get_config("Database password :red:!VISIBLE!:-:","")
	db_name = get_config("Database name","dme")
	pprint("\n")
	pprint(":green:"+eline)
	pprint(":bold::green:#Web Server settings#")
	pprint(":green:"+eline)
	
	www_remote = get_config("Local webserver or remote (FTP)",None,VALID_LIST,["local","ftp"]).lower()
	if (www_remote=="local"):
		### Local webserver
		while True:
			www_location = os.path.abspath(get_config("WWW data location","/var/www/dme"))
			www_overwrite = "y"
			if (os.path.exists(www_location)):
				www_overwrite = get_config("Location exists, overwrite?",None,VALID_LIST,["y","n"])
				if (www_overwrite.lower()=="n"): continue
				else: break
			else:
				try:
					os.makedirs(www_location)
				except Exception as m:
					pprint(":red:"+str(m)+":-:")
					pprint(":red::bold:Invalid path or insufficient rights.:-:")
					continue
			break
	else:
		### FTP webserver
		ftp_host = get_config("FTP host","localhost")
		ftp_port = int(get_config("FTP port",21,VALID_NUMBER))
		ftp_user = get_config("FTP user",None,VALID_NONEMPTY)
		ftp_pass = get_config("FTP password :red:!VISIBLE!:-:","")
		pprint("FTP settings review: :green:ftp://%s@%s:%d:-:"%(ftp_user,ftp_host,ftp_port))
