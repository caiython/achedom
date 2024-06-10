from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.deskmanager import DESKMANAGER
from django.contrib import messages

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ClearKeys(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not DESKMANAGER.reset_config():
            messages.error(
                request, 'Error trying to reset Desk Manager configs. Please, message the system administrator.')

        channel_layer = get_channel_layer()

        components = [
            {
                'component_id': 'deskmanager-api-keys-status',
                'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Not Authorized</span>'
            },
            {
                'component_id': 'operator_key_input_box',
                'content': '<input type="text" class="form-control" id="operator_key_input" name="operator_key">'
            },
            {
                'component_id': 'ambient_key_input_box',
                'content': '<input type="text" class="form-control" id="ambient_key_input" name="ambient_key">'
            },
            {
                'component_id': 'save_deskmanager_keys_button',
                'content': '<input type="submit" value="Authorize" form="backend_deskmanager_save_keys" class="btn btn-success btn-sm me-1">'
            },
            {
                'component_id': 'clear_deskmanager_keys_button',
                'content': '<input type="submit" value="Deauthorize" form="backend_deskmanager_clear_keys" class="btn btn-danger btn-sm ms-1" disabled="">'
            },
            {
                'component_id': 'deskmanager-data-update-mode-status',
                'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Not set</span>'
            },
            {
                'component_id': 'data_update_mode',
                'content': '<select id="data_update_mode_select" class="form-select form-select-sm" name="mode" aria-label="Mode Select" disabled=""><option selected=""></option><option value="Auto">Auto</option><option value="Manual">Manual</option></select>',
            },
            {
                'component_id': 'save_deskmanager_data_update_mode_button',
                'content': '<input type="submit" value="Set" form="backend_deskmanager_save_data_update_mode" class="btn btn-success btn-sm me-1" disabled="">',
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
