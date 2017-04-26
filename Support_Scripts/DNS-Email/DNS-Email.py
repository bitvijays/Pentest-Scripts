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
#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("domain",help="Domain Name")
#args = parser.parse_args()
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("domain", help="Email address from which Domain Name are registered")
args = parser.parse_args()
print(args.domain)

if args.domain:
	url="http://viewdns.info/reversewhois/?q=" + args.domain
	buffer = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()

	body = buffer.getvalue()
	soup = BeautifulSoup(body,"html.parser")

	td = soup.find_all('table')

	print td[3]
	flag=0
	a=[]
	start='<td>'
	end='</td>'
	for i in td[3].find_all('td'):
		flag=flag+1
		if flag>0:
			if (flag-1)%3 == 0:
##				print i
#				print i[1:-1]
				result = re.search('%s(.*)%s' % (start, end), str(i)).group(1)
				print result
