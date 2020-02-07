from django.urls import path, include
from account import views


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('restricted', views.restricted),
    path('send_money', views.send_money),
    path('create_group', views.create_group)
]