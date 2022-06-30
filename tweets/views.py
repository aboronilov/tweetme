import random
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from tweets.forms import TweetForm

from tweets.models import Tweet

def home_view(request, *args, **kwargs):
   return render(request, 'pages/home.html', status=200)

def tweet_create_view(request, *args, **kwargs):
   form = TweetForm(request.POST or None)
   context = {
      'form': form
      }
   if form.is_valid():
      obj = form.save(commit=False)
      obj.save()
      form = TweetForm()
   return render(request, 'components/form.html', context=context)      

def tweet_list_view(request, *args, **kwargs):
   objects = Tweet.objects.all()
   tweets_list = [{"id": obj.id, "content": obj.content, "likes": random.randint(0,120)} for obj in objects]
   data = {
      'isUser': False,
      'response': tweets_list
   }
   return JsonResponse(data)

def tweet_detail_view(requets, tweet_id, *args, **kwargs):
   data = {
      "tweet_id": tweet_id,
      # "image": obj.image.url,
   }
   status = 200
   try:
      obj = Tweet.objects.get(pk=tweet_id)
      data["content"] = obj.content
   except:
      data['message'] = 'Not found'
      status = 404
      raise Http404(f"No item in DB with {tweet_id}")

   return JsonResponse(data, status=status)
