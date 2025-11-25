# apps/posts/forms.py
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, label="Post anonymously")

    class Meta:
        model = Post
        fields = ['caption', 'image', 'video', 'anonymous']
        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 resize-none',
                'rows': 3,
                'placeholder': 'What\'s on your mind?'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500',
                'accept': 'video/*'
            }),
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments to posts."""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 resize-none',
                'rows': 2,
                'placeholder': 'Write a comment...'
            }),
        }
