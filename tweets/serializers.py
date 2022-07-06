from django.conf import settings
from rest_framework import serializers

from .models import Tweet


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def action_validate(self, value):
        value = value.lower().strip()
        if not value in settings.TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError(
                f"Wrong action type. Action should be {settings.TWEET_ACTION_OPTIONS}")
        return value


class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj, *args, **kwargs):
        return obj.likes.count()

    def valdate_content(self, value):
        if len(value) > settings.TWEET_MAX_LENGTH:
            raise serializers.ValidationError("The tweet is too long")
        return value


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'is_retweet', 'parent']

    def get_likes(self, obj, *args, **kwargs):
        return obj.likes.count()

