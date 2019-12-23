from django.contrib.syndication.views import Feed

from blog.models import Post


class LatestPostsFeed(Feed):
    title = "Latest Blog Posts"
    link = "/rss/"

    def items(self):
        return Post.objects.filter(active=True).order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.headline

    def item_pubdate(self, item):
        return item.pub_date

    def item_author_name(self, item):
        return item.author

    def item_description(self, item):
        return item.summary
