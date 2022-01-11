from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from taggit.models import Tag

from .forms import CommentForm, PostForm
from .models import Comment, Post


class PostIndex(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(PostIndex, self).get_context_data(**kwargs)
        context["post_list"] = Post.objects.filter(status=1)
        context["tag_list"] = Tag.objects.all()
        return context


class SearchResults(ListView):
    model = Post
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Post.objects.filter(
            Q(status=1), Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        query = self.request.GET.get("q")
        context = super(SearchResults, self).get_context_data(**kwargs)
        context["tag_list"] = Tag.objects.all()
        context["page_title"] = query
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class DraftList(ListView):
    model = Post
    template_name = "draft_index.html"

    def get_context_data(self, **kwargs):
        context = super(DraftList, self).get_context_data(**kwargs)
        context["post_list"] = Post.objects.filter(status=0)
        context["tag_list"] = Tag.objects.all()
        return context


class SavedList(ListView):
    model = Post
    template_name = "saved_index.html"

    def get_context_data(self, **kwargs):
        context = super(SavedList, self).get_context_data(**kwargs)
        context["post_list"] = Post.objects.filter(saves=self.request.user)
        context["tag_list"] = Tag.objects.all()
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"
    success_url = "/"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.slug = slugify(post.title)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name="dispatch")
class PostEdit(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_edit.html"
    success_url = "/"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.slug = slugify(post.title)
        post.save()
        return super().form_valid(form)


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["comment_form"] = CommentForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        comment = Comment(
            body=request.POST.get("body"),
            author=self.request.user,
            post=self.get_object(),
        )
        comment.save()
        return self.get(self, request, *args, **kwargs)


def save_post(request, **kwargs):
    user = request.user
    post = Post.objects.get(slug=kwargs["slug"])
    if not post.saves.filter(id=request.user.id).exists():
        post.saves.add(user)
        post.save()
        return render(request, "partials/saves_area.html", context={"post": post})
    else:
        post.saves.remove(user)
        post.save()
        return render(request, "partials/saves_area.html", context={"post": post})


class TagList(ListView):
    model = Post
    template_name = "tag_index.html"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return Post.objects.filter(status=1, tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context["tag_list"] = Tag.objects.all()
        context["page_title"] = self.tag
        return context


@method_decorator(login_required, name="dispatch")
class SettingsIndex(TemplateView):
    template_name = "settings.html"
