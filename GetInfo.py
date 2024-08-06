import time
import random
import xml.etree.ElementTree as ET
import requests
import re
import hashlib


# username = "admin"
# password = "admin"
# Authrealm = "Highwmg"
# AuthQop = "auth"
# GnCount = 1
# proxies = {
#     'http': 'http://127.0.0.1:8080',
# }

class usa_wireless:

    def __init__(self):
        self.username = "admin"
        self.password = "admin"
        self.Authrealm = "Highwmg"
        self.AuthQop = "auth"
        self.GnCount = 1
        self.proxies = {
            'http': 'http://127.0.0.1:8080',
        }
        response = requests.get(url=login_url).headers # header获取nonce
        nonce = re.findall("nonce=\"(.*?)\"",str(response))[0]
        self.nonce = nonce
        rand = random.randrange(100001)
        date = int(time.time() * 1000)
        DigestRes_md5 = hashlib.md5()
        HA1_md5 = hashlib.md5()
        HA2_md5 = hashlib.md5()
        tmp_md5 = hashlib.md5()
        tmp_md5.update((str(rand) + "" + str(date)).encode('utf-8'))
        HA1_md5.update((self.username + ":" + self.Authrealm + ":" + self.password).encode('utf8'))
        HA2_md5.update(("GET" + ":" + "/cgi/xml_action.cgi").encode('utf8'))
        HA1 = HA1_md5.hexdigest()
        HA2 = HA2_md5.hexdigest()
        tmp = tmp_md5.hexdigest()
        AuthCnonce = tmp[:16]
        Authcount = ("0000000000" + hex(self.GnCount)[2:])[-8:]
        DigestRes_md5.update((HA1 + ":" + self.nonce + ":" + "00000001" + ":" + AuthCnonce + ":" + self.AuthQop + ":" + HA2).encode('utf-8'))
        DigestRes = DigestRes_md5.hexdigest()
        headers = {
            'Host': '192.168.1.1',
            'Authorization' : "Digest " + "username=\"" + self.username + "\", realm=\"" + "Highwmg" + "\", nonce=\"" + str(
            self.nonce) + "\", uri=\"" + "/cgi/xml_action.cgi" + "\", response=\"" + DigestRes + "\", qop=" + self.AuthQop + ", nc=" + Authcount + ", cnonce=\"" + AuthCnonce + "\""
            }
        status =  requests.get(url=login_url,headers=headers).status_code
        if status == 200:
            self.headers = headers
        else:
            print("登录失败")
            print(requests.get(url=login_url,headers=headers).headers)


    def get_status(self):

        response_xml = requests.get(url=get_statusinfo_url, headers=self.headers,proxies=self.proxies).text
        root = ET.fromstring(response_xml)
        wan_elem = root.find("wan")
        if wan_elem is not None:
            cellular_elem = wan_elem.find('cellular')
            if cellular_elem is not None:
               pdp_elem = cellular_elem.find('pdp_context_list')
               if pdp_elem is not None:
                   Item_elem = pdp_elem.find('Item')
                   if Item_elem is not None:
                       con_status = Item_elem.find('success')
                       if con_status.text == "1":
                            status = "up"
                       else:
                            status = "down"
        return status

    def restart_mifi(self):
        requests.get(url=restart_mifi_url, headers=self.headers)

    def restore_mifi(self):
        requests.get(url=restore_mifi_url, headers=self.headers)


    def enordis_net (self,data):

        rand = random.randrange(100001)
        date = int(time.time() * 1000)
        DigestRes_md5 = hashlib.md5()
        HA1_md5 = hashlib.md5()
        HA2_md5 = hashlib.md5()
        tmp_md5 = hashlib.md5()
        tmp_md5.update((str(rand) + "" + str(date)).encode('utf-8'))
        HA1_md5.update((self.username + ":" + self.Authrealm + ":" + self.password).encode('utf8'))
        HA2_md5.update(("POST" + ":" + "/cgi/xml_action.cgi").encode('utf8'))
        HA1 = HA1_md5.hexdigest()
        HA2 = HA2_md5.hexdigest()
        tmp = tmp_md5.hexdigest()
        AuthCnonce = tmp[:16]
        Authcount = ("0000000000" + hex(self.GnCount)[2:])[-8:]
        DigestRes_md5.update((HA1 + ":" + self.nonce + ":" + "00000001" + ":" + AuthCnonce + ":" + self.AuthQop + ":" + HA2).encode('utf-8'))
        DigestRes = DigestRes_md5.hexdigest()
        headers = {
            'Host': '192.168.1.1',
            'Authorization' : "Digest " + "username=\"" + self.username + "\", realm=\"" + "Highwmg" + "\", nonce=\"" + str(
            self.nonce) + "\", uri=\"" + "/cgi/xml_action.cgi" + "\", response=\"" + DigestRes + "\", qop=" + self.AuthQop + ", nc=" + Authcount + ", cnonce=\"" + AuthCnonce + "\""
            }
        "Digest " + "username=\"" + self.username + "\", realm=\"" + self.Authrealm + "\", nonce=\"" + self.nonce + "\", uri=\"" + "/cgi/xml_action.cgi" + "\", response=\"" + DigestRes + "\", qop=" + self.AuthQop + ", nc=" + Authcount + ", cnonce=\"" + AuthCnonce + "\""
        requests.post(url=enordis_net_url, headers=headers,data=data,proxies=self.proxies)

if __name__ == "__main__":
    mifi_ip = "192.168.1.1"
    input_ip = input("请输入你的mifiip地址,直接回车默认为192.168.1.1")
    if input_ip != "":
        mifi_ip = input_ip
    login_url = "http://" + mifi_ip + "/login.cgi"
    get_statusinfo_url = "http://" + mifi_ip + "/xml_action.cgi?method=get&module=duster&file=status1"
    get_dhcpstatusinfo_url = "http://" + mifi_ip + "/xml_action.cgi?method=get&module=duster&file=lan"
    change_dhcpip_url = "http://" + mifi_ip + "/xml_action.cgi?method=set&module=duster&file=lan"
    restart_mifi_url = "http://" + mifi_ip + "/xml_action.cgi?method=get&module=duster&file=reset"
    restore_mifi_url = "http://" + mifi_ip + "/xml_action.cgi?method=get&module=duster&file=restore_defaults"
    enordis_net_url = "http://" + mifi_ip + "/xml_action.cgi?method=set&module=duster&file=wan"
    enable_data="""<?xml version="1.0" encoding="US-ASCII"?> <RGW><wan><connect_disconnect>cellular</connect_disconnect></wan></RGW>"""
    disable_data="""<?xml version="1.0" encoding="US-ASCII"?> <RGW><wan><connect_disconnect>disabled</connect_disconnect></wan></RGW>"""
    flag = input("请选择功能，1 重启mifi ； 2 获取联网情况 ； 3 重置mifi ; 4 开启蜂窝网络 ； 5 关闭蜂窝网络")
    Usa_wireless1 = usa_wireless()
    if flag == "1":
        Usa_wireless1.restart_mifi()
        print("mifi正在重启")
    if flag == "2":
        status = Usa_wireless1.get_status()
        print("联网情况" + ":" + status)
    if flag == "3":
        status = Usa_wireless1.restore_mifi()
        print("mifi正在重置")
    if flag == "4":
        status = Usa_wireless1.enordis_net(enable_data)
        print("mifi将开启网络连接")
    if flag == "5":
        Usa_wireless1.enordis_net(disable_data)
        print("mifi将关闭网络连接")






