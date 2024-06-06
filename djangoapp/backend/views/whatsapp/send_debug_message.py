from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.whatsapp import WHATSAPP
from django.contrib import messages
import logging
from backend.tasks import celery_send
from django.middleware.csrf import get_token


class SendDebugMessage(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not WHATSAPP.is_running() and not WHATSAPP.is_authenticated and not WHATSAPP.target and WHATSAPP.mode:
            return HttpResponseRedirect(reverse('config'))

        try:
            celery_send.delay(
                target=WHATSAPP.target,
                message=request.POST.get('message'),
                csrf_token=get_token(request)
            )
            messages.success(request, 'Message sent.')
            return HttpResponseRedirect(reverse('config'))

        except Exception as e:
            messages.warning(
                request, 'Internal server error. Please contact system administrator.')
            logging.error(e)
            return HttpResponseRedirect(reverse('config'))
