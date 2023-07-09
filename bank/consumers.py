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


class AuditConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        self.room_name = f'audit_{self.scope["url_route"]["kwargs"]["room_name"]}'
        self.room_group_name = f"shop_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def update_progress_bar(self, event):
        self.send(text_data=json.dumps({
            "progress": event['progress']
        }))


class DeclarationConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        self.room_name = "declaration"
        self.room_group_name = f"shop_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def upload_declaration(self, event):
        self.send(text_data=json.dumps({
            "count_docs": event['count_docs']
        }))