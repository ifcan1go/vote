# -*- coding: utf-8 -*-
import random
import time
from bs4 import BeautifulSoup
import requests
import threading

num_thread=10

url = 'https://hrapi.shixiseng.com/api/rp/participant/vote?participant_uuid=rp_geuervsvynmi'
headers = {'Accept': 'application/json, text/plain, */*',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-US,en;q=0.5',
           'Connection': 'keep-alive',
           'Content-Type': 'Content-Type',
           'Host': 'hrapi.shixiseng.com',
           'Origin': 'https://rp.shixiseng.com',
           'Referer': 'https://rp.shixiseng.com/mrp.html',
           'TE': 'Trailers',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0', }


def get_vote_num(proxies=None):
    votes_url = 'https://hrapi.shixiseng.com/api/rp/participant/internship?participant_uuid=rp_geuervsvynmi'
    if proxies is None:
        r = requests.get(votes_url)
    else:
        r = requests.get(votes_url, proxies=proxies)
    soup = BeautifulSoup(r.text, "html5lib")
    text = soup.prettify()
    num_ = text.find('votes')
    vote_num = int(text[num_ + 7:num_ + 13])
    return vote_num


def get_proxy():
    ip_lists = []
    with open('verified.txt', 'r', encoding='UTF-8') as f:
        ips = f.readlines()
        for i in ips:
            ip = (i.split("|")[1])
            port = (i.split("|")[2])
            protocol = (i.split("|")[5])
            ipList = {protocol: ip + ":" + port}
            ip_lists.append(ipList)
    f.close()
    return ip_lists


def vote(proxy):
    for j in range(10):
        r = requests.get(url=url, headers=headers, proxies=proxy)
        random_wait_time = random.random() * 2
        time.sleep(random_wait_time)
        now = get_vote_num(proxy)
        print(proxy,"当前票数：", now)


if __name__ == "__main__":
    ip_lists = get_proxy()
    max_vote = len(ip_lists)
    begin_num = get_vote_num()
    print("当前票数：", begin_num)
    random.shuffle(ip_lists)
    for nn in range(int(max_vote / num_thread)):
        threads = []
        for i in range(min(num_thread, max_vote - nn * num_thread)):
            t = threading.Thread(target=vote, args=(ip_lists[nn * num_thread + i],))
            threads.append(t)
        for i in range(min(num_thread, max_vote - nn * num_thread)):
            t=threads[i]
            t.start()
        for i in range(min(num_thread, max_vote - nn * num_thread)):
            t = threads[i]
            t.join()
        random_wait_time = random.random() * 10
        time.sleep(random_wait_time)
    now = get_vote_num()
    print("当前票数：", now, "成功投票：", now - begin_num)
