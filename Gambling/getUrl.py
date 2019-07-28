import requests
import pyodbc
import subprocess
import json
import time

#from multiprocessing import Pool
from multiprocessing import Process, Lock

def makeCSVline(line):

    delimetr = line.index('-')
    FrstPart=line[1:delimetr]
    SecondPart=line[delimetr+1:-1].replace(' ','').replace('-',' ')
    return(FrstPart+','+SecondPart)

def getUrls(url,startLine,EndLine,Company,Lid=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
    r = requests.get(url, headers = headers)   
    r.encoding = 'UTF-8'
    OrigScript = str(r.text)
    script = OrigScript    
        
    save=''    
    i=0
    startLen=len(startLine)-1
    Urls=''
    Mids=[]
    while 1==1:

#        site.write(script)
        try:
            index = script.index(startLine) 
        except Exception as e:
            print(e)
            break
        
        proxyUrl=script[index+startLen:index+startLen+script[index+startLen:].index(EndLine)]
        if len(proxyUrl)>2:
            newLine = Company +',' + str(Lid) +',' + makeCSVline(proxyUrl) #1 - айди для 1xstavka
            Mids.append(proxyUrl[1:proxyUrl.index('-')])
            try: #убираем ссылки на матчи, нужны только лиги
                newLine.index('/')
            except:             
                Urls = Urls + newLine +'\n'
        else:
            index=index+2
            
        i=index+script[index+startLen:].index(EndLine)
        script=script[i:] 

# СОХРАНЯЕМ МАТЧИ 
    save = save + Urls 
    return[getCoefs(Lid,OrigScript,Mids),save]
        
        
def getLeagues(url,startLine,EndLine,Company,Sport):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
    r = requests.get(url, headers = headers)   
    r.encoding = 'UTF-8'
    script=str(r.text)
    
    save=''
    i=0
    startLen=len(startLine)-1
    Urls=''
    
    while 1==1:

#        site.write(script)
        try:
            index = script.index(startLine) 
            proxyUrl=script[index+startLen:index+startLen+script[index+startLen:].index(EndLine)]
        except Exception as e:
            print(e)
            break


        if len(proxyUrl)>2:
            newLine = Company +','+ makeCSVline(proxyUrl) +','+ Sport #1 - айди для 1xstavka
            try: #убираем ссылки на матчи, нужны только лиги
                newLine.index('/')
            except:             
                Urls = Urls + newLine +'\n'
        else:
            index=index+2
        
        try:
            i=index+script[index+startLen:].index(EndLine)
            script=script[i:] 
        except Exception as e:
            print(e)
            break

# СОХРАНЯЕМ МАТЧИ 
        save = save + Urls
    return(save)
        

        
def InsertSQL(sqlCmd,SqlFile):
    with open(SqlFile, 'w', encoding='utf-8') as file:
        file.write(sqlCmd)   
    cmd=r'SQLCMD -S DESKTOP-1EMAB5Q\SQLSERVER -d Gambling -i "'+ SqlFile +'" '
    subprocess.call(cmd)

def SqlCmd(cmd):
    driver = 'DRIVER={SQL Server}'
    server = 'SERVER=DESKTOP-1EMAB5Q\SQLSERVER'
    db = 'DATABASE=Gambling'
    WinAtrz='Trusted_Connection=True'
    AutoCommite='autocommit=True'
    conn_str = ';'.join([driver, server,  db, WinAtrz,AutoCommite])
    try: 
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(cmd)
        return(cursor.fetchall())
        cursor.close()
    except Exception as e:
        print(cmd)
        print(e)
    


def getCoefs(Lid,script,Mids):   
    Coefs=''

    try:
        StartScriptIndex=script.index(';var SSR_DASHBOARD = ')
        EndScriptIndex=script[StartScriptIndex:].index(';var SSR_TOP_SPORTS = ')
        scriptLig=script[StartScriptIndex:StartScriptIndex+EndScriptIndex]      

        for Mid in Mids:
            try:
                startLineMatch='{"CI":'+ str(Mid) +',"CN"'
                StartScriptMatchIndex=scriptLig.index(startLineMatch)
                EndLineMatchIndex=scriptLig[StartScriptMatchIndex:].index(']')+1
                
                scripMatch = scriptLig[StartScriptMatchIndex:StartScriptMatchIndex+EndLineMatchIndex]
                scripMatchList = scripMatch[scripMatch.index('['):]
                data = json.loads(scripMatchList)
                newRowList = ['1',str(Mid),JsonCoefParse(data,1),JsonCoefParse(data,2),JsonCoefParse(data,3),JsonCoefParse(data,4)]
                newRowList += [JsonCoefParse(data,5),JsonCoefParse(data,6),JsonCoefParse(data,9),'0',JsonCoefParse (data,10),JsonCoefParse(data,7),'0',JsonCoefParse(data,8)]
                newRowList += [JsonCoefParse(data,11),'0',JsonCoefParse(data,12),JsonCoefParse(data,13),'0',JsonCoefParse(data,14)]
                newRow = ",".join(newRowList )+'\n'
                Coefs=Coefs + ForaIntoChar(newRow)   
            except Exception as e:
                print(e)
#            print(Coefs)
                    
    except Exception as e:
        print(e)
        
    if Coefs is not None:
#        InPut = InPut + Coefs
        return(Coefs)

        
        
    
def get_index(input_string, sub_string, ordinal):
    current = -1
    for i in range(ordinal):
        try:
            current = input_string.index(sub_string, current + 1)
        except Exception as e:
            raise ValueError("ordinal {} - is invalid".format(ordinal))
    return current

def ForaIntoChar(input_string):
    sub_string=','
    ordinal=12
    startIndex= get_index(input_string, sub_string, ordinal)
    EndIndex= startIndex+1+input_string[startIndex+1:].index(',')    
    fora = input_string[startIndex+1:EndIndex]    
    OutString=input_string[:startIndex]+",'"+ fora + "'" + input_string[EndIndex:]
    return(OutString)  
    
def JsonCoefParse(data,T):
    for i in range(len(data)):
        if data[i]['T']==T:
            return(str(data[i]['C']))
            del data[i]
            break
    return('0')    

def getSports():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
    r = requests.get('https://1xstavka.ru/', headers = headers)   
    r.encoding = 'UTF-8'
    script=str(r.text)
    StartSportIndex=script.index('var SPORTS = {')
    script=script[StartSportIndex:StartSportIndex+script[StartSportIndex:].index('}')]
#    print(scriptSports)
    
    i=0
    startLine='"'
    EndLine='"'
    startLen=len(startLine)-1
    Sports=[]
    
    while 1==1:

#        site.write(script)
        try:
            index = script.index(startLine) 
            Sport=script[index+startLen+1:index+startLen+script[index+startLen+1:].index(EndLine)+1]
        except Exception as e:
            print(e)
            break

        if len(Sport)>2:
            Sports.append(Sport.replace('_','-'))
        else:
            index=index+2
        
        try:
            i=index+startLen+script[index+startLen+1:].index(EndLine)+2
            script=script[i:] 
        except Exception as e:
            print(e)
            break

    return(Sports)
    
    
def SportLoad(Sport,lock):

        # СОХРАНЯЕМ ЛИГИ
    savefile=r'C:\Users\Artem\Google Диск\Python Scripts\Gambling\Leagues.csv'
    url='https://1xstavka.ru/line/'+Sport+'/'  

     
    lock.acquire()
    with open(savefile, 'w', encoding='utf-8') as file:
        file.write(getLeagues(url,'line/'+ Sport +'/','"','1',Sport))       

    SqlFile=r'C:\Users\Artem\Google Диск\Python Scripts\Gambling\ProgFiles\PEtlXBetLeague.sql'
    sqlCmd="""Exec [Gambling].[dbo].[PEtLeague] '""" + Sport +"""'"""
    
    InsertSQL(sqlCmd,SqlFile)
    lock.release()
#       
    # СОХРАНЯЕМ МАТЧИ И КОЭФЫ
    cmd="""select Lid,League from [Gambling].[dbo].[League] where CompanyId=1 and Sport='""" + Sport +"""'"""
    SqlResult=SqlCmd(cmd)
    MatchSave=''
    CoefSave=''
    LeaguesNum=len(SqlResult)
    
    for i in range(LeaguesNum):
        Lid=SqlResult[i][0]
        League=SqlResult[i][1].rstrip()
        url='https://1xstavka.ru/line/'+ Sport +'/'+ str(Lid) +'-'+League.replace(' ','-')+'/'
        startLine = Sport+'/'+ str(Lid) +'-'+League.replace(' ','-')+'/'
        Load = getUrls(url,startLine,'"','1',Lid)
        MatchSave = MatchSave+ Load[1]
        CoefSave = CoefSave + Load[0]
        LeaguesNum-=1
        print('Sport: '+ Sport +'. Leagues left: ' +str(LeaguesNum))
    
    lock.acquire()      
    savefile=r'C:\Users\Artem\Google Диск\Python Scripts\Gambling\Matches.csv'
    with open(savefile, 'w', encoding='utf-8') as file:
        file.write(MatchSave)       
    
    SqlFile=r'C:\Users\Artem\Google Диск\Python Scripts\Gambling\ProgFiles\PEtlMatch.sql'
    sqlCmd="""Exec [Gambling].[dbo].[PEtlMatch] '""" + Sport +"""'"""
    InsertSQL(sqlCmd,SqlFile)
        
    savefile=r'C:\Users\Artem\Google Диск\Python Scripts\Gambling\MatchCoef.csv'    
    with open(savefile, 'w', encoding='utf-8') as file:
        file.write(CoefSave)     
        
    SqlFile=r'C:\Users\Artem\Google Диск\Python Scripts\Gambling\ProgFiles\PEtlMatchCoef.sql'
    sqlCmd="""Exec [Gambling].[dbo].[PEtlMatchCoef] '""" + Sport +"""'""" 
    InsertSQL(sqlCmd,SqlFile)     
    lock.release()
    

start=time.time()

Sports=['Basketball','Ice-Hockey','Volleyball','Table-Tennis','Esports','Tennis','Football']
#Sports=getSports()

#    print(p.map(SportLoad, Sports))
if __name__ == '__main__':
    procs=[]
    lock = Lock()
    
    for index, number in enumerate(Sports):
        proc = Process(target=SportLoad, args=(number,lock))
        procs.append(proc)
        proc.start()
    
    for proc in procs:
        proc.join()
        
#for Sport in Sports:
#    SportLoad(Sport)


print('Duration: '+ str(time.time()-start) + 's')
      
                                                            

