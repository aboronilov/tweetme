from django import forms

from tweets.models import Tweet


class TweetForm(forms.ModelForm):
   TWEET_MAX_LENGTH = 240

   class Meta:
      model = Tweet
      fields = ['content']

   def clean_content(self, *args, **kwargs):
      content = self.cleaned_data.get('content')
      if len(content) > self.TWEET_MAX_LENGTH:
         raise forms.ValidationError("This tweet is too long")
      return content
