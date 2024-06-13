from django.http import HttpRequest, JsonResponse
from django.views import View
from backend.services.whatsapp import WHATSAPP


class Send(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            WHATSAPP.send_message(request.POST.get('target'),
                                  request.POST.get('message'))
            return JsonResponse({'sent': True})
        except:
            return JsonResponse({'sent': False})
