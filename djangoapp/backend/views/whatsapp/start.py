from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.whatsapp import WHATSAPP
from django.middleware.csrf import get_token


class Start(View):
    def post(self, request: HttpRequest) -> HttpResponse:

        if WHATSAPP.is_running():
            return HttpResponseRedirect(reverse('config'))

        WHATSAPP.start(get_token(request))
        return HttpResponseRedirect(reverse('config'))
