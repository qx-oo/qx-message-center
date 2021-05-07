from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack


class AioAnonymousMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope['user'] = AnonymousUser()
        return await self.app(scope, receive, send)


def AioAnonymousMiddlewareStack(app):
    return AioAnonymousMiddleware(AuthMiddlewareStack(app))
