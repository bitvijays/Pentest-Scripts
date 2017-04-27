This script utilizes the script from the tellmeweb created by YGN Ethical Hacker Group, Yangon, Myanmar. It modifies it to use nikto on multiple websites.

**Description**:
    
The niktomeweb takes gnmap outpout (-oG) generated together with -sV option.  It takes all hosts with http & https ports open. Then it feeds them into nikto. It also saves all the nikto files in the folder.


**Background**
Nikto is excellent Scan web server for known vulnerabilities for websites. When performing PTs over large array of IPs in tight deadline, recon must be done as fast as possible via automation.


**Nikto-Me-Web (Automating Nikto from NMap output)**
The Nikto-me-web takes nmap output in Grepable format (-oG) generated together with -sV option. It extracts all hosts with http & https ports open. Then it feeds them into nikto. 

Brendan Coles wrote a similar script in bash which runs whatweb in all ports - https://gist.github.com/798148


**Log Path**
Scan results can be found in logs/ folder. Result files are .nikto

