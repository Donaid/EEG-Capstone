# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 06:29:19 2022

@author: k
"""
import websocket
import json
import time

ws = websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/test1')


while(True):
    time.sleep(15)
    exec(open("complete 2.py").read())
    
     