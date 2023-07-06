import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from users.models import Message


class ChatConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        self.room_name = "chat"
        self.room_group_name = f"shop_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        user = User.objects.get(pk=text_data_json["user"])
        new_message = Message.objects.create(user=user, text=text_data_json["message"], date=datetime.datetime.now())
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "username": user.first_name,
                "message": new_message.text,
                "date": new_message.date.strftime('%H:%M')
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "username": event['username'],
            "message": event['message'],
            "date": event['date']
        }))
