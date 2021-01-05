import datetime
import subprocess
from scapy.sendrecv import AsyncSniffer
from scapy.all import TCP, UDP, IP

class Sniffer:

    def __init__(self, interface, excluded_ips, store) -> None:
        self.interface = interface
        self.excluded_ips = excluded_ips
        self.__store = store
        self.__open_ports = self.__run_command_os("sudo lsof -i -n -P | grep LISTEN | awk '{print $9}' | awk -F: '{print $2}'")
        self.__ip_interface = self.__run_command_os("ip add show " + self.interface + " | grep 'inet' | awk '{print $2}' | awk -F/ '{print $1}'")
        self.__sniff =  AsyncSniffer(iface=self.interface, prn=self.__pkt_callback, store=False)
        self.__sniff.start()

    def __run_command_os(self, cmd) -> tuple:
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        return tuple(set(str(ps.communicate()[0])[2:-3].split('\\n')))

    def __pkt_callback(self, pkt) -> None:
        if (IP in pkt):
            if (pkt.haslayer(TCP) or pkt.haslayer(UDP)) and (str(pkt.dport) not in self.__open_ports) and (pkt[IP].dst in self.__ip_interface) and (pkt[IP].src not in (self.excluded_ips)):
                event = {"time": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f"), "ip_addr_src": pkt[IP].src, "ip_addr_dst": pkt[IP].dst, "port_src": pkt.sport, "port_dst": pkt.dport, "transport_protocol_flag": str(pkt[TCP].flags.value) if TCP in pkt else "None"}
                self.__store.write(event)
    
    def start(self) -> None:
        self.__sniff.start()

    def stop(self) -> None:
        self.__sniff.stop()
