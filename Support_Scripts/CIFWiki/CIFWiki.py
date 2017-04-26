##################################################################################################################################################################################################
#Copyright (C) 2016 Vijay Kumar ( bitvijays )                                                                                                                                                    #
#                                                                                                                                                                                                #
#This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3        #
#of the License, or (at your option) #any later version.                                                                                                                                         #
#                                                                                                                                                                                                #
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the     #
#GNU General Public License for #more details.                                                                                                                                                   #
#                                                                                                                                                                                                #
#You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.                                                            #
#                                                                                                                                                                                                #
#                                                                                                                                                                                                #
##################################################################################################################################################################################################

import pycurl
import re
from StringIO import StringIO
from bs4 import BeautifulSoup
import os


buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://github.com/csirtgadgets/massive-octo-spice/wiki/The-CIF-Book')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

body = buffer.getvalue()
# Body is a string in some encoding.
# In Python 2, we can print it without knowing what the encoding is.
#print(body)
##Creating the beautiful soup for the Book
#soup = BeautifulSoup(open("CIFv2.book"),"html.parser")
soup = BeautifulSoup(body,"html.parser")
#print soup.ol.li
#ol = soup.find_all('ol')
#li = soup.find_all('li')
#Taking the ordered list
first_link = soup.ol
#Taking the list in ordered list
li= first_link.find_all_next('li')

#Variable for storing the list of .md file
a = []


for line in li:
##Clearing some stuff
	if re.search("Footer, go to", str(line)):
	        continue
	try:
#Creating another soup, searching if it contains href, majorly to avoid ol
		s2 = BeautifulSoup(`line`,"html.parser")
		if re.search("href=",str(line)):
			a.append(s2.a.get('href'))
		else:
#			print line
			continue
	except IndexError:
	        print "Error"

#Changing https://github.com/csirtgadgets/massive-octo-spice/wiki to https://github.com/csirtgadgets/massive-octo-spice/wiki/Home to create Home.md
pattern = "^https://github.com/csirtgadgets/massive-octo-spice/wiki$"
for idx, line in enumerate(a):
	m = re.match(pattern, line, flags=0)
	if m is None:
	    continue
	else:
	    a[idx] = "https://github.com/csirtgadgets/massive-octo-spice/wiki/Home"

##Replacing https://github.com/csirtgadgets/massive-octo-spice/wiki/ with empty spaces to get the particular md file.
pattern = "^https://github.com/csirtgadgets/massive-octo-spice/wiki/"
pattern2 = "^/csirtgadgets/massive-octo-spice/wiki/"

for idx, line in enumerate(a):
	a[idx] = re.sub(pattern,"", line, count=0, flags=0)

##Reading the extra pages!!
pages = soup.find_all('li', class_="wiki-more-pages")
for line in pages:
	s2 = BeautifulSoup(`line`,"html.parser")
	if re.search("href=",str(line)):
		temp = s2.a.get('href')
		temp = re.sub(pattern2,"",temp, count=0, flags=0)
		if temp in a:
			continue
		else:
			a.append(temp)
	else:
		print "Hello:"

##Converting the %3F pattern to ?
pattern = "%3F$"
for idx, line in enumerate(a):
	a[idx] = re.sub(pattern, "?", line, count=0, flags=0)

##Inserting # Heading on to the first line of the .md for better tracking of chapters and Headings.
for i in a:
	cmd = "sed -i '1i # " + i + "' " + i + ".md"
	print cmd
	os.system(cmd)



##Converting the .md file to .pdf file using markdown-pdf
for i in a:
	cmd = "markdown-pdf" + " " + i + ".md" + " " + "-o" + " " + i + ".pdf"
	os.system(cmd)

b=""
for i in a:
	b = b + " " + i + ".pdf"

cmd = "pdftk" + " " + b + " " + "output.pdf"
print cmd

#os.system(cmd)
