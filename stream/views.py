from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Channel, FavouriteChannel, Programme, ScheduleItem, WatchlistItem


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
    return render(request, "stream/watch.html", {"programme": programme})


def search(request):
    query = request.GET.get("q", "").strip()
    results = Programme.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)) if query else Programme.objects.none()
    return render(request, "stream/search.html", {"query": query, "results": results})


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
