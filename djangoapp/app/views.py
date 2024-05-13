from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from . import tasks


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    ctx = {'page_section': 'Home'}
    return render(request, 'index.html', ctx)



def celery_hello_world(request: HttpResponse) -> JsonResponse:
    tasks.hello_world.delay()
    return JsonResponse({'Hello': 'world!'})
