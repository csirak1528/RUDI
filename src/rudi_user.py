from rudi_defaults import dev_ip
from rudi_data import *

if not dev_ip in wlan_ips:
    wlan_ips.append(dev_ip)
    add_save_data("wlan_ips",wlan_ips)
    close()

