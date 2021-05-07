from rest_framework import serializers
from qx_base.qx_core.tools import DictInstance
from .settings import messagecenter_settings
from .models import Message


UserSerializer = messagecenter_settings.message_user_serializer


if UserSerializer:
    def userinfo_func(user): return UserSerializer(user).data
else:
    if messagecenter_settings.has_userinfo:
        def userinfo_func(user): return user.get_simple_userinfo()
    else:
        def userinfo_func(user): return user.id


um_read_only_fields = (
    "id", "created", "detail", "user", "from_user", "type", "object_id",)


class MessageSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    from_user = serializers.SerializerMethodField()

    def get_user(self, instance):
        return userinfo_func(instance.user)

    def get_from_user(self, instance):
        return userinfo_func(instance.from_user)

    class Meta:
        model = Message
        fields = um_read_only_fields + ('is_read', )
        read_only_fields = um_read_only_fields


class BulkUpdateMessageSerializer(serializers.Serializer):

    type = serializers.ChoiceField(
        list(Message.type_map_model.keys()), label="消息类型",
        required=False)

    def create(self, validated_data):
        _type = validated_data.get('type', None)
        if _type:
            Message.objects.filter(
                type=_type,
                user_id=self.context['request'].user.id,
            ).update(is_read=True)
        else:
            Message.objects.filter(
                user_id=self.context['request'].user.id,
            ).update(is_read=True)
        return DictInstance(data=validated_data)
