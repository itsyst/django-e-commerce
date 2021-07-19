from django.urls import path
from . import views


# UrlConfig
urlpatterns = [
    path('home/', views.home)
]
