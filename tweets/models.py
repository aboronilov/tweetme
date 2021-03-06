from django.conf import settings
from django.db import models
import random

class TweetLike(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
   timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
   parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   content = models.TextField(blank=True, null=True)
   likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='tweet_user', through=TweetLike)
   image = models.FileField(upload_to='images/', blank=True, null=True)
   timestamp = models.DateTimeField(auto_now_add=True)

   class Meta:
      ordering = ['-id']

   @property
   def is_retweet(self):
      return self.parent != None

