from django.contrib import admin
from blog.models import BlogMod


# Register your models here.
@admin.register(BlogMod)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published", "views_count")
    list_display_links = ['title']
    search_fields = ['title', 'content']
    list_filter = ['is_published', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
