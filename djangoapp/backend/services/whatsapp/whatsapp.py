# D:\vscode\djangoapp-docker-base\djangoapp\app\tests.py

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


class Whatsapp():
    fixtures = [
        'app/fixtures/app.json',
        ...
    ]

    MODE_OPTIONS = [
        'Auto',
        'Manual',
    ]

    def __init__(self):
        self.target = None
        self.mode = None

    def start(self, csrf_token):
        try:
            selenium_grid_url = "http://selenium:4444/wd/hub"
            options = webdriver.FirefoxOptions()
            self.browser = webdriver.Remote(command_executor=selenium_grid_url,
                                            keep_alive=True,
                                            options=options)
            self.browser.get('https://web.whatsapp.com/')

            # Send ws
            components = [
                {
                    'component_id': 'selenium-instance-status',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-success">Running</span>'
                },
                {
                    'component_id': 'backend_whatsapp_start_button',
                    'content': '<input type="submit" value="Run" form="backend_whatsapp_start" class="btn btn-success btn-sm me-1 disabled"></input>'
                },
                {
                    'component_id': 'backend_whatsapp_stop_button',
                    'content': '<input type="submit" value="Stop" form="backend_whatsapp_stop" class="btn btn-danger btn-sm ms-1"></input>'
                }
            ]

            for component in components:

                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'update_component',
                    {
                        'type': 'chat.message',
                        'component_id': component['component_id'],
                        'content': component['content'],
                    }
                )

            celery_update_qr_code.delay(csrf_token)

            return 1
        except Exception as e:
            logging.error(e)
            return 0

    def stop(self):
        try:
            self.target = None
            self.mode = None
            self.browser.quit()
            self.browser.stop_client()

            # Send ws
            channel_layer = get_channel_layer()

            components = [
                {
                    'component_id': 'selenium-instance-status',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Stopped</span>'
                },
                {
                    'component_id': 'backend_whatsapp_start_button',
                    'content': '<input type="submit" value="Run" form="backend_whatsapp_start" class="btn btn-success btn-sm me-1"></input>'
                },
                {
                    'component_id': 'backend_whatsapp_stop_button',
                    'content': '<input type="submit" value="Stop" form="backend_whatsapp_stop" class="btn btn-danger btn-sm ms-1" disabled></input>'
                },
                {
                    'component_id': 'whatsapp_is_authenticated_status',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Not Authenticated</span>'
                },
                {
                    'component_id': 'whatsapp_is_authenticated_status_modal',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Not Authenticated</span>'
                },
                {
                    'component_id': 'get_qr_code_button',
                    'content': '<button type="button" class="btn btn-light btn-sm" data-bs-toggle="modal" data-bs-target="#get_qrcode_modal" disabled><i class="bi bi-qr-code-scan"></i> Get QR Code</button>'
                },
                {
                    'component_id': 'whatsapp_target_selected',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Not Set</span>'
                },
                {
                    'component_id': 'target_select',
                    'content': '''
                            <select class="form-select form-select-sm my-2" name="target" aria-label="Target Select" disabled>
                                <option selected></option>
                            </select>
                    '''
                },
                {
                    'component_id': 'mode_select',
                    'content': '''
                            <select class="form-select form-select-sm my-2" name="mode" aria-label="Mode Select" disabled>
                                <option selected></option>
                                <option value="Auto">Auto</option>
                                <option value="Manual">Manual</option>
                            </select>
                    '''
                },
                {
                    'component_id': 'save_messaging_settings_button',
                    'content': '<input type="submit" value="Save" form="backend_whatsapp_save_messaging_settings" class="btn btn-success btn-sm me-1" disabled></input>'
                },
                {
                    'component_id': 'clear_messaging_settings_button',
                    'content': '<input type="submit" value="Clear" form="backend_whatsapp_clear_messaging_settings" class="btn btn-danger btn-sm ms-1" disabled></input>'
                },
                {
                    'component_id': 'debug_message_status',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Must Have a Target</span>'
                },
                {
                    'component_id': 'text_message_input_box',
                    'content': '<input type="text" class="form-control" id="text_message_input" name="message" placeholder="Hey! This is a test message!" disabled>'
                },
                {
                    'component_id': 'send_debug_message_button',
                    'content': '<input type="submit" value="Send" form="send_debug_message" class="btn btn-success btn-sm me-1" disabled></input>'
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

            return 1
        except Exception as e:
            logging.error(e)
            return 0

    def is_running(self):
        try:
            if self.browser.current_url:
                return 1
            return 0
        except Exception as e:
            logging.error(e)
            return 0

    def is_qr_code_on_screen(self):
        qrcode_xpath = '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas'
        try:
            # WebDriverWait(self.browser, 10).until(
            #    EC.presence_of_element_located((By.XPATH, qrcode_xpath)))
            self.browser.find_element(By.XPATH, qrcode_xpath)
            return 1
        except NoSuchElementException:
            return 0
        except TimeoutException as te:
            logging.error(te)
            return 0
        except Exception as e:
            logging.error(e)
            return 0

    def save_qrcode(self):

        try:
            reload_qrcode_button_xpath = "/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/span/button"
            self.browser.find_element(
                By.XPATH, reload_qrcode_button_xpath).click()
            sleep(2)
        except NoSuchElementException:
            pass
        except Exception as e:
            logging.error(e)
            return 0

        try:
            qrcode_xpath = '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas'
            qr_code = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, qrcode_xpath)))
            screenshot = self.browser.get_screenshot_as_png()
            img = Image.open(BytesIO(screenshot))
            x, y, w, h = qr_code.location['x'], qr_code.location['y'], qr_code.size['width'], qr_code.size['height']
            cropped_img = img.crop((x-5, y-5, x+w+5, y+h+5))
            img_path = os.path.join(settings.MEDIA_ROOT, 'qrcode.png')
            cropped_img.save(img_path)
            return 1
        except Exception as e:
            logging.error(e)
            return 0

    def send_message(self, target, text_to_send, delay=10):
        try:
            target_xpath = '//span[contains(@title,"' + target + '")]'
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, target_xpath))).click()
            sleep(1)
            message_box_xpath = '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
            message_box = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, message_box_xpath)))
            ActionChains(self.browser).move_to_element(
                message_box).click().send_keys(text_to_send, Keys.ENTER).perform()
            sleep(delay)
            return 1
        except Exception as e:
            logging.error(e)
            return 0

    def is_authenticated(self):
        try:
            me_display_name = self.browser.execute_script(
                "return window.localStorage.getItem('me-display-name');")
            if me_display_name is None:
                return 0
            return 1
        except Exception as e:
            logging.error(e)
            return 0

    def get_contacts(self):

        if not self.is_running and not self.is_authenticated:
            return []

        contacts = []

        for _ in range(10):

            try:
                chats_xpath = '/html/body/div[1]/div/div/div[2]/div[3]/div/div[3]/div[1]/div/div'
                chats_container = self.browser.find_element(
                    By.XPATH, chats_xpath)
            except NoSuchElementException:
                try:
                    chats_xpath = '/html/body/div[1]/div/div/div[2]/div[3]/div/div[2]/div/div/div'
                    chats_container = self.browser.find_element(
                        By.XPATH, chats_xpath)
                except NoSuchElementException:
                    sleep(3)
                    continue
                except Exception as e:
                    logging.error(e)
                    return []
            except Exception as e:
                logging.error(e)
                return []

            try:
                chats_divs = chats_container.find_elements(By.XPATH, './div')
                for chat_div in chats_divs:
                    try:
                        span_element = chat_div.find_element(
                            By.XPATH, './/div/div/div[2]/div[1]/div[1]//span')
                    except NoSuchElementException:
                        try:
                            span_element = chat_div.find_element(
                                By.XPATH, './/div/div/div[2]/div[1]/div[1]/div//span')
                        except NoSuchElementException:
                            sleep(3)
                            continue
                        except Exception as e:
                            logging.error(e)
                            return []
                    except Exception as e:
                        logging.error(e)
                        return []

                    span_content = span_element.text
                    contacts.append(span_content)

                contacts.sort()

            except Exception as e:
                logging.error(e)
                return []

            if len(contacts) > 0:
                return contacts

            sleep(3)

        return []

    def save_messaging_settings(self, target, mode):
        try:
            if target in self.get_contacts() and mode in self.MODE_OPTIONS:
                self.target = target
                self.mode = mode

                # Send WS
                channel_layer = get_channel_layer()

                target_select_options = ''.join(
                    [f'<option value="{contact}" {"selected" if self.target == contact else ""}>{contact}</option>' for contact in self.get_contacts()])

                components = [
                    {
                        'component_id': 'whatsapp_target_selected',
                        'content': '<span class="badge rounded-pill text-bg-success">Set</span>'
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
                        'content': f'''
                        <select class="form-select form-select-sm my-2" name="mode" aria-label="Mode Select">
                            <option value=""></option>
                            <option value="Auto" {"selected" if self.mode == "Auto" else ""}>Auto</option>
                            <option value="Manual" {"selected" if self.mode == "Manual" else ""}>Manual</option>
                        </select>
                    '''
                    },
                    {
                        'component_id': 'clear_messaging_settings_button',
                        'content': '<input type="submit" value="Clear" form="backend_whatsapp_clear_messaging_settings" class="btn btn-danger btn-sm ms-1"></input>'
                    },
                    {
                        'component_id': 'debug_message_status',
                        'content': '<span class="badge rounded-pill text-bg-success">Ready</span>'
                    },
                    {
                        'component_id': 'text_message_input_box',
                        'content': '<input type="text" class="form-control" id="text_message_input" name="message" placeholder="Hey! This is a test message!">'
                    },
                    {
                        'component_id': 'send_debug_message_button',
                        'content': '<input type="submit" value="Send" form="send_debug_message" class="btn btn-success btn-sm me-1"></input>'
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
                return 1
            return 0
        except Exception as e:
            logging.error(e)
            return 0

    def clear_messaging_settings(self):
        try:
            self.target = None
            self.mode = None

            # Send WS
            channel_layer = get_channel_layer()

            target_select_options = ''.join(
                [f'<option value="{contact}">{contact}</option>' for contact in self.get_contacts()])

            components = [
                {
                    'component_id': 'whatsapp_target_selected',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Not Set</span>'
                },
                {
                    'component_id': 'target_select',
                    'content': f'''
                            <select class="form-select form-select-sm my-2" name="target" aria-label="Target Select">
                                <option value="" selected></option>
                                {target_select_options}
                            </select>
                        '''
                },
                {
                    'component_id': 'mode_select',
                    'content': '''
                            <select class="form-select form-select-sm my-2" name="mode" aria-label="Mode Select">
                                <option value="" selected></option>
                                <option value="Auto">Auto</option>
                                <option value="Manual">Manual</option>
                            </select>
                        '''
                },
                {
                    'component_id': 'clear_messaging_settings_button',
                    'content': '<input type="submit" value="Clear" form="backend_whatsapp_clear_messaging_settings" class="btn btn-danger btn-sm ms-1" disabled></input>'
                },
                {
                    'component_id': 'debug_message_status',
                    'content': '<span class="ms-1 badge rounded-pill text-bg-danger">Must Have a Target</span>'
                },
                {
                    'component_id': 'text_message_input_box',
                    'content': '<input type="text" class="form-control" id="text_message_input" name="message" placeholder="Hey! This is a test message!" disabled>'
                },
                {
                    'component_id': 'send_debug_message_button',
                    'content': '<input type="submit" value="Send" form="send_debug_message" class="btn btn-success btn-sm me-1" disabled></input>'
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

            return 1
        except Exception as e:
            logging.error(e)
            return 0


WHATSAPP = Whatsapp()
