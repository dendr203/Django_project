from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from django.contrib import messages

from .models import Category, Account, Playlist, Artist, Album, Song, AccountFollowedAlbums, AccountFollowedPlaylists, \
    AccountFollowedArtists


# Create your views here.

def index(request):
    return render(request, 'Index.html')


def userLogin(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = Account.objects.get(username=username)
            if user.password == password:
                login(request, user)
                request.session['logged_in_user'] = user.username  # Uložení jména uživatele do relace
                return redirect('userAccount')
            else:
                error_message = "Neplatné heslo. Zkuste to znovu."
        except Account.DoesNotExist:
            error_message = "Neplatné přihlašovací údaje. Zkuste to znovu."
    return render(request, 'UserLogin.html', {'error_message': error_message})


def userAccount(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        try:
            account = Account.objects.get(username=logged_in_user)
            created_playlists = Playlist.objects.filter(creator_account=account)
            categories = Category.objects.all()
            return render(request, 'UserAccount.html', {'account': account,
                                                        'created_playlists': created_playlists,
                                                        'categories': categories})
        except Account.DoesNotExist:
            return redirect('userLogin')
    else:
        return redirect('userLogin')


def deletePlaylist(request, playlist_id):
    if request.method == 'POST':
        playlist = Playlist.objects.get(pk=playlist_id)
        playlist.delete()
    return redirect('userAccount')


def createPlaylist(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        if request.method == 'POST':
            playlist_name = request.POST.get('playlistName')
            playlist_note = request.POST.get('playlistNote')
            playlist_category = Category.objects.get(category_name = request.POST.get('playlistCategory'))
            account = Account.objects.get(username = logged_in_user)
            new_playlist = Playlist(playlist_name=playlist_name, playlist_note=playlist_note,
                                    playlist_category=playlist_category, creator_account=account)
            new_playlist.save()
            return redirect('userAccount')
    else:
        return redirect('userLogin')


def followingPlaylists(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        try:
            account = Account.objects.get(username=logged_in_user)
            following_playlists = AccountFollowedPlaylists.objects.filter(account=account)
            available_playlists = Playlist.objects.exclude(accountfollowedplaylists__account=account).exclude(creator_account=account)
            return render(request, 'FollowingPlaylists.html',{'account': account,
                                                              'followingPlaylists': following_playlists,
                                                              'availablePlaylists': available_playlists})
        except Account.DoesNotExist:
            return redirect('userLogin')
    else:
        return redirect('userLogin')


def unfollowPlaylist(request, playlist_id):
    if request.method == 'POST':
        logged_in_user = request.session.get('logged_in_user')
        if logged_in_user:
            AccountFollowedPlaylists.objects.filter(account__username=logged_in_user, playlist_id=playlist_id).delete()
    return redirect('followingPlaylists')


def followPlaylist(request, playlist_id):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        if request.method == 'POST':
            account = Account.objects.get(username = logged_in_user)
            playlist = Playlist.objects.get(playlist_id = playlist_id)

            messages.debug(request, account.username)
            messages.debug(request, playlist.playlist_name)
            new_follow = AccountFollowedPlaylists(account = account, playlist = playlist)
            new_follow.save()
            return redirect('userAccount')
    else:
        return redirect('userLogin')







def followingAlbums(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        try:
            account = Account.objects.get(username=logged_in_user)
            following_albums = AccountFollowedAlbums.objects.filter(account=account)
            return render(request, 'FollowingAlbums.html', {'account': account, 'followingAlbums': following_albums})
        except Account.DoesNotExist:
            return redirect('userLogin')
    else:
        return redirect('userLogin')


def unfollowAlbum(request, album_id):
    if request.method == 'POST':
        logged_in_user = request.session.get('logged_in_user')
        if logged_in_user:
            AccountFollowedAlbums.objects.filter(account__username=logged_in_user, album_id=album_id).delete()
    return redirect('followingPlaylists')
