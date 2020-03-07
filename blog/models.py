from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class TagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Tag(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    active = models.BooleanField(default=True)

    objects = TagManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.slug


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.active().filter(created_on__lte=timezone.now())

    def active(self):
        return self.filter(active=True)


class Post(models.Model):
    headline = models.CharField(max_length=200, unique=True, help_text="Headline for the Post")
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE, related_name='blog_posts')
    summary = models.TextField(blank=True, max_length=200)
    cover = models.ImageField(upload_to='cover_images/')
    body = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField(
        verbose_name=_("Publication date"),
    )
    slug = models.SlugField(max_length=200, unique=True, help_text=_(
        "This is what the URI looks like " "ex. https://yourwebsite.com/slug"))
    active = models.BooleanField(
        help_text=_(
            "Tick to make this entry live. "
            "inactive entries whereas the general public aren't."
        ),
        default=True,
    )
    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }
        return reverse('post_detail', kwargs=kwargs)

    def view_incr(self):
        self.views += 1
        self.save(update_fields=['views'])


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class BlogConfig(models.Model):
    blog_name = models.CharField(max_length=16, default='BlogName')
    bootswatch_theme = models.URLField(
        help_text=_(mark_safe(
            'Paste BootsWatch theme URL here'
            ' <a target="_blank" href="https://www.bootstrapcdn.com/bootswatch/">GET THEME URL</a>'
        )),
        default="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css")

    about_us = models.TextField()

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog_name

    class Meta:
        verbose_name_plural = 'BlogConfig'
