from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.middleware.csrf import get_token
from backend.services.whatsapp import WHATSAPP
from backend.services.deskmanager import DESKMANAGER
from backend.models.deskmanager import ServiceOrder
from backend.tasks import celery_send
import logging


class SendManualMessage(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not WHATSAPP.is_running() and not WHATSAPP.is_authenticated and not WHATSAPP.target and WHATSAPP.mode:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        try:
            service_order_id = request.POST.get('service_order_id')

            if not service_order_id:
                raise Exception()

            service_order = ServiceOrder.objects.get(pk=int(service_order_id))

            if service_order.whatsapp_sent:
                messages.warning(
                    request, 'The message you were trying to send has already been sent.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            message = DESKMANAGER.build_whatsapp_message(
                service_order.to_dict())

            celery_send.delay(
                target=WHATSAPP.target,
                message=message,
                csrf_token=get_token(request)
            )

            service_order.whatsapp_sent = True
            service_order.save()

            messages.success(request, 'Message sent.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        except Exception as e:
            messages.warning(
                request, 'Internal server error. Please contact system administrator.')
            logging.error(e)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
