#!/usr/bin/python3
# -*- coding: utf-8 -*-

# # Debugging:
# import logging
# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


# Config
url_base = 'https://www.math.kit.edu/'
url_login = 'https://www.math.kit.edu/admin/person/'
url_logout = 'https://www.math.kit.edu/admin/logout/'
url_homepage_de = 'https://www.math.kit.edu/admin/person/homepage/'
url_homepage_en = 'https://www.math.kit.edu/admin/person/homepage/en/'
CAs = 'CAs/KIT-CA.pem'

from sys import stderr

if __name__ == '__main__':

	# Create session:
	import requests
	s = requests.Session()

	# Obtain session ID:
	r1 = s.get(url_login, verify=CAs)
	from lxml import html
	t1 = html.fromstring(r1.text)
	l1 = t1.xpath('//input[@name="LoginGueltigbis"]/@value')
	if len(l1) != 1:
		raise ValueError('Non-existent or non-unique field for the session expiry time.')
	else:
		expires = l1[0]

	l2 = t1.xpath('//input[@name="LoginSID"]/@value')
	if len(l2) != 1:
		raise ValueError('Non-existent or non-unique field for the session ID.')
	else:
		session_id = l2[0]

	stderr.write("Your session ID is: " + str(session_id) + '\n')
	import time
	d0 = time.gmtime(int(expires))
	stderr.write("It expires :" + time.asctime(d0) + '\n')

	# Login
	# Get password:
	import getpass
	pwd = getpass.getpass()

	# Make form:
	# Session ID in the form is the same as PHPSESSID in the
	# cookie.
	login = {"LoginNutzerkennung": '',
		'LoginPasswort': pwd,
		'LoginGueltigbis': expires,
		'LoginSID': session_id}

	# Send form:
	r2 = s.post(url_login, verify=CAs, data=login)

	# Check page retrieval:
	r3 = s.get(url_homepage_de, verify=CAs)

	with open('/tmp/html_output.html', 'wb') as f:
		f.write(r3.content)

	# Logout:
	r4 = s.get(url_logout, verify=CAs)
	with open('/tmp/logout.html', 'wb') as f:
		f.write(r4.content)
