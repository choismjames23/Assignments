from django.contrib import admin
from blog.models import Blog, Comment

admin.site.register(Comment)
class CommentInline(admin.TabularInline): # TabularInline -> 표로 만들어서 한 페이지에 표현해주기 위함
    model = Comment
    fields = ['content', 'author']
    extra = 1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]
