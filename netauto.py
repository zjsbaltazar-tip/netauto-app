from netconf import NetConf as nf
from options import Options as opt
import xml.dom.minidom
import requests

class NetAuto(object):

    def __init__(self, netconf: nf, options: opt):
        self.netconf = netconf
        self.options = options
        self.state = False
        self.strbuffer = ""
    
    def init(self):
        self.state = True
        self.options.connect("banner", self.set_banner_motd)
        self.options.connect("hostname", self.set_hostname)
        self.options.connect("loopback", self.set_loopback)
        self.options.connect("config", self.display_config)
        self.options.connect("exit", self.exit)
        self.run()

    def display_options(self):
        self.strbuffer += "Available Options:\n"
        for index, value in enumerate(self.options.getall().values()):
            self.strbuffer += f"{index+1}.) {value[0]}"
            if index < len(self.options.getall())-1:
                self.strbuffer += "\n"
        print(self.strbuffer)
        self.strbuffer = ""

    def run(self):
        while self.state:
            self.display_options()
            select = input("Select an option [1-{}]: ".format(len(self.options.getall())))
            try:
                key = list(self.options.getall().keys())[int(select)-1]
            except:
                key = None
            if key is not None:
                self.options.trigger(key)
            else:
                print("Invalid input!")

    def exit(self):
        self.state = False

    def set_banner_motd(self):
        netconf_bmotd_start = """
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <banner>
            <motd>
            <banner>"""
        netconf_bmotd_end = """</banner>
        </motd>
        </banner>
        </native>
        </config>
        """
        bmotd = input("Banner motd: ")
        netconf_bmotd = netconf_bmotd_start + bmotd + netconf_bmotd_end
        netconf_reply = self.netconf.manager.edit_config(target="running", config=netconf_bmotd)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
    
    def set_hostname(self):
        pass

    def set_loopback(self):
        pass

    def display_config(self):
        # Current device configuration
        netconf_reply = self.netconf.manager.get_config(source="running")
        # Print device config
        netconf_filter = """
        <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
        </filter>
        """
        netconf_reply = self.netconf.manager.get_config(source="running", filter=netconf_filter)
        # Print YANG config
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())