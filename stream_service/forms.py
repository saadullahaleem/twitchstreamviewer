from django import forms
from .models import User

class StreamerForm(forms.ModelForm):
    favorite_streamer = forms.CharField(label='Your Favorite Streamer', max_length=100)

    class Meta:
        model = User
        fields = ['favorite_streamer']