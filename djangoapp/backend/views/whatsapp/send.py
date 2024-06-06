from django.http import HttpRequest, JsonResponse
from django.views import View
from backend.services.whatsapp import WHATSAPP

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages


class Send(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            WHATSAPP.send_message(request.POST.get('target'),
                                  request.POST.get('message'))
            return JsonResponse({'sent': True})
        except:
            return JsonResponse({'sent': False})
