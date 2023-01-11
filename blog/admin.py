from django.contrib import admin
from. models import Post, Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status']
    list_editable = ['status']
    list_filter = ['author', 'status']
    raw_id_fields = ['author']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy ='publish'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']