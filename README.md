# krypton_mitm
this is my first script. this is a man in the middle i made.. malay languege

support kali linux only!!

require:
python3
python3-pip
scapy
wifi adapter

how to install the script and run it:

sudo apt update && apt upgrade -y

sudo apt install python3 python3-pip  -y

sudo pip3 install scapy

git clone https://github.com/kryptonproject/krypton_mitm

cd krypton_mitm

sudo python3 krypton_mitm.py -ip_range local_ip/10




if you wanna find a local ip on your wifi use this command:
arp-scan --interface=wlan0 -l
and pick the device local ip that you wanna mitm attack

MAKE SURE YOUR WIFI ADAPTER IS CONNECTED TO YOUR VIRTUALBOX AND THE WIFI
auth:krypton
thanks to: david bombal, 177member, stucx team, myopecs. (thanks to them for teaching me about hacking and programming)

WARNING:EDUCATIONAL PURPOSES ONLY, IF YOU USE THE SCRIPT FOR THE BAD THING.. IM GOING TO FIND YOU!!!
