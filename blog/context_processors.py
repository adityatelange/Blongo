from blog.models import BlogConfig


def blog_settings(request):
    blog_setting = BlogConfig.objects.all().first()
    return {
        "blog_conf": blog_setting
    }
