from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import RedirectView

from . import feeds
from . import views
from .sitemaps import SitemapView, PostSitemapView

sitemaps = {
    'static': SitemapView,
    'post': PostSitemapView
}
urlpatterns = [
    # path("", views.Index.as_view(), name='index'),
    path("", views.AllBlogPost.as_view(), name='index'),
    # path("all-blog-posts/", views.AllBlogPost.as_view(), name='all_blog_posts'),
    path("about/", views.About.as_view(), name='about'),
    path("search/", views.BlogSearch.as_view(), name='search'),

    # archive views
    path('<int:year>/<str:month>/<int:day>/',
         views.BlogPerDay.as_view(),
         name="archive-day"),
    path('<int:year>/<str:month>/',
         views.BlogPerMonth.as_view(),
         name="archive-month"),
    path('<int:year>/', views.BlogPerYear.as_view(), name="archive-year"),

    # tag views
    path("tag/<slug:tag>", views.TagArchive.as_view(), name="tag", ),
    path("tag/", RedirectView.as_view(url='all'), name='tag/all'),

    # author views
    path("author/<slug:author>", views.AuthorArchive.as_view(), name="author", ),
    path("author/", RedirectView.as_view(url='all'), name='author/all'),

    # feed
    path('rss/', feeds.LatestPostsFeed(), name='feeds'),

    # sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    # detail post view
    path('<slug:slug>/', views.BlogPostDetail.as_view(), name='post_detail'),

]
