import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class FruitConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = "fruit"
        self.room_group_name = f"shop_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def update_fruit(self, event):
        self.send(text_data=json.dumps({
            "status": event['status'],
            "fruit_name": event['fruit_name'],
            "fruit_id": event['fruit_id'],
            "date": event['date'],
            "amount": event['amount'],
            "usd": event['usd'],
            "operation": event['operation']
        }))