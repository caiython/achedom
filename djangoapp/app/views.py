from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import tasks


# Create your views here.
def welcome(request: HttpRequest) -> HttpResponse:

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
        return HttpResponseRedirect(reverse('welcome'))

    ctx = {
        'service_orders': True,
        'is_staff': request.user.is_staff
    }
    return render(request, 'app/service_orders.html', ctx)


def config(request: HttpRequest) -> HttpResponse:

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('welcome'))

    ctx = {
        'config': True,
        'is_staff': request.user.is_staff
    }
    return render(request, 'app/config.html', ctx)


def celery_hello_world(request: HttpResponse) -> JsonResponse:
    tasks.hello_world.delay()
    return JsonResponse({'Hello': 'world!'})
