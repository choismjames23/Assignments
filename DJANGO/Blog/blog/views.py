from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from blog.models import Blog
from blog.forms import BlogForm


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

    # 검색기능
    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) | # or 검색할 경우 | 사용
            Q(content__icontains=q)
        )
        # blogs = blogs.filter(title__icontains=q)
        # title : 제목 , content : 본문

    # 쿠키와 세션 실습
    # visits = int(request.COOKIES.get('visits', 0)) + 1
    # request.session['count'] = request.session.get('count', 0) + 1
    # 페이지네이터
    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    context = {
        #'blogs': blogs,
        'page_obj': page_object,
        'object_list': page_object.object_list,
        # 'count' : request.session['count']
    }
    response = render(request, template_name='blog_list.html', context=context)
    # response.set_cookie('visits', visits)
    return response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, template_name='blog_detail.html', context=context)


@login_required() #settings 의 LOGIN URL로 redirect
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False) # 실제로 db에 커밋을 하지 않고 일단 생성만 함
        blog.author = request.user     # 현재 로그인한 유저의 이름을 author에 저장
        blog.save()
        # author_id를 pk로 넘겨주기 위해 keyword argument로 딕녀서리를 넘겨줌
        return redirect(reverse('fb:detail',kwargs={'pk': blog.pk}))


    context = {'form':form}
    return render(request, template_name='blog_create.html', context=context)
@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    # if request.user != blog.author:
    #     raise Http404

    # form 안에 instance를 추가하여 기존에 있던 데이터를 함께 가져온다
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        blog = form.save()
        return redirect(reverse('fb:detail', kwargs={'pk': blog.pk}))

    context = {
        'form': form,
    }
    return render(request, template_name='blog_update.html', context=context)

@login_required()
@require_http_methods(['POST'])
def blog_delete(request, pk):
    # if request.method != 'POST':
    #     raise Http404

    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('fb:list'))
