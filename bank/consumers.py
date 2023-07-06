import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class BankConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        self.room_name = "bank"
        self.room_group_name = f"shop_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def update_bank_account(self, event):
        self.send(text_data=json.dumps({
            "amount": event['amount']
        }))

    def update_progress_bar(self, event):
        self.send(text_data=json.dumps({
            "amount": event['amount']
        }))