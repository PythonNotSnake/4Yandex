# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:49:23 2019

@author: Artem
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:03:58 2019

@author: Artem

Обмен
https://www.bestchange.ru/wiki/article-ex-code.html

"""
import time
import sys
sys.path.append(r"C:\Users\Artem\Google Диск\Python Scripts\BTC")
import TrdTools as tt


def LoopTry(func,arg=[]):
    try:       
        exec('func('+str(arg)[1:-1] +')')
    except Exception as e:
        print(e)
        time.sleep(1)
        LoopTry(func,arg)
      
        
fee=0.002
AllPairs = tt.pair_settings().keys()
AllCurrency = tt.currency()
#### WHA### WHAT ON MY BALANCE
#AllCurrency = tt.currency()
#balances=tt.balances
#for cur in AllCurrency:
#    MyBalance=balances(cur)
#    if MyBalance>0:
#        MyCurrency=cur  
#        print('Currency: '+ MyCurr '+ MyCurrency +' Balance: '+str(MyBalance))

MyCurrency='BTC'
MyBalanceReal=0.001

win=0
WinCur1=''
WinCur2=''

now = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
print('Start at ' + now)

# print(AllPrices()[1]['ZEC_RUB'])

while 1==1:
    
    
    for cur1 in AllCurrency:
        
        start=time.time()
        
        if win==1:
            cur1=WinCur1        
        
        pair1=cur1+'_'+MyCurrency
        MyBalance=MyBalanceReal
#        MyBalance = tt.balances(MyCurrency) # реальный баланс
        
        if pair1 in AllPairs:
            AllPrices =  tt.AllPrices(AllPairs)
            
    
            BuyPriceCur1=float(AllPrices[0][pair1])  #tt.AskTop(pair1)
            NewBalanceCur1=MyBalance/BuyPriceCur1*(1-fee)
    
            
            for cur2 in AllCurrency:
                
                if win==1:
                    cur2=WinCur2
                    
                pair2=cur2+'_'+cur1
                MyBalance=MyBalanceReal
                
                if pair2 in AllPairs:
#                    tt.pair_settings()[pair2] #можно убрать
                    BuyPriceCur2=float(AllPrices[0][pair2]) #tt.AskTop(pair2)
                    NewBalanceCur2=NewBalanceCur1/BuyPriceCur2*(1-fee)
                    
                    #  TRY TO CLOSE DEAL WITH PROFIT               
                    pairClose=cur2+'_'+MyCurrency
                    if pairClose in AllPairs:
                        SellPriceClose=float(AllPrices[1][pairClose])#tt.BidTop(pairClose)                        
                        NewBalanceClose=NewBalanceCur2*SellPriceClose*(1-fee)
                        
#                        print(time.time()-start)
                        
                        if NewBalanceClose > 1.035*MyBalance and time.time()-start<3:
                            print('\nWIN')
                            print(time.ctime())
                            print(pair1+' '+str(BuyPriceCur1))
                            print(cur1 +' balance '+ str(NewBalanceCur1))
                            print(pair2+' '+ str(BuyPriceCur2))
                            print(cur2 +' balance '+ str(NewBalanceCur2))
                            print(pairClose+' '+ str(SellPriceClose))
                            print(MyCurrency +' balance '+ str(NewBalanceClose))

                            
#                            quantity1=float(tt.pair_settings()[pair1]['min_quantity']) * 1.2
                            quantity1=MyBalance/BuyPriceCur1 # на все бабки
                            OrderId1 = tt.MarketBuy(pair1,quantity1,0)#tt.MarketBuy(pair1)
                            print('Waiting OrderId1 '+ str(OrderId1))
#                            while OrderId1 in tt.user_open_orders(pair1):                                
#                            time.sleep(0.1)
                                
#                            quantity2 = quantity1 / BuyPriceCur2 *(1-fee)
                            OrderId2 = tt.MarketBuy(pair2,NewBalanceCur2*0.9999,0)
                            print('Waiting OrderId2 '+ str(OrderId2))
#                            while OrderId2 in tt.user_open_orders(pair2):                              
#                            time.sleep(0.1)
                            
#                            quantity3 = quantity2 * SellPriceClose *(1-fee)
                            OrderId3 = tt.MarketSell(pairClose,tt.balances(cur2),0)
                            print('Waiting OrderId3 '+ str(OrderId3))
#                            while OrderId3 in tt.user_open_orders(pairClose):                             
#                                time.sleep(0.1)
                                
                            win=1
                            WinCur1=cur1
                            WinCur2=cur2  
                            print('Реальный баланс: ' + str(tt.balances(MyCurrency)) +' '+ MyCurrency)
                            
                        else:
                            error='Bad deal'
                            win=0
#                            print(error)
                    else:
                        error='No pairClose '+str(pairClose)
#                        print(error)
                
                else:
                    error='No pair2 '+str(pair2)
#                    print(error)
        else:
            error='No pair1 '+str(pair1)
#            print(error)
    




    
    



