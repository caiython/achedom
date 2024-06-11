from django.http import HttpRequest, JsonResponse
from django.views import View
from backend.services.whatsapp import WHATSAPP

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class UpdateQrCode(View):
    def post(self, request: HttpRequest) -> JsonResponse:

        if WHATSAPP.is_authenticated():
            channel_layer = get_channel_layer()
            target_select_options = ''.join(
                [f'<option value="{contact}" {"selected" if WHATSAPP.target == contact else ""}>{contact}</option>' for contact in WHATSAPP.get_contacts()])
            components = [
                {
                    'component_id': 'whatsapp_is_authenticated_status_modal',
                    'content': '<span class="badge rounded-pill text-bg-success">Authenticated</span>'
                },
                {
                    'component_id': 'whatsapp_is_authenticated_status',
                    'content': '<span class="badge rounded-pill text-bg-success">Authenticated</span>'
                },
                {
                    'component_id': 'get_qr_code_button',
                    'content': '<button type="button" class="btn btn-light btn-sm" data-bs-toggle="modal" data-bs-target="#get_qrcode_modal" disabled><i class="bi bi-qr-code-scan"></i> Get QR Code</button>'
                },
                {
                    'component_id': 'save_messaging_settings_button',
                    'content': '<input type="submit" value="Save" form="backend_whatsapp_save_messaging_settings" class="btn btn-success btn-sm me-1"></input>'
                },
                {
                    'component_id': 'target_select',
                    'content': f'''
                        <select class="form-select form-select-sm my-2" name="target" aria-label="Target Select">
                            <option value=""></option>
                            {target_select_options}
                        </select>
                    '''
                },
                {
                    'component_id': 'mode_select',
                    'content': '''
                            <select class="form-select form-select-sm my-2" name="mode" aria-label="Mode Select">
                                <option selected></option>
                                <option value="Auto">Auto</option>
                                <option value="Manual">Manual</option>
                            </select>
                    '''
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
            return JsonResponse({'is_authenticated': True, 'is_running': True})

        if WHATSAPP.is_running():
            WHATSAPP.save_qrcode()
            channel_layer = get_channel_layer()

            components = [
                {
                    'component_id': 'whatsapp_is_authenticated_status',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-warning">Waiting for QR Code Scan</span>'
                },
                {
                    'component_id': 'get_qr_code_button',
                    'content': '<button type="button" class="btn btn-light btn-sm" data-bs-toggle="modal" data-bs-target="#get_qrcode_modal"><i class="bi bi-qr-code-scan"></i> Get QR Code</button>'
                },
                {
                    'component_id': 'qr_code_image',  # Update the <img> on front
                    'content': ''
                },
                {
                    'component_id': 'whatsapp_is_authenticated_status_modal',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-warning">Waiting for QR Code Scan</span>'
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

            return JsonResponse({'is_authenticated': False, 'is_running': True})

        return JsonResponse({'is_authenticated': False, 'is_running': False})
