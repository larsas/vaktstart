import json
import lz4
import sys
import subprocess
import getpass
import os.path
from os import path
import string
import re
#import urlmarker
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#./lz4json/lz4jsoncat ~/.mozilla/firefox/*/sessionstore-backups/recovery.jsonlz4



#Information in recovery.jsonlz4 file seems to be split into one area with active firefox windows, and previously opened windows(but now closed) below. 

test = subprocess.Popen(["/home/larsas/lz4json/lz4jsoncat","/home/larsas/.mozilla/firefox/gzt4icdx.default-release/sessionstore-backups/previous.jsonlz4"], stdout=subprocess.PIPE)
#recovery.jsonlz4"
#print(type(test))
output = test.communicate()[0]
#new_str = output.decode('utf-8') # Decode using the utf-8 encoding
#print(new_str)
#print(type(new_str))
#print(output)
#print(type(output))
#print(new_str)
#print('--------------------------------------------------HERE------------------------------')
#cjson=json.dumps(output)
#print(type(cjson))
#print(cjson)
#print(type(cjson))

d = json.loads(output)

#remove_ct=int(d.find('_closedTabs'))
#print(d.find('_closedTabs'))
#new_d=d[:remove_ct]
#new_d=d
new_d=json.dumps(d)

#print(new_d)
#print(type(new_d))

urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', new_d)
print(urls)

#driver = webdriver.Firefox()
#driver.current_url

#driver.window_handles[0].current_url



#https://selenium-python.readthedocs.io/getting-started.html

#https://stackoverflow.com/questions/46416852/get-urls-of-all-open-tabs-using-python

#geckodriver
#https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path


