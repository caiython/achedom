from django.http import HttpRequest, JsonResponse
from django.views import View
from backend.services.whatsapp import WHATSAPP


class UpdateQrCode(View):
    def post(self, request: HttpRequest) -> JsonResponse:

        if WHATSAPP.is_authenticated():
            return JsonResponse({'is_authenticated': True, 'is_running': True})

        if WHATSAPP.is_running():
            WHATSAPP.save_qrcode()
            return JsonResponse({'is_authenticated': False, 'is_running': True})

        return JsonResponse({'is_authenticated': False, 'is_running': False})
