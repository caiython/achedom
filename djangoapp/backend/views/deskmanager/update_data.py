from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from django.conf import settings
from backend.services.deskmanager import DESKMANAGER
from backend.services.whatsapp import WHATSAPP
from backend.models import ServiceOrder
import datetime
from html import unescape


class UpdateData(View):
    def get(self, request: HttpRequest) -> JsonResponse:

        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('SecretKey'):
            return JsonResponse({'message': 'Unauthorized'}, status=401)

        if authorization_header.split(' ')[1] != settings.SECRET_KEY:
            return JsonResponse({'message': 'Unauthorized'}, status=401)

        if request.GET.get('auto_update') and DESKMANAGER.data_update_mode != 'Auto':
            return JsonResponse({'auto_updated': False}, status=200)

        if not ServiceOrder.objects.exists():
            search_result = DESKMANAGER.service_order_search('')

            if search_result is None:
                return JsonResponse({'auto_updated': request.GET.get('auto_update')})

            newest_service_order = ServiceOrder(
                **_process_service_order_data(search_result[0]))
            newest_service_order.save()
            if WHATSAPP.target and WHATSAPP.mode == 'Auto':
                sent = WHATSAPP.send_message(
                    WHATSAPP.target, DESKMANAGER.build_whatsapp_message(newest_service_order.to_dict()))
                if sent:
                    newest_service_order.whatsapp_sent = True
                    newest_service_order.save()
            return JsonResponse({'auto_updated': request.GET.get('auto_update')})

        if DESKMANAGER.is_updating_data:
            return JsonResponse({'auto_updated': request.GET.get('auto_update')})

        DESKMANAGER.is_updating_data = True

        while DESKMANAGER.is_updating_data:

            if DESKMANAGER.data_update_mode is None:

                DESKMANAGER.is_updating_data = False

                break

            last_service_order_code_on_db = ServiceOrder.objects.last().service_order_code

            if _updated_data_through_code_sum(
                    last_service_order_code_on_db):
                continue

            if _updated_data_through_checking_date(
                    last_service_order_code_on_db):
                continue

            DESKMANAGER.is_updating_data = False

            break

        return JsonResponse({'auto_updated': request.GET.get('auto_update')})


def _updated_data_through_code_sum(last_service_order_code_on_db):
    new_service_order_code = DESKMANAGER.new_service_order_code(
        last_service_order_code_on_db)
    search_result = DESKMANAGER.service_order_search(
        new_service_order_code)
    if search_result is None:
        return 1
    if len(search_result) != 0:
        new_service_order = ServiceOrder(
            **_process_service_order_data(search_result[0]))
        new_service_order.save()
        if WHATSAPP.target and WHATSAPP.mode == 'Auto':
            sent = WHATSAPP.send_message(
                WHATSAPP.target, DESKMANAGER.build_whatsapp_message(new_service_order.to_dict()))
            if sent:
                new_service_order.whatsapp_sent = True
                new_service_order.save()
        return 1
    return 0


def _updated_data_through_checking_date(last_service_order_code_on_db):
    next_date_service_order_code = DESKMANAGER.next_date_service_order_code(
        last_service_order_code_on_db)
    search_result = DESKMANAGER.service_order_search(
        next_date_service_order_code)
    if search_result is None:
        return 1
    if len(search_result) != 0:
        new_service_order = ServiceOrder(
            **_process_service_order_data(search_result[0]))
        new_service_order.save()
        if WHATSAPP.target and WHATSAPP.mode == 'Auto':
            sent = WHATSAPP.send_message(
                WHATSAPP.target, DESKMANAGER.build_whatsapp_message(new_service_order.to_dict()))
            if sent:
                new_service_order.whatsapp_sent = True
                new_service_order.save()
        return 1
    return 0


def _process_service_order_data(service_order_data: dict) -> dict:
    return {
        'service_order_code': service_order_data['CodChamado'],
        'creation_datetime': datetime.datetime.strptime(f"{service_order_data['DataCriacao']} {service_order_data['HoraCriacao']}", "%Y-%m-%d %H:%M:%S"),
        'user': service_order_data['NomeUsuario'] + ' ' + service_order_data['SobrenomeUsuario'],
        'customer': DESKMANAGER.get_client_by_user_key(service_order_data['ChaveUsuario']),
        'priority': service_order_data['NomePrioridade'],
        'subject': service_order_data['Assunto'],
        'description': unescape(service_order_data['Descricao']),
        'operator': service_order_data['NomeOperador'] + ' ' + service_order_data['SobrenomeOperador'] if 'NomeOperador' in service_order_data else 'SERVICE DESK'
    }
