from ncclient import manager as m

# Network Configuration
class NetConf(object):

    def __init__(self, host: str, port: int, username: str, password: str, hostkey_verify=False):
        self.manager = m.connect(
            host=host, port=int(port),
            username=username, password=password,
            hostkey_verify=bool(hostkey_verify)
        )

    