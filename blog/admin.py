from django.contrib import admin

from .models import Post, Tag, BlogConfig
from trix.admin import TrixAdmin

admin.site.site_header = "Blog Admin"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Welcome to Blog Admin Dashboard"


class PostAdmin(TrixAdmin, admin.ModelAdmin):
    list_display = ('headline', 'views', 'slug', 'active', 'pub_date')
    list_filter = ("active", "pub_date",)
    search_fields = ['headline', 'body']
    prepopulated_fields = {'slug': ('headline',)}
    autocomplete_fields = ("tags",)
    trix_fields = ('body',)

    actions = ["mark_active", "mark_inactive"]

    def mark_active(self, request, queryset):
        queryset.update(active=True)

    def mark_inactive(self, request, queryset):
        queryset.update(active=False)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_filter = ("active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug", "name"]


class BlogConfigAdmin(admin.ModelAdmin):
    list_display = ("blog_name", "bootswatch_theme")


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BlogConfig, BlogConfigAdmin)
