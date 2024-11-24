import sys
import time
from browser_manager import BrowserManager


def main():
    # Простейший пример использования модуля
    browser_manager = BrowserManager()
    driver = browser_manager.initialize_webdriver()

    if driver is None:
        print("driver == None")
        sys.exit()

    driver.get("https://example.com/")
    time.sleep(5000)    # Задержка, чтобы увидеть, открылся ли сайт

    browser_manager.close_driver()


if __name__ == '__main__':
    main()