import os

from PIL import Image
from django.conf import settings
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe


class IMUEditor(AdminFileWidget):
    """
        ref: https://www.djangosnippets.org/snippets/934/
        A FileField Widget that displays an image instead of a file path
        if the current file is an image.
    """

    def thumbnail(self, image_path):
        absolute_url = os.path.join(settings.MEDIA_URL, image_path)
        return u'<img src="%s" alt="%s" />' % (absolute_url, image_path)

    def render(self, name, value, attrs=None, renderer=None):

        output = []
        file_name = str(value)
        if file_name:
            try:  # is image
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                output.append(
                    '%s</a><br /> ' %
                    (self.thumbnail(file_name),))
            except IOError:  # not image
                pass

        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

    class Media:
        css = {'all': ('css/imu.css',)}
        js = ()
