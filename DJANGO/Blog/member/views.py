from django.conf import settings
#from config import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.urls import reverse

def sign_up(request):
    # print(request.POST)
    # username = request.POST.get('username')
    # password1 = request.POST.get('password1')
    # password2 = request.POST.get('password2')

    #username 중복 확인 작업
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()
    """
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    #password 정책 확인
    context = {
        'form' : form,
    }
    return render(request, template_name='registration/signup.html', context=context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(reverse('blog_list'))

    context = {
        'form' : form
    }

    return  render(request, template_name='registration/login.html', context=context)

