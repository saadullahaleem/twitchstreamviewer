from channels.routing import ProtocolTypeRouter, URLRouter
import stream_service.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter(stream_service.routing.websocket_urlpatterns)
})
