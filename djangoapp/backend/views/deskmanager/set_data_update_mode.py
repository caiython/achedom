from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.deskmanager import DESKMANAGER

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class SetDataUpdateMode(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not DESKMANAGER.api_token:
            return HttpResponseRedirect(reverse('config'))

        DESKMANAGER.set_data_update_mode(request.POST.get('mode'))

        channel_layer = get_channel_layer()

        components = [
            {
                'component_id': 'deskmanager-data-update-mode-status',
                'content': '<span class="ms-1 badge rounded-pill text-bg-success">Set</span>'
            },
            {
                'component_id': 'data_update_mode',
                'content': f'''
                    <select id="data_update_mode_select" class="form-select form-select-sm" name="mode" aria-label="Mode Select" {'disabled' if not DESKMANAGER.api_token else ''}>

                        {'<option selected></option>' if not DESKMANAGER.data_update_mode else ''}
                        <option value="Auto" {'selected' if DESKMANAGER.data_update_mode == 'Auto' else ''}>Auto</option>
                        <option value="Manual" {'selected' if DESKMANAGER.data_update_mode == 'Manual' else ''}>Manual</option>
                    </select>
                '''
            },
            {
                'component_id': 'clear_deskmanager_data_update_mode_button',
                'content': '<input type="submit" value="Reset" form="backend_deskmanager_clear_data_update_mode" class="btn btn-danger btn-sm ms-1">'
            }
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
