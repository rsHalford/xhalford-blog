from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.urls import reverse


class RSSFeed(Feed):
    title = "xHalford Blog"
    link = ""
    description = "Latest articles published to xhalford.com, about all things software"

    def items(self):
        return Post.objects.filter(status=1)

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return item.formatted_markdown()

    def item_author_name(self, item):
        return item.author

    def item_pubdate(self, item):
        return item.created_on


class AtomFeed(RSSFeed):
    feed_type = Atom1Feed
    subtitle = RSSFeed.description
