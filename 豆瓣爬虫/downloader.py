# _*_ coding:utf-8 _*_
import requests 
import random
import lxml.html
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker
import time 
import threading

engine = create_engine('mysql+pymysql://root@localhost:3306/film?charset=utf8',echo=True)
Base = declarative_base()

class Film(Base):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    filmname = Column(String(64), nullable=False, index=True)
    filmscore = Column(Float, nullable=False)
    contentnum = Column(Integer, nullable=False)
    def __repr__(self):
        return '%s(%r)'% (self.__class__.__name__, self.username)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_data(filmname, filmscore,contentnum):
    filmname = filmname
    filmscore = filmscore
    contentnum = contentnum
    film = Film(filmname=filmname,
                filmscore=filmscore,
                contentnum=contentnum)
    session.add(film)



USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

headers = {}

#获取代理
def get_proxy():
    proxy_result = requests.get("http://127.0.0.1:8080/").json()
    proxy_data = proxy_result['data']
    proxy_list = []
    for proxy in proxy_data:
        type_ = proxy['type']
        ip_ = proxy['type']+'://'+ proxy['ip_and_port']
        dict_ = {}
        dict_[type] = ip_
        proxy_list.append(dict_)
    return proxy_list

# def downloader(proxy=None, url=None):
# 	proxy = proxy 
# 	response = requests.get(url, proxies=proxy, headers=headers)
# 	return response

def downloader(proxy=[], url=None,user_agent=[],num_retries=3):
    if user_agent:
        headers = {}
        headers['headers'] = random.choice(user_agent)
    if proxy:
        proxies = random.choice(proxy)
    data1 = requests.get(url, proxies=proxies, headers=headers)
    # html = response.html
    data1.status_code
    if data1.status_code != 200:
        return None
    # except Exception as e:
    #     print('Download error:', str(e))
    #     html = ''
    #     # html = ''
    #     # if num_retries > 0 and code1 < 600 and code1 >= 500:
    #     # 	downloader(proxy,url,user_agent,num_retries-1)
    return data1
      




#数据提取并存储
def get_data_save(resp):
    response = resp
    html = response.content
    html = lxml.html.fromstring(html)
    for i in range(1,21):
        name = html.xpath("/html/body/div[3]/div[1]/div/div[1]/div[2]/table[%d]//a/text()"%i)
        name = [ str1.strip() for str1 in name if str1.strip() != '']
        film_name = name[0][0:-2].strip()
        film_score = html.xpath("/html/body/div[3]/div[1]/div/div[1]/div[2]/table[%d]//span[@class='rating_nums']/text()"%i)
        if not film_score:
            film_score=0
        else:
            film_score = float(film_score[0])
        content_num = html.xpath("/html/body/div[3]/div[1]/div/div[1]/div[2]/table[%d]//span[@class='pl']/text()"%i)
        if not content_num:
            content_num = 0
        else:
            content_num = int(content_num[0][1:-4])
        add_data(film_name,film_score,content_num)
    try:
        session.commit()
    except:
        session.rollback()
        raise


    
#编码转换
def de_code(str1):
    str1 = str1
    return str1.encode('utf-8').decode('utf-8')

#提取电影所属国家，主演
# def get_data(film):
#     film = film
#     list2 = film[0].split('/')
#     film_country = list2[0].strip().split('(')[1][0:-1]
#     for film_str in list2:
#         if not film_str.strip().startswith('20'):
#             film_actor = film_str.strip()
#             break
#     return film_country, film_actor



def threaded_crawler(url_list, proxy_list, user_agent, max_threads=5):
    url_list = url_list
    proxy_list = proxy_list
    user_agent = user_agent
    
    #downloader(proxy=[], url=None,user_agent=[],num_retries=3):
    def process_queue():
        while url_list:
            url = url_list.pop()
            response1 = downloader(proxy=proxy_list,
                                  user_agent=user_agent,
                                  url=url)
            if response1.status_code != 200:
                break
            else:
                get_data_save(response1)
                time.sleep(3)

    threads = []
    while threads or url_list:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and url_list:
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(1)

if __name__ == "__main__":
    url_list = []
    for i in range(50):
        http_ = "https://movie.douban.com/tag/2015?start=%d&type=S"%(i*20)
        url_list.append(http_)
    for i in range(50):
        http_ = "https://movie.douban.com/tag/2014?start=%d&type=S"%(i*20)
        url_list.append(http_)
    for i in range(50):
        http_ = "https://movie.douban.com/tag/2013?start=%d&type=S"%(i*20)
        url_list.append(http_)
    proxy_list = get_proxy()
    user_agent = USER_AGENT_LIST
    threaded_crawler(url_list, proxy_list, user_agent)
    session.close()





