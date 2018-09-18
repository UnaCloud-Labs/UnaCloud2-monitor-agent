from urllib.request import urlopen


class NetworkUtils:

    def get_ip_addr(self):
        return urlopen('http://ip.42.pl/raw').read().decode("utf-8")
