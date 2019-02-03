import json
import requests
from django.conf import settings
from stream_service.models import Event, Streamer
from stream_service.consumers import send_to_room

def get_follow_message(from_name, to_name):
    return f"{from_name} followed {to_name}"

def create_follow_event(streamer_name, from_name):
    print("creating follow event")
    message = get_follow_message(from_name, streamer_name)
    streamer, _ = Streamer.objects.get_or_create(display_name=streamer_name)
    event = Event.objects.create(streamer=streamer, text=message)
    send_to_room(streamer_name, message)
    return event

def get_latest_events(streamer_name, count=10):
    return Event.objects.filter(streamer__display_name=streamer_name).order_by(
        '-created_at')[:count]

def get_auth_headers():
    return {
        'client-id': settings.SOCIAL_AUTH_TWITCH_KEY
    }

def get_channel_info(display_name):
    endpoint = 'channels'
    headers = {
        'client-id': settings.SOCIAL_AUTH_TWITCH_KEY
    }
    payload = {
        'url': f'{settings.TWITCH_API}/{endpoint}/{display_name}',
        'headers': headers
    }
    response = requests.get(**payload)
    return json.loads(response.text)

def get_user_id(login_name):
    endpoint = 'users'
    url = f'{settings.TWITCH_NEW_API}/{endpoint}?login={login_name}'
    try:
        response = requests.get(url=url, headers=get_auth_headers())
        return json.loads(response.text).get('data')[0]['id']
    except Exception as e:
        return None

def subscribe_to_follows(login_name, callback_url):
    user_id = get_user_id(login_name)
    print(f"user_id for login name {login_name}: {user_id}")
    endpoint = 'webhooks/hub'
    url = f'{settings.TWITCH_NEW_API}/{endpoint}'
    payload = {
        "hub.mode": "subscribe",
        "hub.topic": f"{settings.TWITCH_NEW_API}/users/follows?first=1&to_id={user_id}",
        "hub.callback": callback_url,
        "hub.lease_seconds": "864000",
        "hub.secret": "s3cRe7"
    }
    response = requests.post(url=url, data=payload, headers=get_auth_headers())

    return response.status_code

