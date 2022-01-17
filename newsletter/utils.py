import base64
import re

from cryptography.fernet import Fernet
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags


class Encryption:
    def __init__(self, key, message):
        self.key = key
        self.message = message

    def encrypt(self):
        message = self.message.encode("utf-8")
        message = Fernet(self.key).encrypt(message)
        message = base64.urlsafe_b64encode(message)
        message = message.decode("utf-8")
        return message

    def decrypt(self):
        message = base64.urlsafe_b64decode(self.message)
        message = Fernet(self.key).decrypt(message)
        message = message.decode("utf-8")
        return message


def validate_email(email):
    if email is None:
        return "Email is required"
    elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        return "Invalid Email Address"
    # elif email.split("@")[-1] in disposable_emails:
    #     return "Disposable emails are not allowed"
    else:
        return None


def send_mail(data):
    try:
        message = EmailMultiAlternatives(
            subject=data["subject"],
            body=data["text_content"],
            from_email=data["from_email"],
            to=data["to"],
        )
        message.attach_alternative(data["html_content"], "text/html")
        message.send()
        return True
    except Exception:
        return False


def subscription_email(email, confirmation_url):
    data = dict()
    data["confirmation_url"] = confirmation_url
    data["to"] = [email]
    data["subject"] = "Newsletter Confirmation"
    data["from_email"] = settings.EMAIL_HOST_USER
    template = get_template("emails/subscription.html")
    data["html_content"] = template.render(data)
    data["text_content"] = strip_tags(data["html_content"])
    return send_mail(data)
