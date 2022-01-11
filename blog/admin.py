from django.contrib import admin
from markdownx.models import MarkdownxField
from markdownx.widgets import AdminMarkdownxWidget

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_on")
    list_filter = ("status", "updated_on", "created_on")
    search_fields = ["title", "content", "tags"]
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        MarkdownxField: {"widget": AdminMarkdownxWidget},
    }


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "date_posted", "time_since")
    list_filter = ("post", "author", "date_posted")
    search_fields = ["post", "author", "body"]
    formfield_overrides = {
        MarkdownxField: {"widget": AdminMarkdownxWidget},
    }


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
