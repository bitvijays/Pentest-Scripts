| Background |
 ------------
WhatWeb is excellent in fingerprinting web apps to the next level in pentest engagements. 80% exploitable flaws exist in web layer and they're mostly unprotected by WAFs. When performing PTs over large array of IPs in tight deadline, recon must be done as fast as possible via automation.


| Tell-Me-Web (Automating WhatWeb from NMap output) |
 ----------------------------------------------------
The tell-me-web takes nmap output in Grepable format (-oG) generated together with -sV option.
It extracts all hosts with http & https ports open.
Then it feeds them into whatweb. 

Brendan Coles wrote a similar script in bash which runs whatweb in all ports - https://gist.github.com/798148


| Log Path |
 ----------
Scan results can be found in logs/ folder. Result files are separated per each IP per port with .whatweb extension.


| How to configure |
 ------------------
If you don't want to use default whatweb installation in BT 4 (/pentest/enumeration/www/whatweb/whatweb), edit $whatweb variable and insert it your whatweb path in whatweb.config file. Then do svn ignore whatweb.config (svn propedit svn:ignore ./whatweb.config)


| How to download/update |
 -----------------------
svn co http://tellmeweb.googlecode.com/svn/trunk/ tellmeweb


| Tutorial |
 -----------------------
http://www.aldeid.com/index.php/Tellmeweb


| About WhatWeb |
 ---------------
 WhatWeb Home: http://www.morningstarsecurity.com/research/whatweb
 YEHG WhatWeb Plugins Beta: https://github.com/yehgdotnet/whatweb-plugins/tree/master/new-plugins
 