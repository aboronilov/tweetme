from django.conf import settings
from rest_framework import serializers

from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
   class Meta:
      model = Tweet
      fields = ['content']

   def valdate_content(self, value):
      if len(value) > settings.TWEET_MAX_LENGTH:
         raise serializers.ValidationError("The tweet is too long")
      return value
