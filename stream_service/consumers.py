from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_to_room(room_name, text):
    channel_layer = get_channel_layer()
    content = {"message": text}
    async_to_sync(channel_layer.group_send)(
        f'chat_{room_name}',
        {
            "type": "message_received",
            "content": json.dumps(content)
        },
    )

class EventsConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['streamer_name']
        self.room_group_name = f'chat_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def message_received(self, event):
        self.send(text_data=event['content'])

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)
        # type = text_data_json['type']
        type = text_data_json['type']

        if type == "ping":
            self.send(text_data=json.dumps({"message": "pong"}))