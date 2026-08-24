from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("watch/<slug:slug>/", views.watch, name="watch"),
    path("search/", views.search, name="search"),
    path("account/", views.account, name="account"),
    path("sports/", views.sports, name="sports"),
    path("plans/", views.plans, name="plans"),
    path("payment/<int:plan_id>/", views.start_payment, name="start_payment"),
    path("analytics/", views.analytics, name="analytics"),
    path("profile/select/<int:profile_id>/", views.select_profile, name="select_profile"),
    path("progress/<int:programme_id>/", views.save_progress, name="save_progress"),
    path("review/<int:programme_id>/", views.review, name="review"),
    path("watchlist/toggle/<int:programme_id>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("favourite/toggle/<int:channel_id>/", views.toggle_favourite, name="toggle_favourite"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
