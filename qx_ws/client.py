from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class MessageClient():

    def __init__(self) -> None:
        self.channel_layer = get_channel_layer()

    def send_msg(self, group_name, message: dict):
        async_to_sync(self.channel_layer.group_send)(
            group_name, {
                "type": "push_message",
                "content": message
            })

    def send_msg_to_all(self, message: dict):
        self.send_msg('global', message)

    def send_msg_to_anonymous(self, message: dict):
        self.send_msg('anonymous', message)

    def send_msg_to_login(self, message: dict):
        self.send_msg('login', message)

    def send_msg_to_user(self, message: dict, user_id):
        group_name = 'user_{}'.format(user_id)
        self.send_msg(group_name, message)
