from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.whatsapp import WHATSAPP


class ClearMessagingSettings(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not WHATSAPP.is_running() and not WHATSAPP.is_authenticated():
            return HttpResponseRedirect(reverse('config'))

        WHATSAPP.clear_messaging_settings()
        return HttpResponseRedirect(reverse('config'))
