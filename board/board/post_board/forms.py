from django import forms
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter
from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categoryType',
            'postCategory',
            'postTitle',
            'postText',
            'slug']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Добавьте ваш комментарий....'}))

    class Meta:
        model = Comment
        fields = ('commentText',)


class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Post
        fields = ('postTitle', 'postText')


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('postTitle', 'postText')
