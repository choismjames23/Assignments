from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import reverse, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView

from post.forms import PostForm, PostImageFormSet, CommentForm
from post.models import Post, Like

User = get_user_model()

class PostListView(ListView):
    # select_related : Post 모델이 'user' 를 foreignkey로 가지고 있으면 사용 가능 ( sql join )
    # prefetch_related : 역참조 / many to many. PostImage 모델이 Post를 foreignkey로 연결되어있음
    # db 부하를 줄이기 위해서 위 두개를 사용한다.
    queryset = Post.objects.all().select_related('user').prefetch_related('images', 'comments', 'likes')
    template_name = 'post/list.html'
    paginate_by = 5
    ordering = ('-created_at',)

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['comment_form'] = CommentForm()
        return data

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = PostImageFormSet
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        image_formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if image_formset.is_valid():
            image_formset.save()

        return HttpResponseRedirect(reverse('main'))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = PostImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        self.object = form.save()

        image_formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if image_formset.is_valid():
            image_formset.save()

        return HttpResponseRedirect(reverse('main'))

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

@csrf_exempt
@login_required
def toggle_like(request):
    post_pk = request.POST.get('post_pk')
    if not post_pk:
        raise Http404

    post = get_object_or_404(Post, pk=post_pk)
    user = request.user

    like , created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        like.delete()

    return JsonResponse({'created': created})


def search(request):
    search_type = request.GET.get('type')
    q = request.GET.get('q', '')

    if search_type in ['user', 'tag'] and q:
        if search_type == 'user':
            object_list = User.objects.filter(nickname__icontains=q)
        else:
            object_list = Post.objects.filter(tags__tag=q)

        context = {
            'object_list':object_list
        }
        return render(request, f'search/search_{search_type}.html', context)

    return render(request, 'search/search.html')