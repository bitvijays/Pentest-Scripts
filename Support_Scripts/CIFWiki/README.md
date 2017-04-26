CIFWiki: ( Collective Intelligence Framework Wiki )

A Simple python script to convert [CIF Wiki]( https://github.com/csirtgadgets/massive-octo-spice/wiki/The-CIF-Book ) into PDF. Utilizes BeautifulSoup to parse the html page, downloading the .md file, utlizing markdown-pdf to create pdf files and pdftk to merge all the pdf documents. However, we do need to clone the CIF github wiki and execute that command in that directory containing markdown files. 

Markdown-pdf and pdftk are required to be installed. markdown-pdf can be installed using 'npm install -g markdown-pdf' and pdftk can be installed using apt-get install pdftk. Also, as snort,bro pdf is not available, we need to remove them from the final pdftk command.

ToDo:

a) Improve documentation for the script.
