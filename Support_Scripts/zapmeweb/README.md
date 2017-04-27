This script utilizes the script from the tellmeweb created by YGN Ethical Hacker Group, Yangon, Myanmar. It modifies it to use **ZAP** on multiple websites

**Description**
The zapmeweb takes gnmap outpout (-oG) generated together with -sV option. It takes all hosts with http & https ports open. Then it feeds them into zap

**Background**
ZAP is excellent Vulnerability scanner for websites. When performing PTs over large array of IPs in tight deadline, recon must be done as fast as possible via automation.


**ZAP-Me-Web : Automating ZAP from NMap output**

The ZAP-me-web takes nmap output in Grepable format (-oG) generated together with -sV option. It extracts all hosts with http & https ports open. Then it feeds them into ZAP. 

**Log Path**

Scan results can be found in logs/ folder. Result files are separated per each IP per port with .session and .alerts different folders extension.


**How to configure**
Just run the ZAP tool as a proxy server with on the port 8080 and configured in the zapmeweb.config. You would also have to install zap-cli.
