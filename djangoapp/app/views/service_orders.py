from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from backend.models import ServiceOrder
from backend.services.whatsapp import WHATSAPP


class ServiceOrders(View):
    def get(self, request: HttpRequest, page_number: str | None) -> HttpResponse:

        if not request.user.is_authenticated:
            messages.warning(
                request, 'The page you are trying to access requires authentication. Please login.')
            return HttpResponseRedirect(reverse('login'))

        service_order_list = ServiceOrder.objects.all().order_by('id').reverse()
        paginator = Paginator(service_order_list, 9)

        page_obj = paginator.get_page(int(page_number) if page_number else 1)

        ctx = {
            'service_orders': True,
            'is_staff': request.user.is_staff,
            'logout_url': reverse('logout'),
            'page_obj': page_obj,
            'whatsapp': {
                'mode_selected': WHATSAPP.mode,
            },
            'url': {
                'backend': {
                    'whatsapp': {
                        'send_manual_message': reverse('backend_whatsapp_send_manual_message'),
                    },
                },
            }
        }

        return render(request, 'app/service_orders.html', ctx)
