from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import Subscriber
from .utils import Encryption, subscription_email, validate_email


def save_email(email):
    try:
        subscriber = Subscriber.objects.get(email=email)
    except ObjectDoesNotExist:
        subscriber = Subscriber(email=email)
    except Exception:
        return False

    subscriber.save()
    return True


def subscribe(request):
    if request.method == "POST":
        data = request.POST.copy()
        email = data.get("email", None)
        error_msg = validate_email(email)
        if error_msg:
            request.session["msg"] = error_msg
            request.session.set_expiry(0)
            return redirect("subscribe")

        save_status = save_email(email)

        if save_status:
            key = settings.ENCRYPT_KEY
            token = email + "+" + str(timezone.now)
            token = Encryption(bytes(key, "utf-8"), token).encrypt()
            confirmation_url = (
                request.build_absolute_uri(reverse("confirm")) + "?token=" + token
            )
            send_status = subscription_email(email, confirmation_url)
            if not send_status:
                subscriber = Subscriber.objects.get(email=email)
                subscriber.delete()
            else:
                msg = (
                    "Email sent to "
                    + email
                    + ".\nConfirm subscription with the link provided."
                )
                request.session["msg"] = msg
                return redirect("subscribe")
    else:
        return render(request, "partials/newsletter_area.html")


def confirm(request):
    if request.method == "POST":
        raise Http404

    token = request.GET.get("token", None)

    if not token:
        msg = "Invalid link."
        request.session["msg"] = msg
        request.session.set_expiry(0)
        return redirect("index")

    key = bytes(settings.ENCRYPT_KEY, "utf-8")
    token = Encryption(key, token).decrypt()
    if token:
        token = token.split("+")
        email = token[0]
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.confirmed = True
            subscriber.save()
            msg = "Subscription confirmed."
        except ObjectDoesNotExist:
            msg = "Invalid link."
    else:
        msg = "Invalid link."

    request.session["msg"] = msg
    request.session.set_expiry(0)
    return redirect("index")


def unsubscribe(request):
    if request.method == "POST":
        raise Http404

    token = request.GET.get("token", None)

    if not token:
        msg = "Invalid link."
        request.session["msg"] = msg
        request.session.set_expiry(0)
        return redirect("index")

    key = bytes(settings.ENCRYPT_KEY, "utf-8")
    token = Encryption(key, token).decrypt()
    if token:
        token = token.split("+")
        email = token[0]
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.delete()
            msg = (
                "Subscription deleted.\nIf this was a mistake, just resubscribe below."
            )
        except ObjectDoesNotExist:
            msg = "Invalid link."
    else:
        msg = "Invalid link."

    request.session["msg"] = msg
    request.session.set_expiry(0)
    return redirect("index")
