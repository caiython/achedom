from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import tasks


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:

    ctx = {
        'login_url': reverse('login'),
        'register_url': reverse('register')
    }
    return render(request, 'index.html', ctx)


def celery_hello_world(request: HttpResponse) -> JsonResponse:
    tasks.hello_world.delay()
    return JsonResponse({'Hello': 'world!'})
