import requests
import urllib
import time
from collections import Counter
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request

def checkdup(lista):
    if len(lista)==len(set(lista)):
        return False
    else:
        return True


def webcrawl(url,avail_url,visited):
    visited.append(url)
    count=0
    try:
        code = requests.get(url)
        ## return response 200 if success
        #visited.append(url)
        plain = code.text
        ## return source code
        s = BeautifulSoup(plain, "html.parser")
        
        for x in s.findAll('a'):
            links = x.get('href')
            if(links.startswith('http')and 'sfu.ca' in links and links not in avail_url):
                count=count+1
                avail_url.append(links)
                #print (links)
            elif(links.startswith('/')):
                links='http://www.sfu.ca'+links
                if(links not in avail_url):
                    count=count+1
                    avail_url.append(links)
                    #print(links)
    except:
        pass
    print("total new url obtained in page:",count)
    return avail_url


def selectnexturl(avail_url,common,visited):
    count=0
    commonwordcount=0
    ret=''
    for i in avail_url:
        parsedurl=urllib.parse.urlparse(i)
        if parsedurl[1] == 'www.sfu.ca' and parsedurl[2]!='':
            count=count+1
            word=parsedurl[2].split('/')[1]
            common.append(word)
    common_word=Counter(common).most_common()
    # print(common_word[1][0])

    while ret=='' and commonwordcount!=len(common_word):
        for i in range(len(avail_url)):
            #print("visited",visited)
            #print(avail_url[i])
            if (avail_url[i].startswith("http://www.sfu.ca/"+common_word[commonwordcount][0])) and (avail_url[i] not in visited):
                ret=avail_url[i]
                #print(ret)
                return ret
        
        if(ret==''):
            commonwordcount=commonwordcount+1

    
    return ret


def html_download(url):
    html = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    file_name=url.replace('/','_')
    file_name=file_name[7:len(url)]
    webpage = str(urlopen(html).read())
    FILE = open(file_name, 'w+') 
    FILE.write(webpage)
   




"""Main crawler"""
avail_url=[]
visited=[]
common=[]
i=0
url='http://www.sfu.ca/computing/people/faculty.html'
print(url)
webcrawl(url,avail_url,visited)
print("First ten pages obtained:",avail_url[0:10])
print("----------------------------------")
html_download(url)
time.sleep(5)
while i<9:
    res=selectnexturl(avail_url,common,visited)
    webcrawl(res,avail_url,visited)
    html_download(res)
    print(res)
    time.sleep(5)
    i+=1;
print("----------------------------------")
print("total sites visited:")
print(visited)
print("----------------------------------")
print("total url obtained",len(avail_url))

result = checkdup(avail_url)
result1 = checkdup(visited)
if result or result1:
    print("There are duplicates in both url list")
else:
    print("There are no duplicates in both url list")

