import json

from django.shortcuts import (render, redirect, HttpResponse)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from stream_service.utils import (get_channel_info, create_follow_event,
                                  subscribe_to_follows, get_latest_events)
from stream_service.forms import StreamerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def get_favorite_streamer(request):
    if request.method == 'POST':
        form = StreamerForm(request.POST)

        if not request.user.is_anonymous:
            form.instance = request.user

        if form.is_valid():
            form.save()
            channel_info = get_channel_info(form.data['favorite_streamer'])
            print(channel_info)
            return redirect('stream')
    else:
        form = StreamerForm()

    return render(request, 'favorite_streamer.html', {'form': form})

@login_required
def get_stream(request):
    url = request.get_host()
    callback_url = request.build_absolute_uri('/callback/')
    print(callback_url)
    subscribe_to_follows(request.user.favorite_streamer, callback_url)
    latest_events = get_latest_events(request.user.favorite_streamer)
    print(latest_events)
    return render(request, 'stream.html', {'user': request.user, 'url': url,
                                           'latest_events': latest_events})


def login(request):
    if not request.user.is_anonymous:
        return redirect('stream')
    return render(request, 'login.html', { 'login_url': '/login/twitch/'})

def logout_view(request):
    logout(request)
    return redirect('login')

@method_decorator(csrf_exempt, name='dispatch')
class WebHookView(CreateView):

    def get(self, request, *args, **kwargs):
        return HttpResponse(request.GET['hub.challenge'])

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        create_follow_event(data['data'][0]['to_name'].lower(),
                           data['data'][0]['from_name'].lower())
        return HttpResponse()