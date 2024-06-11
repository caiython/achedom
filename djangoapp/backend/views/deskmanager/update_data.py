from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from backend.services.deskmanager import DESKMANAGER
from backend.services.whatsapp import WHATSAPP
from backend.models import ServiceOrder
import datetime
from html import unescape


class UpdateData(View):
    def post(self, request: HttpRequest) -> HttpResponse:

        if request.POST.get('auto_update') and DESKMANAGER.data_update_mode != 'Auto':
            return JsonResponse({'auto_updated': False})

        if not ServiceOrder.objects.exists():
            newest_service_order = ServiceOrder(
                **_process_service_order_data(DESKMANAGER.service_order_search('')[0]))
            newest_service_order.save()
            if WHATSAPP.target and WHATSAPP.mode == 'Auto':
                sent = WHATSAPP.send_message(
                    WHATSAPP.target, _build_whatsapp_message(newest_service_order.to_dict()))
                if sent:
                    newest_service_order.whatsapp_sent = True
                    newest_service_order.save()
            return JsonResponse({'auto_update': request.POST.get('auto_update')})

        if DESKMANAGER.is_updating_data:
            return JsonResponse({'auto_update': request.POST.get('auto_update')})

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

        return JsonResponse({'auto_update': request.POST.get('auto_update')})


def _updated_data_through_code_sum(last_service_order_code_on_db):
    new_service_order_code = DESKMANAGER.new_service_order_code(
        last_service_order_code_on_db)
    search_result = DESKMANAGER.service_order_search(
        new_service_order_code)
    if len(search_result) != 0:
        new_service_order = ServiceOrder(
            **_process_service_order_data(search_result[0]))
        new_service_order.save()
        if WHATSAPP.target and WHATSAPP.mode == 'Auto':
            sent = WHATSAPP.send_message(
                WHATSAPP.target, _build_whatsapp_message(new_service_order.to_dict()))
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
    if len(search_result) != 0:
        new_service_order = ServiceOrder(
            **_process_service_order_data(search_result[0]))
        new_service_order.save()
        if WHATSAPP.target and WHATSAPP.mode == 'Auto':
            sent = WHATSAPP.send_message(
                WHATSAPP.target, _build_whatsapp_message(new_service_order.to_dict()))
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


def _build_whatsapp_message(service_order_data: dict) -> str:

    lines = [
        "*NOVO CHAMADO!*",
        "```",
        f"Distribuição: {service_order_data.get('operator')}",
        "",
        f"1. Código do Chamado: {service_order_data.get('service_order_code')}",
        f"Data e Hora de Criação: {service_order_data.get('creation_datetime').strftime('%d/%m/%y, %H:%M')}",
        f"Solicitante: {service_order_data.get('user')} - {service_order_data.get('customer')}",
        f"Prioridade: {service_order_data.get('priority')}",
        "",
        "",
        f"Assunto: {service_order_data.get('subject')}",
        "",
        "Descrição:",
        "",
        f"{str(service_order_data.get('description')).strip()}",
        "```",
    ]
    return "\n".join(lines)
