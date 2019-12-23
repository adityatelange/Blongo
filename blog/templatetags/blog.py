from django import template

from ..models import Post, Tag

register = template.Library()


@register.inclusion_tag('blog/month_links_snippet.html')
def render_month_links():
    return {
        'dates': Post.objects.filter(active=True).dates('pub_date', 'month', order='DESC'),
    }


@register.inclusion_tag('blog/tag_links_snippet.html')
def render_tag_links():
    return {
        'tags': Tag.objects.filter(active=True)
    }

