from django.urls import path

from books import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
]