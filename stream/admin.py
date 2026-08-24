from django.contrib import admin
from .models import (Channel, Episode, FavouriteChannel, League, Match, Programme, Profile, Rental, Review,
					 ScheduleItem, Season, SubscriptionPlan, Team, UserSubscription, ViewingHistory, WatchlistItem)

admin.site.register([Channel, Programme, ScheduleItem, WatchlistItem, FavouriteChannel, Profile, ViewingHistory,
					 SubscriptionPlan, UserSubscription, Review, Rental, Season, Episode, League, Team, Match])
