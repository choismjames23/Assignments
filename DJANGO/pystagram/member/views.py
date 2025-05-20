from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from member.forms import SignupForm, LoginForm
from utils.email import send_email

User = get_user_model()

class SignupView(FormView):
    template_name = 'auth/signup.html'
    form_class = SignupForm
    # success_url = reverse_lazy('signup_done')

    def form_valid(self, form):
        user = form.save()
        # 이메일 발송
        # 암호화 과정
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        # print(signer_dump)
        # # 복호화 과정 1
        # decoded_user_email = signing.loads(signer_dump)
        # print(decoded_user_email)
        # # 복호화 과정 2
        # email = signer.unsign(decoded_user_email, max_age= 60*30) # 30분 시간제한 둘 수 있다.
        # print(email)

        # 이메일 인증 링크? 메일로 보내서 누르면 연결될 링크
        # ex) http://localhost:8000/verify/?code=adfadfan -> 배포할때는 로컬 호스트가 아니라 바꿔줘야한다.
        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/verify/?code={signer_dump}'
        if settings.DEBUG:
            print(url)
        else:
            subject = '[Pystagram] 이메일 인증을 완료해주세요'
            message = f'다음 링크를 클릭해주세요. <br><a href="{url}">url</a>'
            send_email(subject, message, user.email)

        return render(
            self.request,
            template_name='auth/signup_done.html',
            context={'user':user}
        )

def verify_email(request):
    code = request.GET.get('code', '')

    signer = TimestampSigner()
    try:
        decoded_user_email = signing.loads(code)
        email = signer.unsign(decoded_user_email, max_age=60*30)
    except (TypeError, SignatureExpired): # unsign 했을때 나오는 오류
        return render(request, 'auth/not_verified.html')

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active=True
    user.save()

    return redirect(reverse('login'))
    # return render(request, 'auth/email_verified_done.html', context={'user':user})


class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.user
        login(self.request, user)

        next_page = self.request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(self.get_success_url())
