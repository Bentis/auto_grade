# -*- coding: utf-8 -*-
import re
import os
from pickle import Pickler, Unpickler
import mechanize
from BeautifulSoup import BeautifulSoup

from notification import notify_email, notify_sms
from settings import *

STUDWEB_URL = 'https://studentweb.ntnu.no/'
STORAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'known.pickle')

def notify(string):
    if NOTIFY_METHOD == EMAIL:
        notify_email(EMAIL_SENDER, EMAIL_ADDRESS, "New grade on Studweb!", string)
    elif NOTIFY_METHOD == SMS:
        notify_sms(SMS_TELE2_EUROBATE_ID, SMS_TELE2_NUMBER, SMS_RECIEVER, string.encode('iso-8859-1'))
    else:
        print string

known_grades = None
update = False

try:
    fp = open(STORAGE_FILE, 'r')
    known_grades = Unpickler(fp).load()
    fp.close()

except IOError, EOFError: # Bad storage file, probably first run
    known_grades = list()
    update = True

br = mechanize.Browser()
br.open(STUDWEB_URL)

br.select_form(name='fnrForm')
br['fodselsnr'] = BIRTH_NUMBER
br['pinkode'] = PIN_NUMBER
br.submit()

br.follow_link(text_regex='Oversikt')
br.follow_link(text_regex='Resultater')

data = br.response().get_data()
soup = BeautifulSoup(data)

main = soup.find('td', {'class':'main'})
rows = main.findAll('tr', {'class': re.compile('pysj(0|1)')})

for row in rows:
    tds = row.findAll('td')
    
    course_id = str(tds[1].string)
    course_name = unicode(tds[2].string)
    grade = str(tds[7].string)
    
    if course_id not in known_grades:
        # found new!
        update = True
        known_grades.append(course_id)
        
        notify("New grade: %s - %s: %s" % (course_id, course_name, grade))

if update:
    fp = open(STORAGE_FILE, 'w')
    Pickler(fp).dump(known_grades)
    fp.close()

br.follow_link(text_regex='Logg ut')
