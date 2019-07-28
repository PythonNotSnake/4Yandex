@echo on
::закрываем программу если она уже открыта
taskkill /fi "WINDOWTITLE eq SubRoutesEvening"
title SubRoutesEvening

C:\Users\ao.semenov\AppData\Local\Continuum\anaconda3\python.exe "\\kari.local\public\all\For Office\Semenov\Telegram\SubSenders\SubRoutesEvening.py
pause