from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from qx_base.qx_core.models import ContentTypeRelated, load_set_queryset_object


class Message(ContentTypeRelated):

    user_id = models.IntegerField(
        verbose_name="用户Id", null=True, blank=True, db_index=True)
    from_user_id = models.IntegerField(
        verbose_name="发送用户Id", null=True, blank=True)
    is_active = models.BooleanField(
        verbose_name="是否可用", default=True)
    is_read = models.BooleanField(
        verbose_name="是否读取", default=False)
    created = models.DateTimeField(
        verbose_name='创建时间', default=timezone.now, editable=False)
    detail = JSONField(
        verbose_name="详情", default=dict)

    type_map_model = settings.QX_MESSAGECENTER_SETTINGS['message_object_map']

    @staticmethod
    def load_user(queryset):
        User = get_user_model()
        field_map = {
            'user_id': 'user',
            'from_user_id': 'from_user'
        }
        if settings.QX_MESSAGECENTER_SETTINGS.get('has_userinfo', True):
            select_related = ['userinfo']
        else:
            select_related = []
        return load_set_queryset_object(
            queryset, User, field_map, select_related)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = verbose_name
