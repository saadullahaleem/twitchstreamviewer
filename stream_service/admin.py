from django.contrib import admin
from stream_service.models import Event, Streamer, User


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'streamer', 'text')

admin.site.register(Streamer)
admin.site.register(User)