from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import (Channel, FavouriteChannel, Match, Programme, Profile, Rental, Review, ScheduleItem,
                     SubscriptionPlan, UserSubscription, ViewingHistory, WatchlistItem)


def home(request):
    programmes = Programme.objects.all()
    watchlist = WatchlistItem.objects.filter(user=request.user).select_related("programme") if request.user.is_authenticated else []
    favourites = set(FavouriteChannel.objects.filter(user=request.user).values_list("channel_id", flat=True)) if request.user.is_authenticated else set()
    return render(request, "stream/home.html", {
        "featured": programmes.filter(is_featured=True)[:3],
        "trending": programmes[:8],
        "channels": Channel.objects.all()[:8],
        "schedule": ScheduleItem.objects.filter(ends_at__gte=timezone.now()).select_related("channel", "programme")[:6],
        "watchlist": watchlist[:4],
        "favourites": favourites,
    })


def watch(request, slug):
    programme = get_object_or_404(Programme, slug=slug)
    if request.user.is_authenticated:
        WatchlistItem.objects.update_or_create(user=request.user, programme=programme)
        ViewingHistory.objects.update_or_create(user=request.user, programme=programme)
    return render(request, "stream/watch.html", {"programme": programme})


def search(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    results = Programme.objects.all()
    if query:
        results = results.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        results = results.filter(programme_type=category)
    return render(request, "stream/search.html", {"query": query, "results": results})


@login_required
def account(request):
    return render(request, "stream/account.html", {
        "watchlist": WatchlistItem.objects.filter(user=request.user).select_related("programme"),
        "history": ViewingHistory.objects.filter(user=request.user).select_related("programme")[:8],
        "profiles": Profile.objects.filter(user=request.user),
        "subscriptions": UserSubscription.objects.filter(user=request.user, is_active=True).select_related("plan"),
        "rentals": Rental.objects.filter(user=request.user).select_related("programme")[:8],
    })


def sports(request):
    return render(request, "stream/sports.html", {"matches": Match.objects.select_related("league", "home_team", "away_team")[:20]})


@login_required
@require_POST
def review(request, programme_id):
    rating = int(request.POST.get("rating", 0))
    if rating not in range(1, 6):
        return JsonResponse({"error": "Rating must be between 1 and 5."}, status=400)
    item, _ = Review.objects.update_or_create(
        user=request.user, programme_id=programme_id,
        defaults={"rating": rating, "comment": request.POST.get("comment", "")},
    )
    return JsonResponse({"rating": item.rating})


@login_required
@require_POST
def toggle_watchlist(request, programme_id):
    item, created = WatchlistItem.objects.get_or_create(user=request.user, programme_id=programme_id)
    if not created:
        item.delete()
    return JsonResponse({"saved": created})


@login_required
@require_POST
def toggle_favourite(request, channel_id):
    item, created = FavouriteChannel.objects.get_or_create(user=request.user, channel_id=channel_id)
    if not created:
        item.delete()
    return JsonResponse({"saved": created})
