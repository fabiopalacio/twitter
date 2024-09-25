from django import forms  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from utils.utils_form import add_placeholder


class PostForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['content'], 'No que está pensando?')

    content = forms.CharField(
        max_length=250, required=True, widget=forms.Textarea(attrs={
            'rows': 3,
            'cols': 45,
            'class': 'form-control w-100 text-area',
        }), label='Tweet')


class CommentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['content'], 'Digite seu comentário...')

    content = forms.CharField(
        max_length=250, required=True, widget=forms.Textarea(attrs={
            'rows': 3,
            'cols': 45,
            'class': 'form-control w-100 text-area',
        }), label='Comentário')
