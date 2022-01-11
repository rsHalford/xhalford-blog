from django.urls import path

from . import views
from .feeds import AtomFeed, RSSFeed

urlpatterns = [
    path("", views.PostIndex.as_view(), name="index"),
    path("search/", views.SearchResults.as_view(), name="search_results"),
    path("drafts/", views.DraftList.as_view(), name="drafts"),
    path("settings/", views.SettingsIndex.as_view(), name="settings"),
    path("create/", views.PostCreate.as_view(), name="post_create"),
    path("edit/<slug:slug>/", views.PostEdit.as_view(), name="post_edit"),
    path("saved/", views.SavedList.as_view(), name="saved"),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("tags/<slug:slug>/", views.TagList.as_view(), name="tag_index"),
    path("save/<slug:slug>/", views.save_post, name="save_post"),
    path("feed/rss", RSSFeed(), name="rss_feed"),
    path("feed/atom", AtomFeed(), name="atom_feed"),
]
