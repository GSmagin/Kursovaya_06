from django.contrib import admin
from blog.models import BlogMod


# Register your models here.
@admin.register(BlogMod)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "created_at", "is_published", "views_count", "author")
    search_fields = ("title", "content")
