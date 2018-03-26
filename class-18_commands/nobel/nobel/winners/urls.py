"""nobel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

app_name = 'winners'
urlpatterns = [
    path('', views.home, name='home'),
    path('winners/', views.list_winners, name='winners-list'),
    path('winners/<int:pk>', views.winner, name='winners-detail'),
    path('countries/', views.list_countries, name='countries-list'),
    path('categories/', views.list_categories, name='categories-list'),
    path('categories/<slug:category>/', views.category_winners, name='category-winner-list'),
    path('api/', views.api, name='api'),
]
