from django.contrib import admin

from .models import Post, Comment, Like
# Register your models here.

class CommentAdmin(admin.TabularInline):
    model = Comment

class LikeAdmin(admin.TabularInline):
    model = Like

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentAdmin, LikeAdmin,
    ]

admin.site.register(Post, PostAdmin)
