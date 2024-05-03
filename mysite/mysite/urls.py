"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from spotify import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('userLogin', views.userLogin, name='userLogin'),
    path('userAccount', views.userAccount, name='userAccount'),
    path('deletePlaylist/<int:playlist_id>', views.deletePlaylist, name='deletePlaylist'),
    path('createPlaylist', views.createPlaylist, name='createPlaylist'),
    path('followingPlaylists', views.followingPlaylists, name='followingPlaylists'),
    path('unfollowPlaylist/<int:playlist_id>', views.unfollowPlaylist, name='unfollowPlaylist'),
    path('followPlaylist/<int:playlist_id>', views.followPlaylist, name='followPlaylist'),
    path('followingAlbums', views.followingAlbums, name='followingAlbums'),
    path('unfollowAlbum/<int:album_id>', views.unfollowAlbum, name='unfollowAlbum')
]
