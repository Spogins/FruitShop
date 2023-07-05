import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from users.models import Message


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        print('connect')
        self.room_name = "chat"
        self.room_group_name = f"shop_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print('disconnect')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        pass

