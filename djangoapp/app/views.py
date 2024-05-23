from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from backend.services.whatsapp import WHATSAPP
from . import tasks


# Create your views here.
def welcome(request: HttpRequest) -> HttpResponse:

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    ctx = {
        'login_url': reverse('login'),
        'register_url': reverse('register')
    }

    return render(request, 'app/welcome.html', ctx)


def home(request: HttpRequest) -> HttpResponse:

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('welcome'))

    ctx = {
        'home': True,
        'is_staff': request.user.is_staff,
        'logout_url': reverse('logout')
    }
    return render(request, 'app/index.html', ctx)


def service_orders(request: HttpRequest) -> HttpResponse:

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    ctx = {
        'service_orders': True,
        'is_staff': request.user.is_staff,
        'logout_url': reverse('logout')
    }

    return render(request, 'app/service_orders.html', ctx)


def config(request: HttpRequest) -> HttpResponse:

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    ctx = {
        'config': True,
        'is_staff': request.user.is_staff,
        'url': {
            'start_wa': reverse('start_wa'),
            'stop_wa': reverse('stop_wa'),
            'save_messaging_settings': reverse('save_messaging_settings'),
            'clear_messaging_settings': reverse('clear_messaging_settings'),
            'send_message': reverse('send_message'),
        },
        'logout_url': reverse('logout'),
        'whatsapp': {
            'is_running': WHATSAPP.is_running(),
            'is_waiting_for_qrcode': WHATSAPP.is_qr_code_on_screen(),
            'is_authenticated': WHATSAPP.is_authenticated(),
            'contacts': WHATSAPP.get_contacts(),
            'target_selected': WHATSAPP.target,
            'mode_selected': WHATSAPP.mode,
        },
    }
    return render(request, 'app/config/config.html', ctx)


def celery_hello_world(request: HttpResponse) -> JsonResponse:
    tasks.hello_world.delay()
    return JsonResponse({'Hello': 'world!'})
