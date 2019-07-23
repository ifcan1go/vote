__author__ = 'changchang.cc'
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import http.client
import threading
from lxml import etree

inFile = open('proxy.txt')
outFile = open('verified.txt', 'w')
lock = threading.Lock()


def get_content_list(html_str):
    content_list = []
    html = etree.HTML(html_str)
    tr_list = html.xpath('//div[@id="list"]/table/tbody/tr')
    for tr in tr_list:
        item = {}
        item["ip"] = tr.xpath('./td[1]/text()')[0]
        item["port"] = tr.xpath('./td[2]/text()')[0]
        content_list.append(item)
    return content_list

def getProxyList(targeturl="http://www.xicidaili.com/nn/"):
    countNum = 0
    ip_list = []
    proxyFile = open('proxy.txt', 'a')

    requestHeader = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    kuaidaili_urls=["https://www.kuaidaili.com/free/inha/%d/" % i for i in range(1, 100)]
    kuaidaili_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, ",  # auto delete br encoding. cos requests and scrapy can not decode it.
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": (
            "Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1562386551; "
            "Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1562386476; "
            "_ga=GA1.2.2146346282.1562386476; "
            "_gat=1; "
            "_gid=GA1.2.1536217319.1562386476; "
            "channelid=0; "
            "sid=1562386470339940; "
        ),
        "Host": "www.kuaidaili.com",
        "Referer": "https://www.kuaidaili.com/free/inha/1/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    for page in range(1, 20):
        url = targeturl + str(page)
        # print url
        req = requests.get(url, headers=requestHeader)
        html_doc = req.text

        soup = BeautifulSoup(html_doc, "html.parser")
        # print soup
        trs = soup.find('table', id='ip_list').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            ip = tds[1].text.strip()
            port = tds[2].text.strip()
            protocol = tds[5].text.strip()
            ip_list.append((ip,port,protocol))
            countNum += 1
    content_lists=[]
    for url in kuaidaili_urls:
        html_str = requests.get(url,headers=kuaidaili_headers).content.decode()
        content_list = get_content_list(html_str)
        content_lists.extend(content_list)
    for ip in content_lists:
        ip_list.append((ip["ip"], ip["port"], 'HTTP'))
    ip_list=list(set(ip_list))
    for ip_ in ip_list:
        ip,port,protocol=ip_
        proxyFile.write("None|%s|%s|None|None|%s|None|None" % (ip,port,protocol))
        print('%s=%s:%s' % (protocol, ip, port))
    proxyFile.close()
    return countNum


def verifyProxyList():
    '''
    验证代理的有效性
    '''
    requestHeader = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    myurl = 'https://rp.shixiseng.com/'

    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.split('|')
        protocol = line[5]
        ip = line[1]
        port = line[2]

        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5.0)
            conn.request(method='GET', url=myurl, headers=requestHeader)
            res = conn.getresponse()
            lock.acquire()
            print("+++Success:" + ip + ":" + port)
            outFile.write(ll + "\n")
            lock.release()
        except:
            print("---Failure:" + ip + ":" + port)


if __name__ == '__main__':
    # tmp = open('proxy.txt' , 'w')
    # tmp.write("")
    # tmp.close()
    #
    # proxynum = getProxyList("http://www.xicidaili.com/nn/")
    # print (u"国内高匿：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/nt/")
    # print (u"国内透明：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wn/")
    # print (u"国外高匿：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wt/")
    # print (u"国外透明：" + str(proxynum))

    print(u"\n验证代理的有效性：")

    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()

    for t in all_thread:
        t.join()

    inFile.close()
    outFile.close()
    print("All Done.")
