from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import commit
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from blog.models import Blog

class BlogListView(ListView):
    model = Blog
    queryset = Blog.objects.all().order_by('-created_at')
    # ordering = ('-created_at',)
    template_name = 'blog_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50)
    #
    # def get_object(self, queryset=None):
    #     object = super().get_object()
    #     object = self.model.objects.get(pk=self.kwargs.get('pk'))
    #
    #     return object
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'CBV'
    #     return context

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog_create.html'
    fields = ('title', 'category', 'content')
    # success_url = reverse_lazy('cb_blog_detail')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


    # model에서 get_absolute_url method를 설정하여 아래 부분은 필요가 없다.
    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    fields = ('title', 'category', 'content')
    # 글쓴이와 로그인 한 사람이 같은지 확인하는 부분
    # 방법 1
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff: # .is_superuser
            return queryset
        return queryset.filter(author=self.request.user)
    # 방법 2
    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.author != self.request.user:
    #          raise Http404
    #
    #     return self.object


    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff: # .is_superuser
            return queryset
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:list')