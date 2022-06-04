from netconf import NetConf as nf
from options import Options as opt
import xml.dom.minidom
import requests

class NetAuto(object):

    def __init__(self, netconf: nf, options: opt, webex_access_token: str, webex_room_id: str):
        self.netconf = netconf
        self.options = options
        self.state = False
        self.strbuffer = ""
        self.webex_access_token = webex_access_token
        self.webex_room_id = webex_room_id
        self.msg = ""
    
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
        self.msg = """
        CONFIGURATION NOTIFICATION:
        Target device: {}
        Changes: Banner motd
        Description: {}
        Note: This is an automated message.
        """.format(self.netconf.host, bmotd)
    
    def set_hostname(self):
        netconf_hn_start = """
        <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>"""
        netconf_hn_end = """</hostname>
        </native>
        </config>
        """
        hn = input("Enter hostname: ")
        netconf_hn = netconf_hn_start + hn + netconf_hn_end
        netconf_reply = self.netconf.manager.edit_config(target="running", config=netconf_hn)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
        self.msg = """
        CONFIGURATION NOTIFICATION:
        Target device: {}
        Changes: Hostname
        Description: {}
        Note: This is an automated message.
        """.format(self.netconf.host, hn)

    def set_loopback(self):
        netconf_loopback_number_start = """
        <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
        <Loopback>
            <name>"""
        netconf_loopback_number_end = """</name>
        """
        netconf_loopback_description_start = """<description>"""
        netconf_loopback_description_end = """</description>
        """
        netconf_loopback_address_start = """<ip>
        <address>
        <primary>
        <address>"""
        netconf_loopback_address_end = """</address>
        """
        netconf_loopback_mask_start = """<mask>"""
        netconf_loopback_mask_end = """</mask>
        </primary>
        </address>
        </ip>
        </Loopback>
        </interface>
        </native>
        </config>
        """
        loopback_number = input("Enter Loopback number: ")
        loopback_description = input("Enter Loopback description: ")
        loopback_address = input("Enter Loopback address: ")
        loopback_mask = input("Enter Loopback mask: ")
        netconf_loopback = netconf_loopback_number_start + loopback_number + netconf_loopback_number_end + netconf_loopback_description_start + loopback_description + netconf_loopback_description_end + netconf_loopback_address_start + loopback_address + netconf_loopback_address_end + netconf_loopback_mask_start + loopback_mask + netconf_loopback_mask_end
        netconf_reply = self.netconf.manager.edit_config(target="running", config=netconf_loopback)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
        self.msg = """
        CONFIGURATION NOTIFICATION:
        Target device: {}
        Changes: Loopback interface
        Description: Loopback{}, {}, IP:{}, mask:{}
        Note: This is an automated message.
        """.format(self.netconf.host, loopback_number, loopback_description, loopback_address, loopback_mask)

    def display_config(self):
        netconf_reply = self.netconf.manager.get_config(source="running")
        netconf_filter = """
        <filter>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
        </filter>
        """
        netconf_reply = self.netconf.manager.get_config(source="running", filter=netconf_filter)
        print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    def webex_notif(self):
        #WEBEX message
        access_token = self.webex_access_token
        room_id = self.webex_room_id
        url = 'https://webexapis.com/v1/messages'

        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
        }
        params = {'roomId': room_id, 'markdown': self.msg}
        res = requests.post(url, headers=headers, json=params)
        print(res.json())
        self.msg = ""