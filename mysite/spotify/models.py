from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class AccountSubType(models.Model):
    sub_type_id = models.AutoField(primary_key=True)
    type_fee = models.DecimalField(max_digits=4, decimal_places=2)
    type_description = models.CharField(max_length=20)

    def __str__(self):
        return self.type_description

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=12)
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    last_payment_date = models.DateField(null=True, blank=True, editable=False)
    next_payment_date = models.DateField(null=True, blank=True, editable=False)
    acc_sub_type = models.ForeignKey(AccountSubType, on_delete=models.CASCADE, null=False, blank=False)


    def save(self, *args, **kwargs):
        if self.acc_sub_type_id is not None:
            if self.acc_sub_type.type_description == "Free":
                self.last_payment_date = None
                self.next_payment_date = None
            else:
                today = date.today()
                self.last_payment_date = today
                next_month = today + relativedelta(months=1)
                self.next_payment_date = next_month

            super().save(*args, **kwargs)

    def __str__(self):
        return self.username

@receiver(post_save, sender=Account)
def update_payment_dates(sender, instance, created, **kwargs):
    def update_payment_dates(sender, instance, created, **kwargs):
        if created:
            if instance.acc_sub_type.type_description == "Free":
                instance.last_payment_date = None
                instance.next_payment_date = None
            else:
                today = date.today()
                instance.last_payment_date = today
                next_month = today + relativedelta(months=1)
                instance.next_payment_date = next_month
            instance.save(update_fields=['last_payment_date', 'next_payment_date'])


class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist_name = models.CharField(max_length=30)
    artist_note = models.CharField(max_length=1000)
    artist_next_tour = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.artist_name

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)
    category_song_count = models.IntegerField(null=True, blank=True)
    category_playlist_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.category_name

class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    playlist_name = models.CharField(max_length=30)
    playlist_create_date = models.DateTimeField(auto_now_add=True)
    playlist_note = models.CharField(max_length=30, null=True, blank=True)
    playlist_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.playlist_name

class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_release_date = models.DateField()
    album_name = models.CharField(max_length=30)
    album_length = models.IntegerField(null=True, blank=True)
    album_song_count = models.IntegerField(null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.album_name

class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    song_name = models.CharField(max_length=30)
    song_length = models.IntegerField()
    song_played_count = models.IntegerField(null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.song_name

class AccountFollowedAlbums(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account.username} sleduje album {self.album.album_name}"

class SongsInPlaylists(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self):
        return f"Píseň {self.song.song_name} je v playlistu {self.playlist.playlist_name}"

class AccountFollowedPlaylists(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account.username} sleduje playlist {self.playlist.playlist_name}"

class AccountFollowedArtists(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account.username} sleduje umělce {self.artist.artist_name}"
