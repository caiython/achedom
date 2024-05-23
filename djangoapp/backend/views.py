from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .services.whatsapp import WHATSAPP
import logging


# Create your views here.
def start_wa(request: HttpRequest) -> HttpResponse:

    if WHATSAPP.is_running():
        return HttpResponseRedirect(reverse('config'))

    WHATSAPP.start()
    return HttpResponseRedirect(reverse('config'))


def stop_wa(request: HttpRequest) -> HttpResponse:

    if not WHATSAPP.is_running():
        return HttpResponseRedirect(reverse('config'))

    WHATSAPP.stop()
    return HttpResponseRedirect(reverse('config'))


def save_messaging_settings(request: HttpRequest) -> HttpResponse:

    if not WHATSAPP.is_running() and not WHATSAPP.is_authenticated():
        return HttpResponseRedirect(reverse('config'))

    WHATSAPP.save_messaging_settings(
        request.POST.get('target'),
        request.POST.get('mode'),
    )
    return HttpResponseRedirect(reverse('config'))


def clear_messaging_settings(request: HttpRequest) -> HttpResponse:

    if not WHATSAPP.is_running() and not WHATSAPP.is_authenticated():
        return HttpResponseRedirect(reverse('config'))

    WHATSAPP.clear_messaging_settings()
    return HttpResponseRedirect(reverse('config'))


def send_debug_message(request: HttpRequest) -> HttpResponse:

    if not WHATSAPP.is_running() and not WHATSAPP.is_authenticated and not WHATSAPP.target and WHATSAPP.mode:
        return HttpResponseRedirect(reverse('config'))

    try:
        WHATSAPP.send_message(
            WHATSAPP.target, request.POST.get('message')
        )
        messages.success(request, 'Message sent.')
        return HttpResponseRedirect(reverse('config'))

    except Exception as e:
        messages.warning(
            request, 'Internal server error. Please contact system administrator.')
        logging.error(e)
        return HttpResponseRedirect(reverse('config'))
