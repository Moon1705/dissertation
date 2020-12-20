import json
import datetime
import subprocess
from scapy.sendrecv import AsyncSniffer
from scapy.all import TCP, UDP, IP

class Sniffer():

    def __init__(self, interface, store) -> None:
        self.interface = interface
        self.status = False
        self.sniff =  AsyncSniffer(iface=self.interface, prn=self.__pkt_callback, store=False)
        self.store = store
        self.__take_open_ports()
        self.__take_ip_interface()

    def __run_command_os(self, cmd) -> tuple:
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        return tuple(set(str(ps.communicate()[0])[2:-3].split('\\n')))

    def __take_open_ports(self) -> None:
        cmd = "sudo lsof -i -n -P | grep LISTEN | awk '{print $9}' | awk -F: '{print $2}'"
        self.open_ports = self.__run_command_os(cmd)

    def __take_ip_interface(self) -> None:
        cmd = "ip add show " + self.interface + " | grep 'inet' | awk '{print $2}' | awk -F/ '{print $1}'"
        self.ip_interface = self.__run_command_os(cmd)

    def __pkt_callback(self, pkt) -> None:
        if (IP in pkt):
            if (pkt.haslayer(TCP) or pkt.haslayer(UDP)) and (str(pkt.dport) not in self.open_ports) and (pkt[IP].dst in self.ip_interface):
                event = {"time": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f"), "packer_size": len(pkt), "mac_addr_src": pkt.src, "mac_addr_dst": pkt.dst, "ip_addr_type": f"IPv{pkt[IP].version}", "ip_addr_src": pkt[IP].src, "ip_addr_dst": pkt[IP].dst, "port_src": pkt.sport, "port_dst": pkt.dport, "transport_protocol_flag": pkt[TCP].flags.value if TCP in pkt else ""}
                self.store.write(json.dumps(event))                 
    
    def start(self) -> None:
        self.sniff.start()
        self.status = True

    def stop(self) -> None:
        self.sniff.stop()
        self.status = False

    def restart(self) -> None:
        self.sniff.stop()
        self.sniff.start()
        self.status = True

    def status(self) -> bool:
        return self.status

