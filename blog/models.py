from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager
import math
import readtime

STATUS = ((0, "Draft"), (1, "Publish"))


class Post(models.Model):
    image = models.URLField(null=True)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = TaggableManager()
    content = MarkdownxField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def formatted_markdown(self):
        return markdownify(self.content)

    def readtime(self):
        result = readtime.of_text(self.content)
        return result.text

    def created_on_pretty(self):
        return self.created_on.strftime("%e %b, %Y")

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": str(self.slug)})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = MarkdownxField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def formatted_markdown(self):
        return markdownify(self.body)

    def date_posted_pretty(self):
        return self.date_posted.strftime("%e %b, %Y")

    def time_since(self):
        now = timezone.now()
        diff = now - self.date_posted

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

    def __str__(self):
        return self.body
