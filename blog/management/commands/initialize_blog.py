from django.core.management.base import BaseCommand

from blog.models import BlogConfig


class Command(BaseCommand):
    help = 'Adds Default Blog Config (Can be used to Reset Blog Settings) '

    def handle(self, *args, **kwargs):
        default_cfg = BlogConfig()
        default_cfg.save()
        self.stdout.write("Created default config for blog")
