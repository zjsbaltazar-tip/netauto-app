from netconf import NetConf as nf
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