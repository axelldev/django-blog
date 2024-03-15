"""Admin settings for blog app"""

from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Model admin for posts"""

    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ["title"]}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Model admin for post comments"""

    search_fields = ["name", "email", "body"]
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    raw_id_fields = ["post"]
    date_hierarchy = "created"
    ordering = ["active", "created"]
