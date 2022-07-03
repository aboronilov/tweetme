import random
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics, mixins

from tweets.forms import TweetForm
from tweets.models import Tweet
from tweets.serializers import TweetSerializer


def home_view(request, *args, **kwargs):
   return render(request, 'pages/home.html', status=200)

@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
   serializer = TweetSerializer(data=request.POST)
   if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user)
      return Response(serializer.data, status=201)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
   qs = Tweet.objects.filter(id=tweet_id)
   if not qs.exists():
      return Response({}, status=404)
   qs = qs.filter(user=request.user)
   if not qs.exists():
      return Response({"message": "You cannot delete this tweet"}, status=401)
   obj = qs.first()
   obj.delete()
   return Response({"message": "Tweet deleted"}, status=200)

# @api_view(['GET'])
# def tweet_list_view(request, *args, **kwargs):
#    tweets = Tweet.objects.all()
#    serializer = TweetSerializer(data=tweets, many=True)
#    if serializer.is_valid(raise_exception=True):
#       return Response(serializer.data, status=200, safe=False)

class TweetListRetrieveView(
   mixins.ListModelMixin,
   mixins.RetrieveModelMixin,
   generics.GenericAPIView
   ):

   queryset = Tweet.objects.all()
   serializer_class = TweetSerializer

   def get(self, request, *args, **kwargs):
      pk = kwargs.get("pk")
      if pk:
         return self.retrieve(request, *args, **kwargs)
      return self.list(request, *args, **kwargs)

def tweet_create_view_pure_django(request, *args, **kwargs):
   """
   REST API create view
   """
   user = request.user
   if not request.user.is_authenticated:
      user = None
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
         return JsonResponse({}, status=401)
      return redirect(settings.LOGIN_URL)
   form = TweetForm(request.POST or None)
   context = {
      'form': form
      }
   next_url = request.POST.get('next') or None
   if form.is_valid():
      obj = form.save(commit=False)
      obj.user = user
      obj.save()
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
         return JsonResponse(obj.serialize(), status=201)
      if next_url is not None and url_has_allowed_host_and_scheme(next_url, settings.ALLOWED_HOSTS):
         return redirect(next_url)
      form = TweetForm()
   if form.errors:
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
         return JsonResponse(form.errors, status = 400)
   return render(request, 'components/form.html', context=context)

def tweet_list_view_pure_django(request, *args, **kwargs):
   objects = Tweet.objects.all()
   tweets_list = [obj.serialize() for obj in objects]
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
