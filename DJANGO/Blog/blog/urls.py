from django.urls import path

from blog import cb_views

app_name = 'blog'

urlpatterns = [
    # CBV(Class Based View) Blog
    path('', cb_views.BlogListView.as_view(), name='list'),
    path('<int:blog_pk>/',cb_views.BlogDetailView.as_view(), name='detail'),
    path('create/', cb_views.BlogCreateView.as_view(), name='create'),
    path('<int:pk>/update/', cb_views.BlogUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', cb_views.BlogDeleteView.as_view(), name='delete'),

    path('comment/create/<int:blog_pk>/', cb_views.CommentCreateView.as_view(), name='comment_create'),
]

# include 하기 전 html 파일 -> {% url 'blog_list %}
# include 하고 나서는 이렇게 바꿔줘야 함 -> {% url blog:list %}