from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tweet
from rest_framework.test import APIClient

User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="test")
        self.user2 = User.objects.create(username="test2", password="test2")
        self.tweet_1 = Tweet.objects.create(
            content="test_tweet_1", user=self.user)
        self.tweet_2 = Tweet.objects.create(
            content="test_tweet_2", user=self.user)
        self.tweet_3 = Tweet.objects.create(
            content="test_tweet_3", user=self.user2)
        self.currentCount = Tweet.objects.count()

    def test_tweet_created(self):
        tweet = Tweet.objects.create(content="test_tweet_4", user=self.user)
        self.assertEqual(tweet.user, self.user)
        self.assertEqual(Tweet.objects.count(), 4)

    def get_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/',
                               {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        likes_count = response.json().get("likes")
        self.assertEqual(likes_count, 1)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/',
                               {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post('/api/tweets/action/',
                               {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        likes_count = response.json().get("likes")
        self.assertEqual(likes_count, 0)

    def test_action_retweet(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/',
                               {"id": 3, "action": "retweet"})
        self.assertEqual(response.status_code, 201)
        new_tweet_id = response.json().get('id')
        self.assertNotEqual(new_tweet_id, 3)
        self.assertEqual(self.currentCount + 1, new_tweet_id)
        
    def test_create_tweet_view(self):
        client = self.get_client()
        response = client.post('/api/tweets/create/',
                               {"content": "test_tweet_4", "user": self.user})
        self.assertEqual(response.status_code, 201)
        new_tweet_id = response.json().get('id')
        self.assertNotEqual(new_tweet_id, 3)
        self.assertEqual(self.currentCount + 1, new_tweet_id)
        
    def test_detail_api_view(self):
        client = self.get_client()
        response = client.get('/api/tweets/1/')
        self.assertEqual(response.status_code, 200)
        tweet_id = response.json().get("id")
        self.assertEqual(tweet_id, 1)

    def test_delete_api_view(self):
        client = self.get_client()
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 200)
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 404)
        response = client.delete('/api/tweets/3/delete/')
        self.assertEqual(response.status_code, 401)
