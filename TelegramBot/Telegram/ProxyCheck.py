# -*- coding: utf-8 -*-
"""
Created on Wed May 22 09:46:50 2019

@author: ao.semenov
"""
import os
import requests


def GetProxy():
    FilePath=r'\\kari.local\public\all\For Office\Semenov\Telegram\ProgFiles\Proxy.txt'
    ProxyFile = open(FilePath,"r")
    ProxyList = [line.rstrip('\n') for line in ProxyFile]
    ProxyFile.close()
    if len(ProxyList)>0:
        return('https://'+str(ProxyList[0]))
    else:
        return('прокси кончились') 

def ProxyCheck():   
    proxy=GetProxy()
    if proxy!='прокси кончились':
        session = requests.session()
        session.proxies = {}
        session.proxies['https'] = proxy  
        send_text = """https://api.telegram.org/bot"""
        try:
            session.get(send_text, timeout=20)
            return(1)
        except:
            print('Прокси сдох '+str(proxy))
            return(0)   
    else:
        return(-1)

def DelProxy(proxy=0):
    try:
        FilePath=r'\\kari.local\public\all\For Office\Semenov\Telegram\ProgFiles\Proxy.txt'
        ProxyFile = open(FilePath,"r")   
        ProxyList = [line.rstrip('\n') for line in ProxyFile]
        ProxyFile.close()
        if len(ProxyList)>0:
                del ProxyList[0]
                os.remove(FilePath)
                ProxyFileNew = open(FilePath,"w")   
                ProxyFileNew.write("\n".join(ProxyList))
                ProxyFileNew.close()     
        else:
            print('В файле '+str(FilePath)+' нет прокси.')
    except Exception as e:
        print('Похоже Proxy.txt уже открыт. Ошибка: '+str(e))  

def ProxyFilter():
    while ProxyCheck()==0:
        DelProxy()
    ProxyChck=ProxyCheck()
    if ProxyChck==-1:
        print('Прокси кончились.')
        ParseNewProxies()
        return(-1)
    elif ProxyChck==1:
        print('Новый прокси: '+str(GetProxy()))
        return(GetProxy())

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