import requests
import random
import re
import string
import time
from bs4 import BeautifulSoup
import requests


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
#
# def WriteIPadress():
#     all_url = [] # 存储IP地址的容器
#     # 代理IP的网址
#     url = "http://api.xicidaili.com/free2016.txt"
#     r = requests.get(url=url)
#     all_url = re.findall("\d+\.\d+\.\d+\.\d+\:\d+",r.text)
#     with open("C:\\Users\\youya\\PycharmProjects\\fun\\ip.txt",'w') as f:
#         for i in all_url:
#             f.write(i)
#             f.write('\n')
#     return all_url
# count = 0 # 计数器
#
# while count < 4000:
#     all_url = WriteIPadress()
#     for i in all_url:
#         proxies = {"http": i}
#         try:
#             r = requests.get(url=url,  headers=headers, proxies=proxies)
#             if(r.json()['flag'] == True):
#                 count += 1
#                 print("成功投票%d次！" % (count))
#             print(r.json())
#         except Exception as reason:
#             print("错误原因是：",reason)

def down_ip_list():
    proxy=get_proxy()
    ip_lists=[]
    page=0
    headers = {  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36' }

    while True:
        num_proxy=0
        while True:
            print (len(ip_lists))
            url = "http://www.xicidaili.com/nn/" + str(page)
            web_data = requests.get(url=url, headers=headers,proxies=proxy)
            soup = BeautifulSoup(web_data.text, "lxml")
            ips = soup.find_all('tr')
            num_proxy+=1
            for i in range(2, len(ips)):
                ip_info = ips[i]
                tds = ip_info.find_all('td')
                ip_lists.append(( tds[5].text,tds[1].text + ":" + tds[2].text))
            if not len(ip_lists)==0:
                break
        page+=1
        if len(ip_lists)>8000:
            break
    with open("C:\\Users\\youya\\PycharmProjects\\fun\\ip1.txt",'rw') as f:
        for i in ip_lists:
            f.write(i[0]+'@'+i[1])
            f.write('\n')
    f.close

def get_vote_num(proxies=None):
    votes_url='https://hrapi.shixiseng.com/api/rp/participant/internship?participant_uuid=rp_geuervsvynmi'
    if proxies is None:
        r = requests.get(votes_url)
    else:
        r = requests.get(votes_url,proxies=proxies)
    soup = BeautifulSoup(r.text, "html5lib")
    text = soup.prettify()
    num_=text.find('votes')
    vote_num=int(text[num_+7:num_+13])
    return vote_num

def get_proxy():
    ip_lists=[]
    with open("C:\\Users\\youya\\PycharmProjects\\fun\\ip.txt",'r') as f:
        ip_list=f.readlines()
        for i in ip_list:
            ipList={i.split('@')[0]:i.split('@')[1][:-1]}
            ip_lists.append(ipList)
    f.close()
    return ip_lists

if __name__ == "__main__":
    down_ip_list()
    ip_lists=get_proxy()
    max_vote=len(ip_lists)
    ip_useful_list = []
    error_count=0
    success_count=0
    count = 0
    begin_num=get_vote_num()
    print ("当前票数：",begin_num)
    random.shuffle(ip_lists)
    for i in range(max_vote):
        last_success_count=success_count

        try:
            proxy = ip_lists[i]
            print (proxy.keys(),proxy[proxy.keys()])
            for j in range(10):
                r = requests.get(url=url,  headers=headers, proxies=proxy)
                random_wait_time = random.random()*3
                time.sleep(random_wait_time)
                if(r.json()['msg'] == 'success'):
                    success_count += 1
        except Exception:
            error_count += 1
        else:
            if ip_useful_list.count(proxy)==0:
                ip_useful_list.append(proxy)
                with open("C:\\Users\\youya\\PycharmProjects\\fun\\ip_useful_list.txt",'w') as f:
                    for key in proxy:
                        f.write(key,proxy[key])
                        f.write('\n')
                f.close()
        now=get_vote_num(ip_lists[i])
        print (i,"当前票数：",now,"成功投票：",now-begin_num)
        random_wait_time = random.random()*7
        time.sleep(random_wait_time)
