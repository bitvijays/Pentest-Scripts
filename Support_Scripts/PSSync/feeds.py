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



import requests
from bs4 import BeautifulSoup
from newspaper import Article,Config
import sqlite3
from math import ceil

###Global Variables
link0=""
ps_num_pages=0
ps_num_articles=0
db_num_pages=0
db_num_articles=0
diff_pages=0
diff_articles=0
#PSNews Variables
uniq_id=title=datetime=postedby=detailsd=tags=actlinks=authors=summary=detailed=""
#PSFiles Variables Extra
ico=refer=details=os=cve=md5=""

###Initialize the database connection and create new tables if not exists"
conn = sqlite3.connect('packetstorm.db')
c = conn.cursor()

##Function to initialize the database a) Creates psnews, psfiles and psstats tables
def db_init():
    # Create table for PacketStorm News
    c.execute('''CREATE TABLE IF NOT EXISTS psnews (uniq_id text PRIMARY KEY, title text, datetime text, postedby text, detailsd text, tags text, actlinks text, authors text, summary text, detailed text, npsync text )''')
    c.execute('''CREATE TABLE IF NOT EXISTS psfiles ( uniq_id text PRIMARY KEY, ico text, title text, datetime text, refer text, details text, tags text, os text, cve text, md5 text, actlinks text, summary text, detailed text, npsync text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS psstats ( pstype text PRIMARY KEY, db_num_articles int, db_num_pages int, ps_num_articles int, ps_num_pages int )''')

###Function to insert the values in to the respective tables, values are passed from the global variables    
def db_insert(pstype):

    if (pstype == "psnews"):
        c.execute("insert or ignore into psnews(uniq_id, title, datetime, postedby, detailsd, tags, actlinks, authors, summary, detailed, npsync) values (?, ?, ?, ?, ?, ?, ?, ?, ? , ?, 'N')", (uniq_id,title,datetime,postedby,detailsd,tags,actlinks, authors, summary, detailed))
        conn.commit()
    elif ( pstype == "psfiles"):
        c.execute("INSERT or ignore INTO PSFILES( uniq_id, ico, title, datetime, refer, details, tags, os, cve, md5, actlinks, summary, detailed, npsync) values (?,?,?,?,?,?,?,?,?,?,?,?,?,'N')", (uniq_id, ico, title, datetime, refer, details, tags, os, cve, md5, actlinks, summary, detailed))
        conn.commit()
    elif ( pstype == "psstats"):
##Entering two values as we would only be updating these values        
        c.execute("INSERT or ignore INTO PSSTATS( pstype, db_num_articles, db_num_pages, ps_num_articles, ps_num_pages) values ( 'psnews', ?, ?, ?, ?)", ( db_num_articles,db_num_pages,ps_num_articles,ps_num_pages))
        c.execute("INSERT or ignore INTO PSSTATS( pstype, db_num_articles, db_num_pages, ps_num_articles, ps_num_pages) values ( 'psfiles', ?, ?, ?, ?)", ( db_num_articles,db_num_pages,ps_num_articles,ps_num_pages))
        conn.commit()

###Function to close the database connection
def db_close():
    # Save (commit) the changes
    conn.commit()
    conn.close()
    
    
#Define what needs to be sync whether the news or the files
#Based on what needs to be synced, link needs to set and soup generated
def syncwhat(pstype, link):

    global link0
    global ps,psc,soup

    if (pstype == "psnews"):
        link0 = "https://packetstormsecurity.com/news/"
    elif (pstype == "psfiles"):
        link0 = "https://packetstormsecurity.com/files/"
    else:
        print "Error in function syncwhat"

#    print link0
    
    if (link == "None"):
        link = link0
    
    ps = requests.get(link)
    print "Syncing " + link
    psc = ps.content
    soup = BeautifulSoup(psc, "lxml")
    
# Figure out the number of articles / pages in psnews or psfiles
def find_numpages_articles(pstype):

    global diff_pages, diff_articles
    
    for i in soup.find_all("div",{'id':"nv"}):
        temp=i.form.find_all('input', {'id':"page-max"})
        for k in temp:
            ps_num_pages=k['value'].replace(',','')

    d=soup.find_all("span", {'id':"total"})
    for i in d:
        e = i.text
        ps_num_articles = e.split("of ")[1].replace(',','')
        
    c.execute("UPDATE psstats SET ps_num_articles = ? ,ps_num_pages = ? WHERE pstype= ? ",  (ps_num_articles,ps_num_pages,pstype))
    c.execute("select db_num_articles, db_num_pages from psstats where pstype = ? ",(pstype,))
    row=c.fetchone()
    
    db_num_articles = int(str(str(row[0]).encode('ascii','ignore')).replace(',',''))
    db_num_pages = int(str(str(row[1]).encode('ascii','ignore')).replace(',',''))
#    print db_num_pages
#    print db_num_articles
       
#The assumption is that we have sync it first time to the end of the articles!!    
    diff_pages = int(ps_num_pages) - int(db_num_pages)
    diff_articles = int(ps_num_articles) - int(db_num_articles)
    print "The difference is in pages " + str(diff_pages) + " in articles " + str(diff_articles)


###This function crawls the psnews/ psfiles pages. If we need to scroll particular pages, range in the for loop can be modified
def page2parse( pstype, pages, arti):

    global link0

    if ((pages == 0) and (arti > 0)):
        parse_what(pstype)            

    elif (pages> 0 ):
        for counter in range(1,pages+1):
#        for counter in range(1,8):
            if (counter==1):
                parse_what(pstype)
            else:
                link = link0 + "page" + str(counter) + "/"
#                print link
#                print counter
                syncwhat(pstype,link)
                parse_what(pstype)


###Function to parse the actual pages of psnews/psfiles
###After parsing, it also inserts the rows in respective tables and updates the count in psstats table.
def parse_what(pstype):
    
    global uniq_id,title,datetime,postedby,detailsd,actlinks,tags,authors,summary,detailed,ico,refer,details,os,cve,md5
    if pstype == "psnews":
        
        for i in soup.find_all("dl",{'class':"news"}):
            uniq_id = i['id']
            title = i.find("dt").text
            datetime = i.find("dd",{'class':"datetime"}).text
            postedby = i.find("dd",{'class':"posted-by"}).text
            try:
                detailsd = i.find("dd",{'class':"detail sd"}).text
            except:
                print "To handle case where detailsd is replaced by detail"
                detailsd = i.find("dd",{'class':"detail"}).text
                detailsd = ""
                
            actlinks = i.find("dd",{'class':"act-links"}).a.get('href')
            
            try:
                tags = i.find("dd",{'class':"tags"}).text
            except:
                print "To handle case where tags class is missed"
                tags =""
            db_insert(pstype)
    
            
    elif pstype == "psfiles":
        
        for i in soup.find_all("dl",{'class':"file"}):
            uniq_id = i['id']
            ico = i.find("dt").a['class'][1]
            title = i.find("dt").text
            datetime = i.find("dd",{'class':"datetime"}).text
            try:
                refer = i.find("dd",{'class':"refer"}).text
            except:
                refer = ""
            try:
                details = i.find("dd",{'class':"detail"}).text
            except:
                print "To handle case where details is replaced by detail"
                details = i.find("dd",{'class':"detail"}).text
                details = ""
                
            temp_actlinks = i.find("dd",{'class':"act-links"}).a.get('href')
            actlinks = "https://packetstormsecurity.com" + temp_actlinks
            try:
                tags = i.find("dd",{'class':"tags"}).text
            except:
                print "To handle case where tags class is missed"
                tags =""
            try:
                os = i.find("dd",{'class':"os"}).text
            except:
                os=""
            try:
                cve = i.find("dd",{'class':"cve"}).text
            except:
                cve = ""
            try:
                md5 = i.find("dd",{'class':"md5"}).text
            except:
                md5 = ""
#            print uniq_id + " " + ico + " " + title + " " + datetime + " " + refer + " " + detail + " " + actlinks + " " + tags + " " + os + " " + cve + " " + md5
            db_insert(pstype)
    
    
    if (pstype == "psnews"):
        c.execute("select count(*) from psnews")
    elif(pstype == "psfiles"):
        c.execute("select count(*) from psfiles")
        
    row = c.fetchone()
    db_num_article_sync = row[0]
#As of now there are 25 articles on one page and the calculation is done on that basis
#Adding one more in case of extra articles
    db_num_pages_sync = ceil(db_num_article_sync/25)
##This logic seems buggy:
#    if ((db_num_article_sync/25) > 0.1):
#        db_num_pages_sync = db_num_pages_sync + 1
#Adding in the database
    c.execute("UPDATE psstats SET db_num_articles = ?, db_num_pages = ? WHERE pstype= ? ",  (db_num_article_sync,db_num_pages_sync, pstype))



###Function to execute newspaper tool to get the authors, summary and detailed text!
###Warning summary and detailed modification might be required!
###This function check for the npsync value ( which is by default N). If 'N', fetch the link and extract summary and other information.
def newspapersync(pstype):
#Another cursor required to update the tables in the for loop, otherwise only one record was updated!     
    d = conn.cursor()
    global authors,summary,detailed
#    c.execute("UPDATE ps_news SET npsync = 'N' ")
    for row in c.execute("Select uniq_id, actlinks from psnews where npsync = 'N' "):
        temp_uniq_id = row[0]
        temp_actlinks = row[1]
        print "Syncing newspaper of " + temp_uniq_id
        try:
            a = Article(temp_actlinks,language = 'en')
            a.download()
            a.parse()
            a.nlp()
            temp_authors = a.authors
            authors = ','.join(temp_authors)
            summary = a.summary
            detailed = a.text
        
            d.execute("Update psnews SET authors =? , summary = ?, detailed = ?, npsync = 'Y' where uniq_id = ? " , (authors,summary,detailed,temp_uniq_id))
            conn.commit()
        except:
###Setting npsync status as E where error is occuring
            d.execute("Update psnews SET npsync = 'E' where uniq_id = ? " , (temp_uniq_id,))
    
	    
    
###Main Function     
def main():
    
    db_init()
    pstype="psfiles"
    db_insert("psstats")
    syncwhat(pstype, "None")

    find_numpages_articles(pstype)
    if ((diff_pages == 0 ) and (diff_articles == 0)):
        print "Everything is in Sync as of now!"
    elif ((diff_pages >= 0) or (diff_articles > 0)):
        page2parse( pstype, diff_pages, diff_articles)
    
#News paper sync as of only for psnews        
    if (pstype == "psnews"):
        newspapersync(pstype)
        
    db_close()

main() 
