from .models import User, Post, Likes, Follows
from django import forms

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets={'post': forms.Textarea(attrs={
            'cols': 50, 'rows': 3,
            'style': 'border-radius: 10px; margin:10px;  vertical-align: middle; font-size: large;',
            'placeholder': 'New Post', })    
        }
        exclude = ('user', 'date', 'like')
