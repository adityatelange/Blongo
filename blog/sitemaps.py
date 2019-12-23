from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post


class SitemapView(Sitemap):
    def items(self):
        return ['about']

    def location(self, obj):
        return reverse(obj)


class PostSitemapView(Sitemap):
    def items(self):
        return Post.objects.filter(active=True)
