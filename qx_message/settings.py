from django.conf import settings
from django.utils.module_loading import import_string
from qx_base.qx_core.tools import DictInstance


IMPORT_LIST = [
    'message_send_callback',
    'message_user_serializer',
]


QX_MESSAGECENTER_SETTINGS = {
    "message_send_callback": lambda m: m,
    "message_object_map": None,
    "message_user_serializer": None,
    "has_userinfo": True,
    "ws_push": True,
}

_b_settings = QX_MESSAGECENTER_SETTINGS

_settings = getattr(settings, 'QX_MESSAGECENTER_SETTINGS',
                    QX_MESSAGECENTER_SETTINGS)

if _settings:
    _b_settings.update(_settings)


def get_attr(key, val):
    if key in IMPORT_LIST:
        if val:
            if isinstance(val, str):
                return import_string(val)
            else:
                return val
    return val


messagecenter_settings = DictInstance(**QX_MESSAGECENTER_SETTINGS)
for key, val in _b_settings.items():
    setattr(messagecenter_settings, key, get_attr(key, val))
