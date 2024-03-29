"""daydash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from daydashapi.views import login, register, EventView, FriendView, TagView, WeatherView, CommentView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'events', EventView, 'event')
router.register(r'friends', FriendView, 'friend')
router.register(r'tags', TagView, 'tag')
router.register(r'weather', WeatherView, 'weather')
router.register(r'comments', CommentView, 'comment')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register),
    path('login', login),
    path('admin/', admin.site.urls),
]
