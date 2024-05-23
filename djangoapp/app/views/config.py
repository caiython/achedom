from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from backend.services.whatsapp import WHATSAPP


class Config(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        ctx = {
            'config': True,
            'is_staff': request.user.is_staff,
            'url': {
                'start_wa': reverse('start_wa'),
                'stop_wa': reverse('stop_wa'),
                'save_messaging_settings': reverse('save_messaging_settings'),
                'clear_messaging_settings': reverse('clear_messaging_settings'),
                'send_message': reverse('send_message'),
            },
            'logout_url': reverse('logout'),
            'whatsapp': {
                'is_running': WHATSAPP.is_running(),
                'is_waiting_for_qrcode': WHATSAPP.is_qr_code_on_screen(),
                'is_authenticated': WHATSAPP.is_authenticated(),
                'contacts': WHATSAPP.get_contacts(),
                'target_selected': WHATSAPP.target,
                'mode_selected': WHATSAPP.mode,
            },
        }

        return render(request, 'app/config/config.html', ctx)