from django.contrib import admin
from .models import (AccountSubType,
                     Account,
                     Artist,
                     Category,
                     Playlist,
                     Album,
                     Song,
                     AccountFollowedAlbums,
                     SongsInPlaylists,
                     AccountFollowedPlaylists,
                     AccountFollowedArtists)

admin.site.register(AccountSubType)
#admin.site.register(Account)
admin.site.register(Artist)
admin.site.register(Category)
admin.site.register(Playlist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(AccountFollowedAlbums)
admin.site.register(SongsInPlaylists)
admin.site.register(AccountFollowedPlaylists)
admin.site.register(AccountFollowedArtists)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('last_payment_date', 'next_payment_date')
        return self.readonly_fields
# Register your models here.
