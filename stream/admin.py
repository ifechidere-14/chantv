from django.contrib import admin
from .models import Channel, FavouriteChannel, Programme, ScheduleItem, WatchlistItem

admin.site.register([Channel, Programme, ScheduleItem, WatchlistItem, FavouriteChannel])
