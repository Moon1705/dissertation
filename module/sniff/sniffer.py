from redis import Redis
from scapy.sendrecv import AsyncSniffer
from scapy.all import TCP, UDP, IP
from datetime import datetime


class Sniff():

    def __init__(self, iface='eth0'):
        self.iface = iface

    def __pkt_callback(self, pkt):
        protocols = (TCP, UDP)
        for protocol in protocols:
            if pkt.haslayer(protocol):
                flag = ""
                if protocol == TCP:
                    flag = pkt[protocol].flags.value
                pkt_json = {"time": datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f"), "packer_size": len(pkt[protocol]), "mac_addr_src": pkt.src, "mac_addr_dst": pkt.dst, "ip_addr_type": f"IPv{pkt[IP].version}", "ip_addr_src": pkt[IP].src, "ip_addr_dst": pkt[IP].dst, "transport_protocol_type": str(protocol)[-5:-2], "port_src": pkt.sport, "port_dst": pkt.dport, "transport_protocol_flag": flag}
                self.db.mset(pkt_json)
    
    def create_redis(self, hostname='localhost', port_access='6379', dbname=0, password_db=None):
        self.db = Redis(host=hostname, port=port_access, db=dbname, password=password_db)

    def start(self):
        self.sniff = AsyncSniffer(iface=self.iface, prn=self.__pkt_callback, store=False)
        self.sniff.start()

    def stop(self):
        self.sniff.stop()
