from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'post_file')


class CommentForm(forms.Form):

    author_name = forms.CharField(
        label="",
        widget=forms.Textarea
    )

    comment_area = forms.CharField(
        label="",
        widget=forms.Textarea
    )
