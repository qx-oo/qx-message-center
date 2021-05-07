from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings


try:
    ws_auth = settings.QX_MESSAGECENTER_SETTINGS.get('ws_auth', True)
except AttributeError:
    ws_auth = False


class MessageConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_list = [
            'global',
        ]
        if ws_auth and self.scope['user'].is_authenticated:
            self.group_list.append('login')
            self.group_list.append('user_{}'.format(self.scope['user'].id))
        else:
            self.group_list.append('anonymous')

        for group_name in self.group_list:
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        for group_name in self.group_list:
            await self.channel_layer.group_discard(
                group_name,
                self.channel_name
            )

    async def receive_json(self, content, **kwargs):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'new_message',
        #         'message': message
        #     }
        # )
        pass

    async def push_message(self, event):
        await self.send_json(event['content'])
