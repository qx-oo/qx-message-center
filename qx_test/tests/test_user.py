import pytest
import json
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from qx_message.models import Message
from qx_message.tasks import sendmessage_task
from qx_message.viewsets import MessageViewSet
from rest_framework.test import force_authenticate


User = get_user_model()


class TestMessage:

    @pytest.mark.django_db
    def test_model(self, rf):

        user1 = User.objects.create(username="test1")
        user2 = User.objects.create(username="test2")
        user3 = User.objects.create(username="test3")
        sendmessage_task.run('user', user1.id, user1.id,
                             user2.id, detail=json.dumps({"title": "hello"}))
        sendmessage_task.run('test', None, user3.id,
                             user2.id, detail=json.dumps({"title": "hello"}))
        message_list = list(Message.objects.filter(user_id=user2.id))
        assert len(message_list) > 1

        request = rf.get('/api/message/user-message/')
        force_authenticate(request, user2)
        views = csrf_exempt(MessageViewSet.as_view({'get': 'list'}))
        response = views(request)
        data = json.loads(response.content)
        assert len(data['data']['results']) > 1
        assert data['data']['results'][0]['user']
        assert data['data']['results'][0]['from_user']

        req_data = {
            'type': 'user',
        }
        request = rf.put('/api/message/user-message/bulk-read/',
                         data=req_data, content_type='application/json')
        force_authenticate(request, user2)
        views = csrf_exempt(MessageViewSet.as_view({'put': 'update_bulk'}))
        response = views(request)
        assert response.status_code == 200
