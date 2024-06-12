from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.whatsapp import WHATSAPP


class SaveMessagingSettings(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not WHATSAPP.is_running() and not WHATSAPP.is_authenticated():
            return HttpResponseRedirect(reverse('config'))

        WHATSAPP.save_messaging_settings(
            request.POST.get('target'),
            request.POST.get('mode'),
        )
        return HttpResponseRedirect(reverse('config'))
