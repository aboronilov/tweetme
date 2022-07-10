"""tweetme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from .views import TweetListAPIview, TweetMixinView, TweetRetrieveAPIview, home_view, tweet_action_view, tweet_create_view, tweet_detail_view, TweetListRetrieveView, tweet_delete_view

urlpatterns = [
    path('', TweetListAPIview.as_view()),
    # path('create/', tweet_create_view),
    # path('<int:pk/', TweetRetrieveAPIview.as_view()),
    # path('<int:pk>/delete/', tweet_delete_view)
]
