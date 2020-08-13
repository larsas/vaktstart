#!/usr/bin/env python3

'''
vaktstart_input_maker.py test version 1.3 (12.08.2020) Author: larsas@met.no

This script creates a textfile which can be used as an input file for the vakstart script
and this textfile should only be interpreted as an origin file, i.e it will require some manual tuning

This script can see your open programs, which desktop they are on with size and location, and it saves your open programs into a textfile with a specific setup.

You need to add your own quickmenus in diana and urls in firefox and google chrome.

--------------------------------------------------------------------------------

How to run this python script: 

type <python3 vaktstart_input_maker.py> while in </vol/vvfelles/bin> folder (cd /vol/vvfelles/bin/ to go into folder in terminal)

in your local terminal (without brackets)

--------------------------------------------------------------------------------

How to run the vaktstart script with this setupfile: 

type </vol/vvfelles/bin/vaktstart /vol/home-vpv/<your ldap username>/<your_textfile>> 

in your local terminal (without brackets)

--------------------------------------------------------------------------------

The script can see the following programs:


[diana , diana vertikale profiler, diana vertikale tverrsnitt, diana bølgespekter, tseries, firefox, QED, modfly, google chrome, ted]


All other programs are ignored

--------------------------------------------------------------------------------

Warning: The y position may, in some cases, deviate with 30 pixel values and require manual tuning. Other issues may also occur.

''' 


import getpass
import subprocess
import os.path
import os
from os import path
import string
import re
from operator import itemgetter

#Programs that the script can see
programs  = ['(diana)','Profiler', 'Tverrsnitt', 'Bølgespekter', 'tseries','Firefox','QED','modfly','Chrome','Ted']

#Input value names of each program
programnames=['diana','dvp','dvc','dwspec','tseries','firefox','QED','modfly','google','ted']

#xy stat strings to look for
xydetails=['Absolute upper-left X:','Absolute upper-left Y:', 'Width', 'Height','Frame extents']

#Empty array to put all useful information into
programlist= []

#Get windows open and window id's
output = os.popen('wmctrl -l').readlines() 

#Manipulate output of wmctrl -l
for i in range(0,len(programs)):
	for j in range(0,len(output)):
		if programs[i] in output[j]:
			
			#Empty array to put program information and xy stats into. 
			programspecifics= []

			iddespro=re.split("( )",output[j])
			programid=iddespro[0]
			programiddesktop=iddespro[4]
			programspecifics.append(iddespro[0])
			programspecifics.append(iddespro[4])

			for k in range(0,len(iddespro)):
				if iddespro[k].find(programs[i])==0:
					if programs[i]==programs[i]:

						iddespro[k]=programnames[i]
					programspecifics.append(iddespro[k])
					

			#Get x and y position and size values, including frame extent correction.
			xystats = os.popen('xwininfo -stats -wm -id {}'.format(iddespro[0])).readlines()

			
			#Manipulate xystats output
			for l in range(0,len(xydetails)):
				for o in range(0,len(xystats)):
					if xydetails[l] in xystats[o]:
						programspecifics.append(xystats[o])

			#Put all information into an array, programs and x y stats. 
			programlist.append(programspecifics)


			#Create an array that has all details on each program sorted by desktop
			sortprogramlist= sorted(programlist, key=itemgetter(1,0)) #Sort after index 0 AND 1, id's and desktopnumber. 

#Do not open modfly windrose
modflylist= []
for t in range(0,len(sortprogramlist)-1):
	if sortprogramlist[t][2]=='modfly' and sortprogramlist[t][0][0:5]==sortprogramlist[t+1][0][0:5]:
		modflyindex=t+1
		modflylist.append(sortprogramlist[t+1])


if modflylist is None:
	pass
else:
	for i in range(0,len(modflylist)):

		sortprogramlist.remove(modflylist[i])
	
	
#Get username
user= getpass.getuser() 

#Name of textfile
vaktstartsetupfileandpath = input('Please enter path to file (for example: /vol/home-vpv/{}/name_of_input_file):'.format(user))

#Home folders <-- if needed, can make array of words, currently not necessary if only two strings.  
#address=['$HOME','~']
#for p in range(0,len(address)):

if vaktstartsetupfileandpath.find('$HOME')==0:
	vaktstartsetupfileandpath= vaktstartsetupfileandpath.replace('$HOME','/home/{}'.format(user))

elif vaktstartsetupfileandpath.find('~')==0:
	vaktstartsetupfileandpath=vaktstartsetupfileandpath.replace('~','/home/{}'.format(user))
else:
	pass

#Make textfile to put setup into. 
if os.path.exists(vaktstartsetupfileandpath):
	oayn=input('Textfile exist already. Please type <a> and press <enter> to append to textfile, type <o> and press <enter> to overwrite the textfile or choose another textfilename:')
	if oayn=='a':
		append_write = 'a+' # append if already exists
		print('\n') 
		print('Appending programs to {}...'.format(vaktstartsetupfileandpath))
		print('\n')
	if oayn=='o':
		#Read file again and then write, this will overwrite file. 
		with open(vaktstartsetupfileandpath, "r") as f:
    			data = f.read()
		append_write = 'w'
		print('\n') 
		print('Overwriting {}...'.format(vaktstartsetupfileandpath))
		print('\n')

else:
	append_write = 'w+' # make a new file if not
	#print('\n')
	#print('File does not exist making new textfile named {}...'.format(vaktstartsetupfileandpath))
	#print('\n')

textfile = open(vaktstartsetupfileandpath,append_write)

#Write information to textfile
for r in range(0,len(sortprogramlist)):

	#Make sure desktop headline is written out once for each desktop
	if sortprogramlist[r-1][1]==sortprogramlist[r][1]:
		pass
	else:	
		if int(sortprogramlist[r][1])==0:
			textfile.write('#----------------Desktop {} ----------------'.format(sortprogramlist[r][1]))
		else:
			textfile.write('\n#----------------Desktop {} ----------------'.format(sortprogramlist[r][1]))
		textfile.write('\n')

	textfile.write('\napplication={}'.format(sortprogramlist[r][2]))
	textfile.write('\ncommandline=')
	textfile.write('\ndesktop={}'.format(sortprogramlist[r][1]))
	textfile.write('\nxposition={}'.format(int(''.join(filter(str.isdigit, sortprogramlist[r][3])))))
	#Correct for frame extent value if it exists
	if 'Frame extents' in sortprogramlist[r][-1] and not sortprogramlist[r][2]=='modfly':# and not sortprogramlist[r][2]=='QED':
		corrval=int(sortprogramlist[r][7].split(',')[2])
		correcty= int(''.join(filter(str.isdigit, sortprogramlist[r][4])))-corrval
		textfile.write('\nyposition={}'.format(correcty))
	else:
		textfile.write('\nyposition={}'.format(int(''.join(filter(str.isdigit, sortprogramlist[r][4])))))
	textfile.write('\nxsize={}'.format(int(''.join(filter(str.isdigit, sortprogramlist[r][5])))))
	textfile.write('\nysize={}'.format(int(''.join(filter(str.isdigit, sortprogramlist[r][6])))))
	textfile.write('\n')






















