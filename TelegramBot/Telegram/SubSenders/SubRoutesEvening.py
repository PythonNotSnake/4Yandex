# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:03:00 2019

@author: ao.semenov
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:36:45 2019

@author: ao.semenov
"""

import datetime as dt
from datetime import datetime
import time
import requests
import pyodbc
import sys


sys.path.append('Z:\For Office\Semenov\Telegram')
import ProxyCheck


def date_diff_in_Seconds(dt2, dt1):
  timedelta = dt2 - dt1
  return timedelta.days * 24 * 3600 + timedelta.seconds

def WaitTill(Time2Wait): # Ждёт до времени в формате '12:33:00'
    time.sleep(1)
    today=dt.datetime.today()
    TodayStart = datetime.strptime(str(today)[0:10] +' '+  str(Time2Wait), '%Y-%m-%d %H:%M:%S')
    DateDiff=date_diff_in_Seconds(TodayStart,today)
    
    if DateDiff<0:
        SWait=24*3600+DateDiff
    else:
        SWait=DateDiff   
        
    print('Sleep '+ str(SWait) +' s')
    time.sleep(SWait)
    
def telegram_bot_sendtext(ChatIDs, bot_message):
    
    bot_token = token
    session = requests.session()
    session.proxies = {}
    session.proxies['https'] = ProxyCheck.ProxyFilter()   
    session.proxies['http'] = 'http://185.85.116.18:8080'
    
    if isinstance(ChatIDs, list)==False: #если не лист, конвертируем в лист
        ChatIDsList=[]
        ChatIDsList.append(ChatIDs)    
    else:   
        ChatIDsList=ChatIDs
    
    for ChatID in ChatIDsList:
        send_text = """https://api.telegram.org/bot""" + str(bot_token) + """/sendMessage?chat_id=""" + str(ChatID) + """&parse_mode=Markdown&text=""" + str(bot_message)
        session.get(send_text)
        print('Message: "' + str(bot_message) + '" sended to ' + str(ChatID) + ' at ' + str(dt.datetime.today()))
        time.sleep(0.017)
        
def RoutesSender():
    WaitTill('19:30:00')
    ### НАХОДИМ ПОДПИСЧИКОВ
    cursor = db.cursor()            
    sql="""select [ChatId] from [DBReport].[dbo].[TelegramSubs] where [SubName]=N'Routes'"""     
    cursor.execute(sql)  
    data =  cursor.fetchall()    
    i=len(data)
    ChatIDs=[]
    while i>0:
        i-=1
        ChatIDs.append(data[i][0])
        
        #### проверяем статус программы     
    sql="""select DateStart from [DBReport].[dbo].[RoutesLogEvening] where cast(DateStart as date)=cast(getdate() as date) and datepart(HOUR,DateStart)=19 and StoreMailStatus>0"""  
    cursor.execute(sql)  
    data =  cursor.fetchall()
    db.commit()
    if len(data)==0:
        text=""" *Маршруты.*
Похоже что-то не так. До сих пор не отправлено не одного письма. Скорее всего это ошибка (возможен случай, когда нет маршрутов для рассылки)."""
        ## делаем рассылку    
        telegram_bot_sendtext(ChatIDs,text)    
    
    WaitTill('23:59:00')
    #### проверяем статус программы     
    cursor = db.cursor()  
    sql="""declare @today date =cast(getdate() as date)
    
            select top 1 DateStart, sum([StoreMailStatus]) [MailSended], count(distinct store) AS [AllStores]
            from [DBReport].[dbo].[RoutesLogEvening] 
            where cast([DateStart] as date) = @today		
            group by [DateStart]
			order by [DateStart] desc]"""  
    cursor.execute(sql)  
    data =  cursor.fetchall()
    db.commit()
    
    
    
    if data[0][1]<data[0][2]:
        text=""" *Маршруты.* 
Программа запустилась в """ + str(data[0][0])[:-10] + """, отправленно """ + str(data[0][1]) +""" писем из """ + str(data[0][2]) + """. Возможно это ошибка."""
        ## делаем рассылку    
        telegram_bot_sendtext(ChatIDs,text)  
    ##заходим на следующий цикл
    RoutesSender() 




    
db = pyodbc.connect(  'Driver={SQL Server Native Client 11.0};',
Server='cl01sql',
Database='DynamicsAx1',
password= '',
Trusted_Connection='yes', autocommit=True)  

token='860957767:AAFNyG3RTV5OOnRSPXuDeQ'

ProxyCheck.ProxyFilter()   # проверяем прокси
RoutesSender()

    
    
    
    
    
    
    
    
    
    
    
    
    
    