from django.urls import path

from . import views

urlpatterns = [
    path("return/", views.return_view, name="return"),
    path("webhook/", views.webhook_view, name="webhook"),
]
