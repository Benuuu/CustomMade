from django import forms

class BrandedTweetForm(forms.Form):
    max_len = 140
    # both keyup and keydown because keypress doesn't detect delete
    attrs={'size':140,
           'onkeyup': 'return textCounter(this, this.form.counter, %d);' % max_len,
           'onkeydown': 'return textCounter(this, this.form.counter, %d);' % max_len
          }
    content = forms.CharField(max_length=max_len, widget=forms.TextInput(attrs=attrs))
