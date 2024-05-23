from django.http import HttpResponse, JsonResponse
from django.views import View
from app import tasks


class CeleryHelloWorld(View):
    def get(self, request: HttpResponse) -> JsonResponse:
        tasks.hello_world.delay()
        return JsonResponse({'Hello': 'world!'})
