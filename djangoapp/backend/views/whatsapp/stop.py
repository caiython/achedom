from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.whatsapp import WHATSAPP


class Stop(View):
    def post(self, request: HttpRequest) -> HttpResponse:

        if not WHATSAPP.is_running():
            return HttpResponseRedirect(reverse('config'))

        WHATSAPP.stop()
        return HttpResponseRedirect(reverse('config'))
