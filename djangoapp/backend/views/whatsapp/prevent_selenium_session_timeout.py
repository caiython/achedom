from django.http import HttpRequest, JsonResponse
from django.views import View
from django.conf import settings
from backend.services.whatsapp import WHATSAPP


class PreventSeleniumSessionTimeout(View):
    def get(self, request: HttpRequest) -> JsonResponse:

        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('SecretKey'):
            return JsonResponse({'message': 'Unauthorized'}, status=401)

        if authorization_header.split(' ')[1] != settings.SECRET_KEY:
            return JsonResponse({'message': 'Unauthorized'}, status=401)

        # Session ping
        if hasattr(WHATSAPP, 'browser'):
            WHATSAPP.browser.current_url

        return JsonResponse({'message': 'Ok'}, status=200)
