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
    genre = models.CharField(max_length=80, blank=True, help_text="For example: Drama, Comedy, Documentary")
    image_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to="videos/%Y/%m/", blank=True, help_text="Upload an MP4 or browser-compatible video file")
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


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles")
    name = models.CharField(max_length=80)
    is_kids = models.BooleanField(default=False)
    pin = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.user.username} | {self.name}"


class ViewingHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="viewing_history")
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    progress_seconds = models.PositiveIntegerField(default=0)
    watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-watched_at"]
        constraints = [models.UniqueConstraint(fields=["user", "programme"], name="unique_viewing_history")]


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2)
    max_devices = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    starts_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class PaymentTransaction(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    provider = models.CharField(max_length=40, default="manual")
    provider_reference = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "programme"], name="unique_review")]


class Rental(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rented_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


class Season(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name="seasons")
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=120, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["programme", "number"], name="unique_season_number")]


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    episode_number = models.PositiveIntegerField()
    video_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=45)

    class Meta:
        ordering = ["season__number", "episode_number"]
        constraints = [models.UniqueConstraint(fields=["season", "episode_number"], name="unique_episode_number")]


class League(models.Model):
    name = models.CharField(max_length=120)
    logo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=120)
    logo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="matches")
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_matches")
    starts_at = models.DateTimeField()
    home_score = models.PositiveIntegerField(null=True, blank=True)
    away_score = models.PositiveIntegerField(null=True, blank=True)
    stream_url = models.URLField(blank=True)
    is_live = models.BooleanField(default=False)

    class Meta:
        ordering = ["starts_at"]
