"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path, include, reverse
from django.views import View
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static

from blog import views, cb_views
from member import views as member_views


# class AboutView(TemplateView):
#     template_name = 'about.html'
#
# class TestView(View):
#     def get(self, request):
#         return render(request, template_name='test_get.html')
#
#     def post(self, request):
#         return render(request, template_name='test_post.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    # FBV(Function Based View) Blog
    # path('', views.blog_list, name='blog_list'),
    # path('blog/detail/<int:pk>/', views.blog_detail, name='blog_detail'),
    # path('create/',views.blog_create, name='blog_create'),
    # path('<int:pk>/update/', views.blog_update, name='blog_update'),
    # path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),

    # CBV(Class Based View) Blog
    # path('', cb_views.BlogListView.as_view(), name='blog_list'),
    # path('<int:pk>/',cb_views.BlogDetailView.as_view(), name='blog_detail'),
    # path('create/', cb_views.BlogCreateView.as_view(), name='blog_create'),
    # path('<int:pk>/update/', cb_views.BlogUpdateView.as_view(), name='blog_update'),
    # path('<int:pk>/delete/', cb_views.BlogDeleteView.as_view(), name='blog_delete'),

    path('', include('blog.urls')),
    path('fb/',include('blog.fbv_urls')),
    # auth
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/',member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),

    # path('about/', AboutView.as_view(template_name='about.html'), name='about'),
    # #path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    # path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
    # #path('redirect2/', lambda req: redirect(reverse('about'))),
    #
    # path('test/', TestView.as_view(), name='test'),

    # summernote
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

