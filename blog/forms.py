from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Comment
from taggit.forms import TagWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "title", "tags", "content", "status"]
        labels = {
            "image": _(""),
            "title": _(""),
            "tags": _(""),
            "content": _(""),
            "status": _(""),
        }
        widgets = {
            "image": forms.TextInput(attrs={"placeholder": "Image URL"}),
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "tags": TagWidget(),
            # "tags": forms.TextInput(attrs={"placeholder": "python, javascript, cpp"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {
            "body": _(""),
        }
