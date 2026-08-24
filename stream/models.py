from django.conf import settings
from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    number = models.PositiveIntegerField(unique=True)
    category = models.CharField(max_length=60, default="General")
    logo_url = models.URLField(blank=True)
    stream_url = models.URLField(blank=True, help_text="HLS or compatible stream URL")
    is_live = models.BooleanField(default=True)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"{self.number} | {self.name}"


class Programme(models.Model):
    TYPE_CHOICES = [("show", "Show"), ("movie", "Movie"), ("sport", "Sport"), ("kids", "Kids")]
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    programme_type = models.CharField(max_length=12, choices=TYPE_CHOICES, default="show")
    image_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=45)
    is_featured = models.BooleanField(default=False)
    is_downloadable = models.BooleanField(default=False)
    age_rating = models.CharField(max_length=12, default="PG")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.title


class ScheduleItem(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="schedule")
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    class Meta:
        ordering = ["starts_at"]


class WatchlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist")
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    progress_seconds = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "programme"], name="unique_watchlist_item")]


class FavouriteChannel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "channel"], name="unique_favourite_channel")]
