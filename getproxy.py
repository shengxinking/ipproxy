#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urlparse
from bs4 import BeautifulSoup

"""
IP struct:
    ip = {
        "ip": "127.0.0.1",
        "port": "8888",
        "info": "XXXXX",
        "t": 1,     # type, 1: 透明, 2: 匿名, 3: 高匿名
        "p": 150,   # ping, 延时 ms
    }

"""

class Base:

    ips = []
    timeout = 5

    def ping(self):
        for ip in self.ips:
            if self._ping(ip["ip"], ip["port"]):
                pass

    def _ping(self, ip, port):
        url = "http://www.baidu.com"
        proxies = {
            "http": "http://%s:%s" % (ip, port),
        }
        try:
            r = requests.get(url, proxies=proxies, timeout=self.timeout)
            if r.status_code == requests.codes.ok:
                return True
        except:
            pass

        return False


    def wredis(self, key):
        pass

class CZ88(Base):
    """ http://www.cz88.net/proxy/http_2.shtml

    """
    base = "http://www.cz88.net/proxy/"

    def get(self):
        self._get("index.shtml")
        for i in range(2, 11):
            self._get("http_%d.shtml", i)

    def _get(self, page):
        page = "http_10.shtml"
        url = urlparse.urljoin(self.base, page)
        r = requests.get(url)
        r.encoding = "GBK"
        if r.status_code != requests.codes.ok:
            print "requests get error!"
            return

        soup = BeautifulSoup(r.text)
        soup = soup.find("div", id="boxright").find_all("li")
        keys = ["ip", "port", "t", "info"]
        for s in soup[1:]:
            ip = {}
            i = 0
            for d in s.stripped_strings:
                ip[keys[i]] = d
                i += 1

            print ip
            self.ips.append(ip)



# http://blog.kuaidaili.com/
def get_kuaidaili():
    pass

# http://www.ip002.com/
def get_ip002():
    pass


def main():
    cz88 = CZ88()
    cz88.get()

if __name__ == "__main__":
    url = "http://cn.bing.com"
    proxies = {
        "http": "http://111.13.136.45:80",
    }
    r = requests.get(url, proxies=proxies, timeout=300)
    print r.status_code
    print r.text
    if r.status_code == requests.codes.ok:
        print r.text
    # main()