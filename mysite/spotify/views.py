from django.shortcuts import render
from django.http import HttpResponse

from .models import Account, Playlist, Artist, Album, Song


# Create your views here.

def index(request):
    return render(request, 'index.html')


def Accounts(request):
    accounts = Account.objects.all()

    return render(request, 'Accounts.html', {'accounts':accounts})

def Playlists(request):
    playlists = Playlist.objects.all()

    return render(request, 'Playlists.html', {'playlists':playlists})

def Artists(request):
    artists = Artist.objects.all()

    return render(request, 'Artists.html', {'artists':artists})

def Albums(request):
    albums = Album.objects.all()

    return render(request, 'Albums.html', {'albums':albums})

def Songs(request):
    songs = Song.objects.all()

    return render(request, 'Songs.html', {'songs':songs})

