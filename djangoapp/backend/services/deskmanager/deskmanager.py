import os
from io import BytesIO
from time import sleep

from django.conf import settings
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
from backend.tasks import celery_update_qr_code

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync
from requests.api import post
from datetime import datetime
from dateutil.relativedelta import relativedelta


class DeskManager:

    DATA_UPDATE_MODES = [
        'auto',
        'manual',
    ]

    def __init__(self):
        self.operator_key = None
        self.ambient_key = None
        self.api_token = None
        self.data_update_mode = None

    def set_keys(self, chave_do_operador: str | None, chave_do_ambiente: str | None) -> bool:

        if not chave_do_operador or not chave_do_ambiente:
            return False

        api_response = post(r"https://api.desk.ms/Login/autenticar",
                            headers={"Authorization": chave_do_operador},
                            json={"PublicKey": chave_do_ambiente})
        if len(api_response.json()) != 49:
            return False
        self.operator_key = chave_do_operador
        self.ambient_key = chave_do_ambiente
        self.api_token = api_response.json()
        return True

    def reset_config(self) -> bool:
        self.operator_key = None
        self.ambient_key = None
        self.api_token = None
        self.data_update_mode = None
        return True

    # Realiza uma pesquisa através dos dados informados na variável "pesquisa"
    def service_order_search(self, search):
        parameters = {"Pesquisa": search}
        try:
            api_response = post(r"https://api.desk.ms/ChamadosSuporte/lista",
                                json=parameters,
                                headers={"Authorization": self.api_token}).json()['root']
        except KeyError:
            self.set_keys(self.operator_key, self.ambient_key)
            api_response = post(r"https://api.desk.ms/ChamadosSuporte/lista",
                                json=parameters,
                                headers={"Authorization": self.api_token}).json()['root']
        return api_response

    # Retorna os dados de um chamado a partir de sua chave primária
    def service_order_data(self, service_order_key):
        parametros = {"Chave": service_order_key}
        api_response = post(r"https://api.desk.ms/ChamadosSuporte",
                            json=parametros,
                            headers={"Authorization": self.api_token}).json()
        return api_response

    def get_client_by_user_key(self, user_key):
        parametros = {"Chave": user_key}
        api_response = post(r"https://api.desk.ms/Usuarios",
                            json=parametros,
                            headers={"Authorization": self.api_token}).json()
        client = api_response['TUsuario']['Cliente'][0]['text']
        return client

    def new_service_order_code(self, service_order_code):
        prefix = service_order_code[:4]
        sufix = self._adjust_sufix(str(int(service_order_code[5:]) + 1))
        new_service_order_code = prefix + "-" + sufix
        return new_service_order_code

    def next_date_service_order_code(self, last_service_order_code):
        current_date = datetime.strptime(last_service_order_code[:4], '%m%y')
        new_date = datetime.strftime(
            current_date + relativedelta(months=1), '%m%y')
        new_service_order_code = new_date + '-000001'
        return new_service_order_code

    def set_data_update_mode(self, mode: str | None) -> bool:
        if mode is None or mode.lower() not in self.DATA_UPDATE_MODES:
            return False
        self.data_update_mode = mode
        return True

    def _adjust_sufix(self, sufix):
        if len(sufix) == 5:
            new_sufix = "0" + sufix
        elif len(sufix) == 4:
            new_sufix = "00" + sufix
        elif len(sufix) == 3:
            new_sufix = "000" + sufix
        elif len(sufix) == 2:
            new_sufix = "0000" + sufix
        elif len(sufix) == 1:
            new_sufix = "00000" + sufix
        else:
            new_sufix = "000000"
        return new_sufix


DESKMANAGER = DeskManager()
