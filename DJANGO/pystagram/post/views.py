from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic import ListView, CreateView, UpdateView

from post.forms import PostForm, PostImageFormSet
from post.models import Post


class PostListView(ListView):
    # select_related : Post 모델이 'user' 를 foreignkey로 가지고 있으면 사용 가능 ( sql join )
    # prefetch_related : 역참조 / many to many. PostImage 모델이 Post를 foreignkey로 연결되어있음
    # db 부하를 줄이기 위해서 위 두개를 사용한다.
    queryset = Post.objects.all().select_related('user').prefetch_related('images')
    template_name = 'post/list.html'
    paginate_by = 5
    ordering = ('-created_at',)


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