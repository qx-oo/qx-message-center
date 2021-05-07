from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async


class AioAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope['user'] = await self.get_user()
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(username='test1')
        except UserModel.DoesNotExist:
            return AnonymousUser()


def AioAuthMiddlewareStack(app):
    return AioAuthMiddleware(AuthMiddlewareStack(app))
