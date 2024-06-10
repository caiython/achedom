from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.deskmanager import DESKMANAGER

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ClearDataUpdateMode(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not DESKMANAGER.api_token and not DESKMANAGER.data_update_mode:
            return HttpResponseRedirect(reverse('config'))

        DESKMANAGER.data_update_mode = None

        channel_layer = get_channel_layer()

        components = [
            {
                'component_id': 'deskmanager-data-update-mode-status',
                'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Not set</span>'
            },
            {
                'component_id': 'data_update_mode',
                'content': '<select id="data_update_mode_select" class="form-select form-select-sm" name="mode" aria-label="Mode Select"><option selected=""></option><option value="Auto">Auto</option><option value="Manual">Manual</option></select>',
            },
            {
                'component_id': 'clear_deskmanager_data_update_mode_button',
                'content': '<input type="submit" value="Reset" form="backend_deskmanager_clear_data_update_mode" class="btn btn-danger btn-sm ms-1" disabled="">'
            },
        ]

        for component in components:
            async_to_sync(channel_layer.group_send)(
                'update_component',
                {
                    'type': 'chat.message',
                    'component_id': component['component_id'],
                    'content': component['content']
                }
            )

        return HttpResponseRedirect(reverse('config'))
