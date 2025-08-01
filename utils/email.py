from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, from_email=None, to_email=None):
    to_email = to_email if isinstance(to_email, list) else [to_email]
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, to_email)