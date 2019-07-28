# -*- coding: utf-8 -*-
"""
Created on Wed May 22 12:01:55 2019

@author: ao.semenov
"""

'https://hidemyna.me/en/proxy-list/?type=s#list'

import requests
#from bs4 import BeautifulSoup



#print(r.encoding)
#print(r.text)

#driver = BeautifulSoup(r.text, 'html.parser')
#tag_for_me = driver.find_elements_by_class_name('div')
#print (tag_for_me)
def ParseNewProxies():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

    url = 'https://www.proxynova.com/proxy-server-list/' # url для второй страницы
    r = requests.get(url, headers = headers)   
    r.encoding = 'cp1251'

    ProxysTxt=''
    with open('test.html', 'w') as site:
        script=str(r.text)
        i=0
        while len(script)>i:
    
            site.write(script)
            try:
                index = script.index('<abbr title="') 
            except:
                break
    
            proxyUrl=script[index+13:index+13+script[index+13:].index('"')]
            i=index+script[index+13:].index('"')
            script=script[i:]                    
            try:
                portStart = script.index('proxies">') 
                port=script[portStart+9:portStart+9+script[portStart+9:].index('<')]
                FullProxy=str(proxyUrl)+':'+str(port) 
                if not FullProxy.upper().isupper(): 
    #                print(FullProxy)
                    ProxysTxt=str(ProxysTxt)+str(FullProxy)+'\n'
            except:     
                break
            
    FilePath=r'\\kari.local\public\all\For Office\Semenov\Telegram\ProgFiles\Proxy.txt'
    ProxyFile = open(FilePath,"w")  
    ProxyFile.write(ProxysTxt)
    ProxyFile.close()
#    


