from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.whatsapp import WHATSAPP
from django.contrib import messages
import logging


class SendDebugMessage(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not WHATSAPP.is_running() and not WHATSAPP.is_authenticated and not WHATSAPP.target and WHATSAPP.mode:
            return HttpResponseRedirect(reverse('config'))

        try:
            WHATSAPP.send_message(
                WHATSAPP.target, request.POST.get('message')
            )
            messages.success(request, 'Message sent.')
            return HttpResponseRedirect(reverse('config'))

        except Exception as e:
            messages.warning(
                request, 'Internal server error. Please contact system administrator.')
            logging.error(e)
            return HttpResponseRedirect(reverse('config'))
