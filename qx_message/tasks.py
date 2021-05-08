import json
from qx_base.qx_core.tasks import Task
from qx_ws.client import MessageClient
from .settings import messagecenter_settings
from .models import Message


send_callback = messagecenter_settings.message_send_callback


class SendMessage(Task):

    def run(self, _type, object_id, from_user, to_user, detail: str):
        data = {
            "type": _type,
            "object_id": object_id,
            "from_user_id": from_user,
            "user_id": to_user,
            "detail": json.loads(detail),
        }
        instance = Message.objects.create(**data)
        if messagecenter_settings.ws_push:
            MessageClient().send_msg_to_user({
                'type': 'new_message',
                'data': {},
            }, to_user)
        send_callback(instance)
        return instance.id
