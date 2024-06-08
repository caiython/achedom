from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from backend.services.whatsapp import WHATSAPP
from backend.services.deskmanager import DESKMANAGER


class Config(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        if not request.user.is_authenticated:
            messages.warning(
                request, 'The page you are trying to access requires authentication. Please login.')
            return HttpResponseRedirect(reverse('login'))

        ctx = {
            'config': True,
            'is_staff': request.user.is_staff,
            'url': {
                'backend': {
                    'whatsapp': {
                        'start': reverse('backend_whatsapp_start'),
                        'stop': reverse('backend_whatsapp_stop'),
                        'save_messaging_settings': reverse('backend_whatsapp_save_messaging_settings'),
                        'clear_messaging_settings': reverse('backend_whatsapp_clear_messaging_settings'),
                        'send_debug_message': reverse('backend_whatsapp_send_debug_message'),
                    },
                    'deskmanager': {
                        'save_keys': reverse('backend_deskmanager_save_keys'),
                        'clear_keys': reverse('backend_deskmanager_clear_keys'),
                        'set_data_update_mode': reverse('backend_deskmanager_set_data_update_mode'),
                        'clear_data_update_mode': reverse('backend_deskmanager_clear_data_update_mode'),
                    },
                },
                'ws': {
                    'update_component': '/ws/update_component/'
                }
            },
            'logout_url': reverse('logout'),
            'whatsapp': {
                'is_running': WHATSAPP.is_running(),
                'is_waiting_for_qrcode': WHATSAPP.is_qr_code_on_screen(),
                'is_authenticated': WHATSAPP.is_authenticated(),
                'contacts': WHATSAPP.get_contacts() if WHATSAPP.is_running() and WHATSAPP.is_authenticated() else [],
                'target_selected': WHATSAPP.target,
                'mode_selected': WHATSAPP.mode,
            },
            'deskmanager': {
                'operator_key': '***********************************' + DESKMANAGER.operator_key[-5:] if DESKMANAGER.operator_key else None,
                'ambient_key': '***********************************' + DESKMANAGER.ambient_key[-5:] if DESKMANAGER.ambient_key else None,
                'auth_token': '********************************************' + DESKMANAGER.api_token[-5:] if DESKMANAGER.api_token else None,
                'data_update_mode': DESKMANAGER.data_update_mode,
            },
            'ws_method': "wss" if request.META.get('HTTP_X_FORWARDED_PROTO', '') == 'https' else "ws"
        }

        return render(request, 'app/config/config.html', ctx)
