from typing import Union, List

from django.conf import settings
from django.core.mail import send_mail

def send_email(subject, message, to_email: Union[str, List[str]]):
    # 리스트가 아닐 경우 리스트로 만들어주기
    to_email = to_email if isinstance(to_email, list) else [to_email, ]

    send_mail(subject, message, settings.EMAIL_HOST_USER, to_email)
