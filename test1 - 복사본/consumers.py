import json
from random import randint


from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer


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
                        