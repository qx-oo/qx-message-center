# qx-message-center

my django project user message center

#### Depends:

    qx-base

### Install:

    $ pip install -e git://github.com/qx-oo/qx-base.git@1.0.2#egg=qx-base
    $ pip install -e git://github.com/qx-oo/qx-message-center.git@master#egg=qx-message-center

### Usage:

settings.py:

    INSTALLED_APPS = [
        ...
        'qx_base.qx_core',
        'qx_message',
        ...
    ]

    QX_MESSAGECENTER_SETTINGS = {
        "message_send_callback": lambda empty: empty,
        "message_object_map": {
            "comment": "comment.Comment",
            "star": "comment.Star",
        },
        "message_user_serializer": "user.models.SimpleUserSerializer",
    }

urls.py:

    urlpatterns_api = [
        path('', include('qx_message.urls')),
    ]

celery.py:

    app.conf.task_routes = {
        'qx_message.tasks.SendMessage': {
            'queue': 'default',
        },
    }

### Websocket Usage:

settings.py:

    INSTALLED_APPS = [
        ...
        'channels',
        'qx_base.qx_core',
        'qx_ws',
        ...
    ]

asgi.py:

    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AioAuthMiddleware(
            URLRouter(
                qx_ws.routing.websocket_urlpatterns,
            )
        ),
    })

Send message:

    from qx_ws.client import MessageClient
    MessageClient().send_msg_to_all({'test': 'ok'})

### Test:

    $ pytest .

ws test:

    $ python manage.py migrate
    $ python manage.py runserver 9005
    $ python manage.py ws_test