# version 0.1
# 个人练习用
# 依赖弹幕分析 视频的精彩部分
# 此版本暂不支持历史弹幕，及分P弹幕，分P弹幕的弹幕地址为CID+1
# ranking
#ajax地址get:https://www.bilibili.com/index/rank/rookie-0-0.json
#ajax地址get:https://www.bilibili.com/index/rank/rookie-1-0.json
#ajax地址get:https://www.bilibili.com/index/rank/rookie-2-0.json
#ajax地址get:https://www.bilibili.com/index/rank/rookie-3-0.json

#https://api.bilibili.com/archive_stat/stat?callback=jQuery172013511373787340042_1499097829747&aid=11792413&type=jsonp&_=1499097830407

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

import logging


def transTimeToString(n):
    hour=n/3600
    remain_minute=n%3600
    minute = remain_minute / 60
    second = remain_minute % 60
    string = ('%d时 %d分 %d秒'%(hour,minute,second))
    return string

class danmu_spider():
    
        
    aurl = 'http://www.bilibili.com/video/av'
    curl = 'http://comment.bilibili.com/%s.xml'
    count_url='https://api.bilibili.com/archive_stat/stat?callback=jQuery172013511373787340042_1499097829747&aid=%s&type=jsonp&_=1499097830407'
    exist = False
             
    def __init__(self, av):
        self.av = av
        self.html = requests.get(self.aurl + str(self.av))
        
        self.soup = BeautifulSoup(self.html.text, 'html.parser')
        if self.soup.find_all(class_='player'):
            self.exist = True
            self.title = self.soup.find('h1').get_text()
            self.author = self.soup.find_all('meta')[3]['content']

            
            script=self.soup.find_all('script')[14]
            ppp=re.compile(r'cid=\d+')
            self.cid = re.search(ppp,script.text).group(0).split('=')[1]
            self.danmus = requests.get(self.curl%self.cid).text.split(r'</d>')
        else:
            return None

    def getData(self):
        r=requests.get(self.count_url%self.av)
        raw_data=r.text.split(',')[2:]
        datas={}
        for d in raw_data:
            name,data=d.split(':')
            name=name.strip('"')
            datas[name]=data
        rank_data={}
        rank_data['coverImg']=self.coverImg()
        rank_data['title']=self.title
        rank_data['author']=self.author
        rank_data['playCount']=datas['view']
        rank_data['danmuCount']=datas['danmaku']
        return rank_data
    
    def coverImg(self):
        try:
            img=self.soup.find('img',class_='cover_image').attrs['src']
        except Exception as e:
            logging.exception(e)
            return None
        return img

    def show_top(self,n=10,mode='web'):
        fenbu=[]
        for danmu in self.danmus[1:]:
            time = danmu[8:].split(',')[0]

            try:
                time=int((float(time))/10)
                if time < 2:
                    continue
                fenbu.append(float(time))
            except Exception as e:
                logging.exception(e)
                pass
        c = Counter()
        for i in fenbu:
            c[i]+=1
        dlist = c.most_common()
        dlist.sort(key = lambda x:x[1],reverse=True)
        top_n = c.most_common(n)
        if mode == 'web':            
            results=[]
            for enum,top in enumerate(top_n): #result= ['enumerate','time_start','time_end','danmu_count']
                result=[(enum+1),transTimeToString(top[0]*10),transTimeToString((top[0]+1)*10),top[1]]
                results.append(result)
            return results    
             
        elif mode == 's':
            string=''
            for top in top_n:
                
                string += ('%d---%d s have %d danmu <br>'%(top[0]*10,(top[0]+1)*10,top[1]))
            return string
'''
import numpy as np
import matplotlib.pyplot as plt
#todo: 弹幕中抢第一的无意义弹幕占了重比例，所以要进行弹幕清洗
def danmu_fenbu_show(danmu):
    fenbu=[]
    for danmu in self.danmus[1:]:
        time = danmu[8:].split(',')[0]
        try:
            fenbu.append(float(time))
        except Exception:
            pass

    danmu_fenbu = np.array(danmu.fenbu)
    plt.hist(danmu_fenbu,round(max(fenbu)/10))
    plt.savefig(r'E:/flask/static/images/av.jpg')
    plt.show()
##
'''
if __name__ == '__main__':
    bd=danmu_spider(11792413)
    x=bd.getData()
