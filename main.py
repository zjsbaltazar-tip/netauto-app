from netconf import NetConf as nf
from netauto import NetAuto as na
from options import Options as opt
from configparser import ConfigParser as conf

if __name__ == "__main__":
    parser = conf()
    parser.read("conf.cfg")
    netconf = nf(
        host=parser.get("NETCONF", "host"), 
        port=parser.getint("NETCONF", "port"), 
        username=parser.get("NETCONF", "username"), 
        password=parser.get("NETCONF", "password"),
        hostkey_verify=parser.getboolean("NETCONF", "hostkey_verify")
    )
    options = opt()
    options += ("banner", "Banner MOTD")
    options += ("hostname", "Hostname")
    options += ("loopback", "Loopback")
    options += ("config", "View Config")
    options += ("exit", "Exit")
    webex_access_token = parser.get("WEBEX", "access_token")
    webex_room_id = parser.get("WEBEX", "room_id")
    netauto = na(netconf, options, webex_access_token, webex_room_id)
    netauto.init()