import os
import random

import undetected_chromedriver as uc
from selenium.common import WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager


# Модуль из my_utils/modules
class BrowserManager:
    def __init__(self, proxy_manager=None, user_agent=None):
        self.driver = None
        self.proxy_manager = proxy_manager
        self.user_agent = user_agent


    def initialize_webdriver(
            self,
            browser_profiles_dir=None,
            profile_name=None,
            use_profile_folder=False,
            use_proxy=False,
            use_stealth=False
    ):
        try:
            if use_profile_folder:
                # Проверяем, что параметры, связанные с профилем, переданы
                if not browser_profiles_dir or not profile_name:
                    raise ValueError(
                        "Если 'use_profile_folder=True', необходимо указать 'browser_profiles_dir' и 'profile_name'."
                    )

            chrome_options = webdriver.ChromeOptions()
            service = Service(ChromeDriverManager().install())

            if use_profile_folder:
                project_dir = os.getcwd()
                profile_dir = os.path.join(project_dir, browser_profiles_dir, profile_name)
                self.get_profile_directory(profile_dir)
                chrome_options.add_argument(f"--user-data-dir={profile_dir}")

            if use_proxy and self.proxy_manager is not None:
                plugin_file = self.proxy_manager.create_extension()
                chrome_options.add_extension(plugin_file)
            else:
                chrome_options.add_argument("--disable-extensions")

            if self.user_agent is not None:
                chrome_options.add_argument(f'--user-agent={self.user_agent}')

            chrome_options.page_load_strategy = "eager" if random.randint(1, 10) > 9 else "normal"
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")

            self.driver = uc.Chrome(service=service, options=chrome_options)

            if use_stealth:
                stealth(driver=self.driver,
                        languages=["ru-RU", "ru", "en-US", "en"],
                        vendor="Google Inc.",
                        platform="Win32",
                        webgl_vendor="Intel Inc.",
                        renderer="Intel Iris OpenGL Engine",
                        fix_hairline=True,
                        run_on_insecure_origins=True,
                        disable_webrtc = True
                        )

            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                'source': '''
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                  '''
            })

            return self.driver
        except Exception as ex:
            print(ex)


    @staticmethod
    def get_profile_directory(profile_dir):
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir, exist_ok=True)
            print(f"Успешно создал новую папку профиля браузера в директории проекта. Чиназес.\n"
                  f"Путь к папке профиля - {profile_dir}")
            return profile_dir
        else:
            print(f"Папка профиля браузера уже существует. Чивапчис.\n"
                  f"Путь к папке профиля - {profile_dir}")
            return profile_dir


    def close_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except WebDriverException as e:
                print(f"Error closing browser: {e}")
            finally:
                self.driver = None
