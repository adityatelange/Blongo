from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.defaults import page_not_found, server_error
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.dates import (
    ArchiveIndexView, DayArchiveView, MonthArchiveView,
    YearArchiveView,
)

from .models import Post, Tag


class Index(TemplateView):
    template_name = 'index.html'
    paginate_by = 2


class BlogViewMixin:
    date_field = 'pub_date'
    paginate_by = 4

    def get_queryset(self):
        posts = Post.objects.filter(active=True)
        return posts


class AllBlogPost(BlogViewMixin, ArchiveIndexView):
    allow_empty = True
    template_name = 'blog/blog_posts_all.html'
    make_object_list = True


class BlogPerDay(BlogViewMixin, DayArchiveView):
    template_name = 'blog/blog_posts_day.html'
    pass


class BlogPerMonth(BlogViewMixin, MonthArchiveView):
    template_name = 'blog/blog_posts_month.html'


class BlogPerYear(BlogViewMixin, YearArchiveView):
    template_name = 'blog/blog_posts_year.html'
    make_object_list = True


class BlogPostDetail(generic.DetailView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    queryset = Post.objects.active()
    model = Post
    template_name = 'blog/blog_post_detail.html'

    def get_object(self, queryset=queryset):
        obj = super(BlogPostDetail, self).get_object()
        obj.view_incr()
        self.object = obj
        return self.object


class TagArchive(ArchiveIndexView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag = None

    date_field = 'pub_date'
    allow_empty = True
    make_object_list = True
    paginate_by = 4
    template_name = 'blog/blog_posts_common_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagArchive, self).get_context_data(**kwargs)
        if self.tag:
            context['custom_data_heading'] = 'Posts for #{}'.format(self.tag.slug)
        else:
            context['custom_data_heading'] = 'All Posts'
        return context

    def get_queryset(self):
        tag = self.kwargs["tag"]
        if tag != "all":
            self.tag = get_object_or_404(Tag, slug=tag, active=True)

        if self.tag:
            posts = Post.objects.filter(Q(active=True) & Q(tags=self.tag))
        else:
            posts = Post.objects.filter(Q(active=True))
        return posts


class AuthorArchive(ArchiveIndexView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.author = None

    date_field = 'pub_date'
    allow_empty = True
    make_object_list = True
    paginate_by = 4
    template_name = 'blog/blog_posts_common_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuthorArchive, self).get_context_data(**kwargs)
        if self.author:
            context['custom_data_heading'] = 'Posts by {}'.format(self.author)
        else:
            context['custom_data_heading'] = 'All Posts'

        return context

    def get_queryset(self):
        author = self.kwargs["author"]
        if author != "all":
            self.author = get_object_or_404(User, username=author, is_active=True)

        if self.author:
            posts = Post.objects.filter(Q(active=True) & Q(author=self.author))
        else:
            posts = Post.objects.filter(Q(active=True))
        return posts


class BlogSearch(ListView):
    model = Post
    paginate_by = 4
    template_name = 'blog/search_results.html'

    def get_context_data(self, **kwargs):
        context = super(BlogSearch, self).get_context_data(**kwargs)
        try:
            q = self.request.GET.get('q')
            q = q.replace(" ", "+")
            context['query'] = q
        except AttributeError:
            context['query'] = ""
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            posts = Post.objects.filter(
                Q(headline__icontains=query) |
                Q(summary__icontains=query) &
                Q(active=True)
            )
        else:
            posts = Post.objects.filter(Q(active=True))
        return posts


class About(TemplateView):
    template_name = 'about.html'


def handler404(request, exception):
    return page_not_found(request=request, exception=exception, template_name="error/404.html")


def handler500(request):
    return server_error(request=request, template_name="error/500.html")
