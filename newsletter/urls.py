from django.urls import path

from . import views

urlpatterns = [
    path("subscribe/", views.subscribe, name="subscribe"),
    path("subscribe/confirm/", views.confirm, name="confirm"),
    path("unsubscribe/", views.unsubscribe, name="unsubscribe"),
]
