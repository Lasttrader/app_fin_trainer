from django import forms
from django_filters import FilterSet, ModelMultipleChoiceFilter,DateTimeFilter
from .models import Post, Category

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'postTitle',
           'postText',
           'slug']