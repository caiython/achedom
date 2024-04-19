from django.http import HttpRequest, JsonResponse

from .services.whatsapp import WHATSAPP


# Create your views here.
def start_wa(request: HttpRequest) -> JsonResponse:
    WHATSAPP.start()
    return JsonResponse({'message': 'whatsapp started'})
