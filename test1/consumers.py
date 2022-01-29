import json
from random import randint
from time import sleep


from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class GraphConsumer(WebsocketConsumer):
    def connet(self):
        self.accept()
        
        for i in range(1000):
            self.send(json.dumps({'value' : randint(-20,20)}))
            sleep(1)
        
        
class test2(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.groupname = 'dashboard'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
            )
        
        await self.accept()
        
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
                self.groupname,
                self.channel_name
            
        )
        
        #Receive data from database.
    async def receive(self, text_data):
        
        datapoint = json.loads(text_data)
        #val = datapoint['value']
        val = datapoint['Attention']
        await self.channel_layer.group_send(
            self.groupname,{
                'type' : 'deprocessing',
                'Attention' : val
                
            }
        )
        
        print ('DB>>>>',text_data)
        
        #pass
#A channel is used to send messages.
    async def deprocessing(self,event):
        valOther=event['Attention']
        
        
        await self.send(text_data = json.dumps({'Attention' : valOther}))
                        