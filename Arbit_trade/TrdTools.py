# -*- coding: utf-8 -*-
"""
Created on Thu May 30 07:13:24 2019

@author: Artem
"""
import Exmo

def MarketBuy(pair,quantity,price):
    order_create=ExmoAPI.api_query('order_create', {
          'pair': pair,
          'quantity':quantity,
          'price':price,
          'type':'market_buy'
        })
    OrderId=order_create['order_id']
    return(OrderId)

def MarketSell(pair,quantity,price):
    order_create=ExmoAPI.api_query('order_create', {
          'pair': pair,
          'quantity':quantity,
          'price':price,
          'type':'market_sell'
        })
    print(order_create)
    OrderId=order_create['order_id']
    return(OrderId)
    
def BuyOrder(quantity,price,pair):
    order_create=ExmoAPI.api_query('order_create', {
          'pair': pair,
          'quantity':quantity,
          'price':price,
          'type':'buy'
        })
    OrderId=order_create['order_id']
    return(OrderId)

def SellOrder(quantity,price,pair):
    order_create=ExmoAPI.api_query('order_create', {
          'pair': pair,
          'quantity':quantity,
          'price':price,
          'type':'sell'
        })
    OrderId=order_create['order_id']
    return(OrderId)

def AskVol(pair):
    order_book  = ExmoAPI.api_query('order_book', {
      'pair': pair,
      'limit':1
    })
    ask_vol=order_book[pair]['ask_quantity']
#    print('AskVol '+str(askvol))
    return(ask_vol)
    

def BidVol(pair):
    order_book  = ExmoAPI.api_query('order_book', {
      'pair': pair,
      'limit':1
    })
    bid_vol=order_book[pair]['bid_quantity']
#    print('BidVol '+str(bidvol))
    return(bid_vol)  
    

def AskTop(pair):
    ticker=ExmoAPI.api_query('ticker')
    try:
        ask_top = float(ticker[pair]['sell_price'])
    #    print('AskTop '+str(asktop))
        return(ask_top)
    except:
        print('AskTop error. No pair ' + pair)

def BidTop(pair):
    ticker=ExmoAPI.api_query('ticker')
    try:
        bid_top = float(ticker[pair]['buy_price'])
    #    print('BidTop '+ str(bidtop))
        return(bid_top)
    except:
        print('BidTop error. No pair ' + pair)

def AllPrices(AllPairs):
    SellPrices={}
    BuyPrices={}
    ticker=ExmoAPI.api_query('ticker')
    ask_top = ticker
    for pair in AllPairs:
    #    SellPrices.append(pair[ask_top[pair]['sell_price']])
        SellPrices[pair]=ask_top[pair]['sell_price']
    
    for pair in AllPairs:
    #    SellPrices.append(pair[ask_top[pair]['sell_price']])
        BuyPrices[pair]=ask_top[pair]['buy_price']
           
    return([SellPrices,BuyPrices])  

    
def Spred(pair):
    sprd = 1 - BidTop(pair)/AskTop(pair)
#    print('Spred '+str(spred))
    return(sprd)

def LastUpdt(pair):
    ticker=ExmoAPI.api_query('ticker')
    updated  = ticker[pair]['updated']
#    print('Updated '+ str(updated))
    return(updated)    

def balances(currency):
    balances = ExmoAPI.api_query('user_info')
    return(float(balances['balances'][currency]))

def currency():
    return(ExmoAPI.api_query('currency'))
 
def pair_settings():
    return(ExmoAPI.api_query('pair_settings'))

def AllOrders():
    OpenOrders=ExmoAPI.api_query('user_open_orders')
    return(OpenOrders)
    
def user_open_orders(pair):
    try:
        OpenOrders=ExmoAPI.api_query('user_open_orders')[pair]
        OrdersList=[]
        for i in range(len(OpenOrders)):
            OrdersList.append(int(OpenOrders[i]['order_id']))    
        return(OrdersList)
    except:
        print('No open orders for '+ pair)
        return([])

def order_cancel(OrderId):
    ExmoAPI.api_query('order_cancel', {
          'order_id': OrderId,
        })
    

ExmoAPI = Exmo.ExmoAPI('K-dd7c5b42d22f7a2aecc9463418cfaa898e09114f', 'S-6c8ee5af5fe56aba9429fbd129070c4db76b4cec')

