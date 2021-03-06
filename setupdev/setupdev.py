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

"""
Setup the environment for development purposes
More info at https://github.com/tomasvotava/diner/tree/master/setupdev
"""

eline = "#################################"

import os
import json
import sys
from ftplib import FTP as _FTP, error_perm as ftp_error_perm

from pformat import pprint, pinput, pformat
from vinput import vinput, VALID_VALID, VALID_NONEMPTY, VALID_NUMBER, VALID_FLOAT, VALID_LIST

from math import ceil

import mysql.connector as mysql

FIRST_RUN = False
conf = {}

class FTP(_FTP):
	def __init__(self,host,user,passwd):
		_FTP.__init__(self,host,user,passwd)
		self.transfered = 0
		self.fsize = 0
	def exists(self,path):
		cur = self.pwd()
		texists = False
		try:
			self.cwd(path)
			texists = True
			self.cwd(cur)
		except ftp_error_perm as m:
			#Borrowed from https://stackoverflow.com/questions/5663787/upload-folders-from-local-system-to-ftp-using-python-script
			if (str(m.args).count("550")):
				texists = False
		return texists
	def stor(self,dest,source):
		self.transfered = 0
		self.fsize = os.path.getsize(source)
		with open(source,"rb") as infile:
			self.storbinary("STOR %s"%dest,infile,callback=self.storcallback)
			sys.stdout.write(80*" "+"\r")
	def storcallback(self,datablock):
		self.transfered+=len(datablock)
		sys.stdout.write(pformat(":yellow:Transfering %d / %d bytes (%d %%)                       \r"%(self.transfered,self.fsize,ceil(self.transfered/self.fsize*100))))
	def makedirs(self,path):
		path = os.path.normpath(path)
		parts = path.split(os.sep)
		current = self.pwd()
		for p in parts:
			if (not self.exists(p)): self.mkd(p)
			self.cwd(p)
		self.cwd(current)
		
def leave():
	print(":yellow::bold:Something went wrong. Exiting.")
	sys.exit(0)

if (not os.path.exists("config.json")):
	FIRST_RUN = True
	pprint(":bold:We will need to set a few things up a little at the begining.")
	conf["store"] = vinput("Do you want to store these settings? Passwords will be stored unencrypted :red:!INSECURE!:-:",None,VALID_LIST,["y","n"])
	settings_return = True
	pprint("\n")
	#DB settings
	while True:
		pprint(":green:"+eline)
		pprint(":bold::green:#DB Settings#")
		pprint(":green:"+eline)
		conf["db_host"] = vinput("Database host","localhost")
		conf["db_user"] = vinput("Database user name",None,VALID_NONEMPTY)
		conf["db_pass"] = vinput("Database password :red:!VISIBLE!:-:","")
		conf["db_name"] = vinput("Database name","dme")
		pprint(":yellow:Attempting connection to the MySQL db...")
		try:
			mydb = mysql.connect(host=conf["db_host"],user=conf["db_user"],passwd=conf["db_pass"],database=conf["db_name"])
			pprint(":green::bold:Success\t:bwhite:Connected")
			break
		except Exception as m:
			pprint(":red::bold:Failed:normal:\t:red::bwhite:%s"%str(m))
			continue
	pprint("\n")
	pprint(":green:"+eline)
	pprint(":bold::green:#Web Server settings#")
	pprint(":green:"+eline)
	
	conf["www_remote"] = vinput("Local webserver or remote (FTP)",None,VALID_LIST,["local","ftp"]).lower()
	if (conf["www_remote"]=="local"):
		### Local webserver
		while True:
			conf["www_location"] = os.path.abspath(vinput("WWW data location","/var/www/dme"))
			conf["www_overwrite"] = "y"
			if (os.path.exists(conf["www_location"])):
				conf["www_overwrite"] = vinput("Location exists, overwrite?",None,VALID_LIST,["y","n"])
				if (conf["www_overwrite"].lower()=="n"): continue
				else: break
			else:
				try:
					os.makedirs(conf["www_location"])
				except Exception as m:
					pprint(":red:"+str(m)+":-:")
					pprint(":red::bold:Invalid path or insufficient rights.:-:")
					continue
			break
	else:
		### FTP webserver
		while True:
			conf["ftp_host"] = vinput("FTP host","localhost")
			#conf["ftp_port"] = int(vinput("FTP port",21,VALID_NUMBER)) #not available yet
			conf["ftp_user"] = vinput("FTP user",None,VALID_NONEMPTY)
			conf["ftp_pass"] = vinput("FTP password :red:!VISIBLE!:-:","")
			pprint("FTP settings review: :green:ftp://%s@%s:-:"%(conf["ftp_user"],conf["ftp_host"]))
			pprint(":yellow:Attempting connection to the FTP server... ")
			try:
				ftp = FTP(conf["ftp_host"],conf["ftp_user"],conf["ftp_pass"])
				pprint(":green::bold:Success\t:bwhite:Connected")
				break
			except Exception as m:
				pprint(":red::bold:Failed:normal:\t:red::bwhite:%s"%str(m))
				continue
		while True:
			conf["www_location"]= vinput("FTP www files location","www/dme")
			if (ftp.exists(conf["www_location"])):
				pprint(":yellow:Remote directory already exists.")
				while True:
					conf["www_overwrite"] = vinput("Overwrite remote directory?",None,VALID_LIST,["y","n"])
					if (conf["www_overwrite"].lower()=="n"): continue
					else: break
				break
			else:
				try:
					ftp.mkd(conf["www_location"])
					pprint(":green:Output location created successfully.")
					break
				except Exception as m:
					pprint(":red:Specified location cannot be used.:bwhite:\t%s"%str(m))
					continue
			try: ftp.close()
			except Exception as m: pprint(":red:Warning Closing FTP failed.\t:bwhite:%s"%str(m))
		pprint("\n")
	# save settings (if wanted)
	if (conf["store"].lower()=="y"):
		config_string = json.dumps(conf)
		fid = open("config.json","w")
		fid.write(config_string)
		fid.close()
		pprint(":green:Settings stored.")
else: #previous config found
	fid = open("config.json","r")
	conf = json.loads(fid.read())
	fid.close()
	pprint(":yellow::bold:Configuration from previous session was found and can be used. Check it bellow.")
	pprint("#:cyan:DB Settings: :bold:%s@%s/%s"%(conf["db_user"],conf["db_host"],conf["db_name"]))
	pprint("#:cyan:Web Server Settings: :bold:%s"%conf["www_remote"])
	if (conf["www_remote"].lower()=="ftp"):
		pprint("#:cyan:FTP Settings: :bold:%s@%s:%s"%(conf["ftp_user"],conf["ftp_host"],conf["www_location"]))
	else:
		pprint("#:cyan:Web location: :bold:%s"%(conf["www_location"]))
	if (vinput("Do you want to start over? :red::bold:Previous configuration will be deleted.",None,VALID_LIST,["y","n"]).lower()=="y"):
		os.remove("config.json")
		pprint(":yellow:Configuration was deleted, start the script again to start over.")
		sys.exit(0)
pprint(":green:"+eline)
pprint(":bold::green:#Required info gathered#")
pprint(":green:"+eline)
pprint(":yellow:Press ENTER to start deployment, Ctrl+C to quit...")
try: input("")
except KeyboardInterrupt: sys.exit(0)
	
### START Deployment
pprint(":yellow:### Deploying the db")
pprint(":yellow:Connecting...")
try:
	mydb = mysql.connect(host=conf["db_host"],user=conf["db_user"],passwd=conf["db_pass"],database=conf["db_name"])
	mcur = mydb.cursor(buffered=True)
	pprint(":green:Connected.")
	query = "SHOW TABLES"
	mcur.execute(query)
	if (mcur.rowcount!=0):
		pprint(":cyan:There are tables in :bold:%s"%conf["db_name"])
		if (vinput("Do you wish to use the db anyway?",None,VALID_LIST,["y","n"]).lower()=="n"):
			sys.exit(0)
	mcur.close()
except Exception as m:
	pprint(":red:Could not connect. Exiting.")
	pprint(":red::bold:%s"%str(m))
	sys.exit(0)
with open("../db/diner.sql","r") as sqlfile:
	sql = sqlfile.read()
	pprint(":yellow:Creating schema...")
	mcur = mydb.cursor(buffered=True)
	try:
		results = mcur.execute(sql,multi=True)
		for cur in results:
			if cur.with_rows: pprint(":yellow:%s"%str(cur.fetchall()))
		pprint(":green::bold:Done.\n")
	except Exception as m:
		pprint(":red:Could not create DB schema.\t:bold:%s"%str(m))
		sys.exit(0)
if conf["www_remote"].lower()=="ftp":
	ftp = FTP(conf["ftp_host"],conf["ftp_user"],conf["ftp_pass"])
	pprint(":magenta:FTP:Changing directory to \'%s\'"%conf["www_location"])
	if (not ftp.exists(conf["www_location"])): ftp.mkd(conf["www_location"])
	ftp.cwd(conf["www_location"])
else:
	ftp = None

wwwsource = "../www/"
for dirpath, dirnames, filenames in os.walk(wwwsource):
	for fname in filenames:
		pprint(":cyan:Copy file \'%s\'"%fname)
		source = os.path.abspath(os.path.join(dirpath,fname))
		remote = os.path.relpath(source,wwwsource)
		head,tail = os.path.split(remote)
		if head:
			if not ftp.exists(head):
				pprint(":cyan:Creating remote folder \'%s\'"%head)
				ftp.makedirs(head)
			pprint(":cyan:Current directory \'%s\'"%head)
			ftp.cwd(head)
		ftp.stor(fname,source)
