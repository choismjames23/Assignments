from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Blog, Comment

admin.site.register(Comment)
class CommentInline(admin.TabularInline): # TabularInline -> 표로 만들어서 한 페이지에 표현해주기 위함
    model = Comment
    fields = ['content', 'author']
    extra = 1

@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ['content',]
    inlines = [
        CommentInline
    ]
