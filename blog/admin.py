from django.contrib import admin
from .models import Post, Comment

# Customizations of post in admin panel

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'author')
    list_editable = ('status',)
    search_fields = ('author', 'title') 
    prepopulated_fields = {'slug' : ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

# Customizations of comments in admin panel 

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'post', 'is_active')
    list_filter = ('post', 'is_active')
    list_editable = ('is_active', )
    search_fields = ('name', 'email')
    ordering = ('-created', )

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
