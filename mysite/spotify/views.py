from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from django.contrib import messages

from .models import AccountSubType, Category, Account, Playlist, Artist, Album, AccountFollowedAlbums, AccountFollowedPlaylists



# Create your views here.

def index(request):
    return render(request, 'Index.html')

def about_index(request):
    return render(request, 'About_index.html')

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





def about_account(request):
    return render(request, 'About_Account.html')

def userAccount(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        try:
            account = Account.objects.get(username=logged_in_user)
            created_playlists = Playlist.objects.filter(creator_account=account)
            return render(request, 'UserAccount.html', {'account': account,
                                                        'created_playlists': created_playlists})
        except Account.DoesNotExist:
            return redirect('userLogin')
    else:
        return redirect('userLogin')


def deletePlaylist(request, playlist_id):
    if request.method == 'POST':
        playlist = Playlist.objects.get(pk=playlist_id)
        playlist.delete()
    return redirect('userAccount')


def openCreatePlaylist(request):
    categories = Category.objects.all()
    return render(request, 'CreatePlaylist.html', {'categories':categories})

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

def openNewFollowPlaylist(request):
    logged_in_user = request.session.get('logged_in_user')
    account = Account.objects.get(username=logged_in_user)
    available_playlists = Playlist.objects.exclude(accountfollowedplaylists__account=account).exclude(creator_account=account)
    return render(request, 'FollowNewPlaylist.html', {'availablePlaylists':available_playlists})

def followPlaylist(request):
    logged_in_user = request.session.get('logged_in_user')
    playlist_id_req = request.POST.get('playlist_id')
    if logged_in_user:
        if request.method == 'POST':
            account = Account.objects.get(username = logged_in_user)
            playlist = Playlist.objects.get(playlist_id = playlist_id_req)
            new_follow = AccountFollowedPlaylists(account = account, playlist = playlist)
            new_follow.save()
            return redirect('followingPlaylists')
    else:
        return redirect('userLogin')







def followingAlbums(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        try:
            account = Account.objects.get(username=logged_in_user)
            following_albums = AccountFollowedAlbums.objects.filter(account=account)
            return render(request, 'FollowingAlbums.html', {'account': account,
                                                            'followingAlbums': following_albums})
        except Account.DoesNotExist:
            return redirect('userLogin')
    else:
        return redirect('userLogin')



def unfollowAlbum(request, album_id):
    if request.method == 'POST':
        logged_in_user = request.session.get('logged_in_user')
        if logged_in_user:
            AccountFollowedAlbums.objects.filter(account__username=logged_in_user, album_id=album_id).delete()
    return redirect('followingAlbums')


def openNewFollowAlbum(request):
    logged_in_user = request.session.get('logged_in_user')
    account = Account.objects.get(username=logged_in_user)
    available_albums = Album.objects.exclude(accountfollowedalbums__account=account)
    return render(request, 'FollowNewAlbum.html', {'availableAlbums':available_albums})


def followAlbum(request):
    logged_in_user = request.session.get('logged_in_user')
    album_id_req = request.POST.get('album_id')
    if logged_in_user:
        if request.method == 'POST':
            f_account = Account.objects.get(username=logged_in_user)
            f_album = Album.objects.get(album_id = album_id_req)
            new_follow = AccountFollowedAlbums(account = f_account, album = f_album)
            new_follow.save()
            return redirect('followingAlbums')
    else:
        return redirect('userLogin')





def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone = request.POST.get('phone')
        sub_type_id = request.POST.get('sub_type')

        # Získání typu účtu z ID
        sub_type = AccountSubType.objects.get(pk=sub_type_id)

        # Vytvoření nového účtu
        new_account = Account.objects.create(
            username=username,
            email=email,
            password=password,
            name=name,
            surname=surname,
            phone=phone,
            acc_sub_type=sub_type
        )

        # Přesměrování na přihlašovací stránku
        return redirect('userLogin')

    else:
        sub_types = AccountSubType.objects.all()
        return render(request, 'CreateAccount.html', {'sub_types': sub_types})