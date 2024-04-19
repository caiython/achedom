from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

# Create your views here.
def start_wa(request: HttpRequest) -> JsonResponse:
    return JsonResponse({'message': 'whatsapp started'})