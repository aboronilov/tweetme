from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse

from tweets.models import Tweet

def home_view(request, *args, **kwargs):
   return render(request, 'pages/home.html', status=200)

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
