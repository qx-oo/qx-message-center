import threading
import time
from django.core.management.base import BaseCommand
from websocket import create_connection
from qx_ws.client import MessageClient
from django.contrib.auth import get_user_model


User = get_user_model()


def ws_client():
    ws = create_connection("ws://127.0.0.1:9005/ws/message/")
    print("[ws]connected server.")
    print("[ws]Receiving...")
    result = ws.recv()
    print("[ws]Received 1 '%s'" % result)
    result = ws.recv()
    print("[ws]Received 2 '%s'" % result)
    ws.close()


def send_msg(user_id):
    time.sleep(1)
    message = {
        'type': 'notify',
        'data': {
        }
    }
    message['data']['message'] = 'all msg'
    MessageClient().send_msg_to_all(message)
    print("[sd]send {}".format(message))
    time.sleep(1)
    message['data']['message'] = 'anonymous msg'
    MessageClient().send_msg_to_anonymous(message)
    print("[sd]send {}".format(message))
    time.sleep(1)
    message['data']['message'] = 'user {} msg'.format(user_id)
    MessageClient().send_msg_to_user(message, user_id)
    print("[sd]send {}".format(message))


class Command(BaseCommand):
    help = 'Test Message Websocket'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(username="test1")
        t1 = threading.Thread(target=ws_client)
        t2 = threading.Thread(target=send_msg, args=(user.id,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("end")
