#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Benjamin Horvath (benhorvath@gmail.com)
Date: March 21, 2016

Web scraping script to store all of Hillary Clinton's e-mails from the 
Wikileaks archive (30,322 total e-mails) in JSON. 

"""

# Libraries
from bs4 import BeautifulSoup
from json import JSONEncoder
import mechanize
import re

# Function to grab content from Wikileaks
def cleanHeader(email):
	""" Excepts HTML of Wikileaks e-mails, scrapes relevant content, and 
	    cleans it. Returns e-mail content.
	"""
	header = email.find(id = 'header').get_text()
	noTabs = header.replace('\t', '')
	deleteFields = ['To: ', 'From: ', 'Date: ', 'Subject: ']
	for field in deleteFields:
		noTabs = noTabs.replace(field, '')
	stripped = noTabs.strip()
	headerList = stripped.split('\n')
	return headerList

# Open txt to append to 
l = open('hillary_archive.txt', "a")

# Wikileaks addresses
baseUrl = 'https://www.wikileaks.org/clinton-emails/emailid/'

for i in range(1, 30323):  # 4138, 8129 timeout -- check
	print(i),

	# Address of e-mail to pull
	emailId = i
	emailUrl = baseUrl + str(emailId)

	# Open connection
	browser = mechanize.Browser() 
	browser.open(emailUrl)

	# Grab e-mail HTML
	email = BeautifulSoup(browser.response().read())

	# Grab e-mail header
	wl_header = cleanHeader(email)

	# Organize header information
	try:
		wl_to = wl_header[0]
	except:
		wl_to = 'NA'

	try:
		wl_from = wl_header[1]
	except:
		wl_from = 'NA'

	try:
		wl_date = wl_header[2]
	except:
		wl_date = 'NA'

	try:
		wl_subj = wl_header[3]
	except:
		wl_subj = 'NA'

	# Grab State Department appended information
	try:
		stateId = email.findAll(class_ = 'unclassified')[0].get_text()
	except:
		stateId = 'NA'
	
	try:
		release = email.findAll(class_ = 'unclassified')[1].get_text()
	except:
		release = 'NA'

	# Grab message contents
	message = email.find(id="uniquer")

	for tag in message.findAll(class_ = 'unclassified'):
		tag.extract()  # removes classified 

	message = message.get_text().replace('\t', '')
	message = message.replace('B6', '')
	message = re.sub(' +', ' ', message)
	message = message.strip()

	# Assmemble data into JSON object
	jsonEmail = JSONEncoder().encode({
		'email_id': emailId, 
		'email_url': emailUrl,
		'wl_to': wl_to,
		'wl_from': wl_from,
		'wl_date': wl_date,
		'wl_subj': wl_subj,
		'state_id': stateId,
		'release': release,
		'message': message
	})

	# Append JSON-formatted e-mail to file
	l.write(jsonEmail)
	l.write(',\n')
	browser.close()
	print('... SUCCESS')

	# NOTE: At end, will need to bracket [] and delete the last comma

# Close connection to write file
l.close()

print("... COMPLETE ...")
