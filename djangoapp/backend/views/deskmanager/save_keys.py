from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.contrib import messages
from backend.services.deskmanager import DESKMANAGER

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class SaveKeys(View):
    def post(self, request: HttpRequest) -> HttpResponse:

        if not DESKMANAGER.set_keys(request.POST.get('operator_key'), request.POST.get('ambient_key')):
            messages.error(
                request, 'Error trying to set Desk Manager keys. Please check the keys provided and try again.')
            return HttpResponseRedirect(reverse('config'))

        channel_layer = get_channel_layer()

        components = [
            {
                'component_id': 'deskmanager-api-keys-status',
                'content': '<span class="ms-1 badge rounded-pill text-bg-success">Authorized</span>'
            },
            {
                'component_id': 'operator_key_input_box',
                'content': f'<input type="text" class="form-control" id="operator_key_input" name="operator_key" placeholder="{"***********************************" + DESKMANAGER.operator_key[-5:] if DESKMANAGER.operator_key else ""}" disabled="">'
            },
            {
                'component_id': 'ambient_key_input_box',
                'content': f'<input type="text" class="form-control" id="ambient_key_input" name="ambient_key" placeholder="{"***********************************" + DESKMANAGER.ambient_key[-5:] if DESKMANAGER.ambient_key else ""}" disabled="">'
            },
            {
                'component_id': 'save_deskmanager_keys_button',
                'content': '<input type="submit" value="Authorize" form="backend_deskmanager_save_keys" class="btn btn-success btn-sm me-1" disabled="">'
            },
            {
                'component_id': 'clear_deskmanager_keys_button',
                'content': '<input type="submit" value="Deauthorize" form="backend_deskmanager_clear_keys" class="btn btn-danger btn-sm ms-1">'
            },
            {
                'component_id': 'data_update_mode',
                'content': '<select id="data_update_mode_select" class="form-select form-select-sm" name="mode" aria-label="Mode Select"><option selected=""></option><option value="Auto">Auto</option><option value="Manual">Manual</option></select>'
            },
            {
                'component_id': 'save_deskmanager_data_update_mode_button',
                'content': '<input type="submit" value="Set" form="backend_deskmanager_save_data_update_mode" class="btn btn-success btn-sm me-1">'
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
