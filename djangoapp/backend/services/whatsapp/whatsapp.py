# D:\vscode\djangoapp-docker-base\djangoapp\app\tests.py

import os
from io import BytesIO
from time import sleep

from django.conf import settings
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Whatsapp():
    fixtures = [
        'app/fixtures/app.json',
        ...
    ]

    def start(self):
        try:
            selenium_grid_url = "http://selenium:4444/wd/hub"
            options = webdriver.FirefoxOptions()
            self.browser = webdriver.Remote(command_executor=selenium_grid_url,
                                            keep_alive=True,
                                            options=options)
            self.browser.get('https://web.whatsapp.com/')
            return 1
        except Exception as e:
            print(e)
            return 0

    def stop(self):
        try:
            self.browser.quit()
            return 1
        except Exception as e:
            print(e)
            return 0

    def is_running(self):
        try:
            if self.browser.session_id:
                return 1
            return 0
        except Exception as e:
            print(e)
            return 0

    def is_qr_code_on_screen(self):
        qrcode_xpath = '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas'
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, qrcode_xpath)))
            return 1
        except TimeoutException as te:
            print(te)
            return 0
        except Exception as e:
            print(e)
            return 0

    def save_qrcode(self):
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
            print(img_path)
            return 1
        except Exception as e:
            print(e)
            return 0

    def send_message(self, target, text_to_send):
        try:
            target_xpath = '//span[contains(@title,"' + target + '")]'
            WebDriverWait(self.browser, 100).until(
                EC.presence_of_element_located((By.XPATH, target_xpath))).click()

            sleep(1)
            message_box_xpath = '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
            message_box = WebDriverWait(self.browser, 100).until(
                EC.presence_of_element_located((By.XPATH, message_box_xpath)))
            ActionChains(self.browser).move_to_element(
                message_box).click().send_keys(text_to_send, Keys.ENTER).perform()

            sleep(10)

            return 1
        except Exception as e:
            print(e)
            return 0


WHATSAPP = Whatsapp()
