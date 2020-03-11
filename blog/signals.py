from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save
from django.dispatch import receiver

from blog.models import Post

THUMBNAIL_SIZE = (1600, 900)


@receiver(pre_save, sender=Post)
def generate_thumbnail(sender, instance, **kwargs):
    image = Image.open(instance.cover)
    image = image.convert("RGB")
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    temp_thumb = BytesIO()
    image.save(temp_thumb, "JPEG")
    temp_thumb.seek(0)
    # set save=False, otherwise it will run in an infinite loop
    instance.cover.save(instance.cover.name, ContentFile(temp_thumb.read()), save=False, )
    temp_thumb.close()
