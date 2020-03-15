from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer
from django.db.models import Q
from .models import Room
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room = None

    async def connect(self):
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            self.user = self.scope['user']
            self.other = self.scope['url_route']['kwargs']['other']

            author_user = User.objects.filter(email=self.user)[0]

            friend_user = User.objects.filter(id=self.other)[0]

            print(friend_user)
            if Room.objects.filter(
                    Q(author=author_user, other=friend_user) | Q(author=friend_user, other=author_user)).exists():
                self.room = Room.objects.filter(
                    Q(author=author_user, other=friend_user) | Q(author=friend_user, other=author_user))[0]
            else:
                self.room = Room.objects.create(
                    author=author_user, other=friend_user)
            self.room_group_name = 'chat_%s' % str(self.room.id)
            print("sdfdsjf", self.room_group_name)
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
