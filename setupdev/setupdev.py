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
from ftplib import FTP

from pformat import pprint, pinput
from vinput import vinput, VALID_VALID, VALID_NONEMPTY, VALID_NUMBER, VALID_FLOAT, VALID_LIST

FIRST_RUN = False


if (not os.path.exists("config.json")):
	FIRST_RUN = True
	pprint(":bold:We will need to set a few things up a little at the begining.")
	conf_store = vinput("Do you want to store these settings? Passwords will be stored unencrypted :red:!INSECURE!:-:",None,VALID_LIST,["y","n"])
	settings_return = True
	pprint("\n")
	#DB settings
	pprint(":green:"+eline)
	pprint(":bold::green:#DB Settings#")
	pprint(":green:"+eline)
	db_host = vinput("Database host","localhost")
	db_user = vinput("Database user name",None,VALID_NONEMPTY)
	db_pass = vinput("Database password :red:!VISIBLE!:-:","")
	db_name = vinput("Database name","dme")
	pprint("\n")
	pprint(":green:"+eline)
	pprint(":bold::green:#Web Server settings#")
	pprint(":green:"+eline)
	
	www_remote = vinput("Local webserver or remote (FTP)",None,VALID_LIST,["local","ftp"]).lower()
	if (www_remote=="local"):
		### Local webserver
		while True:
			www_location = os.path.abspath(vinput("WWW data location","/var/www/dme"))
			www_overwrite = "y"
			if (os.path.exists(www_location)):
				www_overwrite = vinput("Location exists, overwrite?",None,VALID_LIST,["y","n"])
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
		ftp_host = vinput("FTP host","localhost")
		ftp_port = int(vinput("FTP port",21,VALID_NUMBER))
		ftp_user = vinput("FTP user",None,VALID_NONEMPTY)
		ftp_pass = vinput("FTP password :red:!VISIBLE!:-:","")
		pprint("FTP settings review: :green:ftp://%s@%s:%d:-:"%(ftp_user,ftp_host,ftp_port))
