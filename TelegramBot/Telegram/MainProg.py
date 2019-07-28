# -*- coding: utf-8 -*-
"""
Created on Mon May  6 18:05:35 2019

@author: ao.semenov

прокси https://free-proxy-list.net/
"""

from telegram.ext import Updater, CommandHandler,MessageHandler, Filters #,InlineQueryHandler
import requests
#import re
import pyodbc
import datetime as dt
from datetime import datetime
import time
import subprocess
from subprocess import check_call
import os
import psutil
import ProxyCheck #мой модуль
#import ProxyParser
        
    
def start(bot, update):    
    txt='Добро пожаловать в помощник кари. Здесь вы сможете подписаться на интересующие вас уведомления в разделе /Menu. Но сначала необходимо открыть доступ, подробности /password.'
    update.message.reply_text(txt) 
    
def info(bot, update):
    chat_id = update.message.chat_id    
    txt="""Добро пожаловать в помощник кари. Список основных комманд в /menu."""
    update.message.reply_text(txt) 
    InList(chat_id,1) 
        
def Menu(bot, update):
    chat_id = update.message.chat_id
    if InList(chat_id,1)==1: 
        txt="""/AllSubs - список существующих подписок;
/yourSubs - ваши подписки."""
        update.message.reply_text(txt) 

    
def AllSubs(bot, update):
    txt='/Routes - маршруты;'
    update.message.reply_text(txt) 
    
def yourSubs(bot, update):
    ChatId = update.message.chat_id
    
    cursor = db.cursor()            
    sql="""select [SubName] from [DBReport].[dbo].[TelegramSubs] where [ChatId]='"""+ str(ChatId) +"""'"""    
    cursor.execute(sql)  
    data =  cursor.fetchall()  
    db.commit()
    
    text='Вы подписанны на: '+ str(data[0])
    update.message.reply_text(text) 
    
def Routes(bot, update): 
    txt="""
    Программа работает 2 раза в день: 
1 запуск - 8:00;
2 запуск -19:00;
Бот через 15 минут после запуска проверяет статус программы и, если что-то не так, отправляет уведомление.
    
/RoutesSub - подписаться на рассылку;
/RoutesUnSub - отписаться;"""
    update.message.reply_text(txt) 
    
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
    print(url)

def telegram_bot_sendtext(ChatIDs, bot_message):
    
    bot_token = token
    session = requests.session()
    session.proxies = {}
    session.proxies['https'] = ProxyCheck.ProxyFilter()   
#    session.proxies['http'] = 'http://185.85.116.18:8080'    
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

#проверка авторизации
def InList(chat_id, SendMessage=0):
     # проверяем есть ли ChatId в вайт листе     
     cursor = db.cursor()         
     sql="""select count(*) from [DBReport].[dbo].[TelegramWhiteList] where ChatId='""" + str(chat_id) + "'"    
     try:
         cursor.execute(sql)    
     except Exception as error:
         print('Error in InList: ' + error)
         
     data =  cursor.fetchall()    
     db.commit()
   
     if int(data[0][0])>0:
         return (1)
     else:           
         if SendMessage==1:
             text='Необходим пароль. Подробнее /password.'
             telegram_bot_sendtext(chat_id,text) 
         return (0)
        
def bop(bot, update):
    chat_id = update.message.chat_id
    if InList(chat_id,1)==1: 
        url = get_url()    
        bot.send_photo(chat_id=chat_id, photo=url)
       

def password(bot, update):
    chat_id = update.message.chat_id
    if InList(chat_id)==1: 
        update.message.reply_text('Вы авторезированы и имеете поный доступ ко всем командам.') 
    else:
        txt=""" Большинство команд доступны после указания пароля, который можно узнать по почте ao.semenov@kari.com. Пароль вводиться в этот чат без всяких спец символов. """
        update.message.reply_text(txt) 

    

def PswrdCheck(bot,update):   
    msg = update.message.text 
    pswrd=''
    name=update.message.from_user.first_name
    if msg==pswrd:
         # проверяем есть ли ChatId в вайт листе
         if InList(update.message.chat_id)==0:         
             #добавляем ChatId в вайтлист             
             cursor = db.cursor()            
             sql="""insert into [DBReport].[dbo].[TelegramWhiteList] values ('""" + str(update.message.chat_id) + """', N'"""+ str(name) + """',getdate())"""      

             try:
                 cursor.execute(sql)    
                 db.commit()
                 print(str(update.message.chat_id) + ' added in [TelegramWhiteList]')
                 update.message.reply_text('Пароль верный. Добро пожаловать, '+ str(name) +'. /menu')  
             except Exception as error:
                 print(str(update.message.chat_id) + ' не удалось добавить [TelegramWhiteList]./n Ошибка: '+str(error))
                 update.message.reply_text('Какая-то техническая ошибка. Обратитесь к разработчикам.')  
                              
    else:
        print('"' + str(msg) + '" is bad password')
        update.message.reply_text('"' + str(msg) + '" неверный пароль. Подробнее /password')  

class Sub():
    def NewSub(ChatId,SubName,update,bot):
        if InList(ChatId,1)==1:
            cursor = db.cursor()            
            sql="""select count(*) from [DBReport].[dbo].[TelegramSubs] where [ChatId]='"""+ str(ChatId) +"""' and [SubName]=N'"""+ str(SubName) +"""'"""     
            cursor.execute(sql)  
            data =  cursor.fetchall()    
            db.commit()
       
            if int(data[0][0])>0:
                print (str(ChatId) +' уже подписан на '+ str(SubName))
                update.message.reply_text('Вы уже были подписаны на '+ str(SubName) +'.') 
            else:
                cursor = db.cursor() 
                sql="""insert into [DBReport].[dbo].[TelegramSubs] values ('"""+ str(ChatId) +"""',N'"""+ str(SubName) +"""')"""  
                try:
                     cursor.execute(sql)    
                     db.commit()
                     print(str(ChatId) + ' подписался на ' + str(SubName))
                     update.message.reply_text('Вы подписались на '+ str(SubName) +'.')  
                except Exception as error:
                     print(str(ChatId) + ' не удалось подписаться на '+ str(SubName) + '. Ошибка: ' + str(error))
                     update.message.reply_text('Какая-то техническая ошибка. Обратитесь к разработчикам.')  
                 
    def UnSub(ChatId,SubName,update,bot):
        cursor = db.cursor()            
        sql="""select count(*) from [DBReport].[dbo].[TelegramSubs] where [ChatId]='"""+ str(ChatId) +"""' and [SubName]=N'"""+ str(SubName) +"""'"""     
        cursor.execute(sql)  
        data =  cursor.fetchall()    
        db.commit()
       
        if int(data[0][0])==0:
            print (str(ChatId) +' не был подписан на '+ str(SubName))
            update.message.reply_text('Вы не были подписаны на '+ str(SubName) +'.') 
        else:
            cursor = db.cursor() 
            sql="""delete a from [DBReport].[dbo].[TelegramSubs] a where [ChatId]='"""+ str(ChatId) +"""' and [SubName]=N'"""+ str(SubName) +"""'"""  
            try:
                 cursor.execute(sql)    
                 db.commit()
                 print(str(ChatId) + ' отписался от ' + str(SubName))
                 update.message.reply_text('Вы отписались от '+ str(SubName) +'.')  
            except Exception as error:
                 print(str(ChatId) + ' не удалось отписаться от '+ str(SubName) + '. Ошибка: ' + str(error))
                 update.message.reply_text('Какая-то техническая ошибка. Обратитесь к разработчикам.')  
                 
    def Routes(bot, update):
        ChatId = update.message.chat_id
        Sub.NewSub(ChatId,'Routes',update,bot)
    def RoutesUnSub(bot, update):
        ChatId = update.message.chat_id
        Sub.UnSub(ChatId,'Routes',update,bot)
        
def killprocess(pid):
    ppidd = str(pid) 
    try:
        if psutil.pid_exists(int(ppidd)):         
            check_call("TASKKILL /F /PID {pid} /T".format(pid=ppidd))
            print ("A process with pid killed " + pid)
        else:
            print ("A process with pid does not exist " + pid)
          
    except psutil.NoSuchProcess:
        print ('oops loose process')


def StartBats(Names):    
    KillBats=r'\\kari.local\public\all\For Office\Semenov\Telegram\ProgFiles\RunningBats.txt'
    KBlist = [line.rstrip('\n') for line in open(KillBats)]
    #  убиваем процессы, если они уже запущены 
    for pid in KBlist:
        killprocess(pid)
        
    FilePath = r'\\kari.local\public\all\For Office\Semenov\Telegram\ProgFiles\RunningBats.txt'
    if os.path.exists(FilePath):
        os.remove(FilePath)
    RunningBats = open(FilePath,"w+")
    RBlist = []
    
    for name in Names:
        try:
            p = subprocess.Popen(r'//kari.local/public/all/For Office/Semenov/Telegram/SubSenders/'+ str(name) +'.bat', creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
            print('Bat '+ str(name) +' started.')
            RBlist.append(str(p.pid))
            
        except Exception as error: 
            print(str(name) + ' bat failed to start. Error: ' + str(error))
   # запоминаем pid-ы процессов чтобы потом их убить         
    RunningBats.write("\n".join(RBlist))
  
    
def main():
       
    REQUEST_KWARGS={
    'proxy_url': ProxyCheck.ProxyFilter(),
    # Optional, if you need authentication:
#    'username': 'PROXY_USER',
#    'password': 'PROXY_PASS',
    }

    updater = Updater(token,request_kwargs=REQUEST_KWARGS)

    #### запускаем программы мониторинга и оповещений
    Names=['SubRoutesMorning','SubRoutesEvening']
    StartBats(Names)
    
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, PswrdCheck))
#    dp.add_handler(MessageHandler(Filters.text, NotUnderstand))
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('password',password))
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('info',info))
    dp.add_handler(CommandHandler('AllSubs',AllSubs))
    dp.add_handler(CommandHandler('yourSubs',yourSubs))
    dp.add_handler(CommandHandler('Routes',Routes))
    dp.add_handler(CommandHandler('RoutesSub',Sub.Routes))
    dp.add_handler(CommandHandler('RoutesUnSub',Sub.RoutesUnSub))
    dp.add_handler(CommandHandler('Menu',Menu))
    
       
    updater.start_polling()
    updater.idle()


db = pyodbc.connect(  'Driver={SQL Server Native Client 11.0};',
Server='cl01sql',
Database='DynamicsAx1',
password= '',
Trusted_Connection='yes', autocommit=True)  

token='860957767:AAFNyG3RTV5O_yntIXXBeW3OnRSPXuDeQ'
#proxy=



if __name__ == '__main__':
    main()





