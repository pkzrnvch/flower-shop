from django.contrib import admin
from django.urls import include, path

from flower_shop_app import views

app_name = 'flower_shop_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
]
