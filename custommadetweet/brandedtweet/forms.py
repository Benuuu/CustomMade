from django import forms

class BrandedTweetForm(forms.Form):
    content = forms.CharField(max_length=140)
