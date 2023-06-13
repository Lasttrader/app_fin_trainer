from django import forms
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter
from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'categoryType',
            'postTitle',
            'postText',
            'upload',
        ]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('commentText',)


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('postTitle', 'postText')
