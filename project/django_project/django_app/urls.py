
from django.urls import path
from django_app import views

urlpatterns = [
    path('', views.get_weather, name = 'weather'),
    path('youtube/', views.youtube, name='youtube'),
    path('instagram/', views.instagram, name='instagram'),

]