@echo on
::закрываем программу если она уже открыта
taskkill /fi "WINDOWTITLE eq SubRoutesMorning"
title SubRoutesMorning

C:\Users\ao.semenov\AppData\Local\Continuum\anaconda3\python.exe "\\kari.local\public\all\For Office\Semenov\Telegram\SubSenders\SubRoutesMorning.py
pause