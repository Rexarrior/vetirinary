"""URL configuration for the veterinary clinic project."""

from django.contrib import admin
from django.urls import include, path

from . import health, views


urlpatterns = [
    path("ready/", health.readiness, name="readiness"),
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("services/", include("services.urls")),
    path("reviews/", include("reviews.urls")),
    path("news/", include("news.urls")),
    path("contacts/", include("contacts.urls")),
    path("about/", include("about.urls")),
    path("api/chatbot/", include("chatbot.urls")),
]
