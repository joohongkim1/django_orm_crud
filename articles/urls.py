from django.urls import path
from . import views

# articles/___ 경로가 들어가면 된다.
urlpatterns = [
    path('create/', views.create),
    path('new/', views.new),
    path('index/', views.index),
]