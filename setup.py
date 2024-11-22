from setuptools import setup, find_packages

setup(
    name='module-browser_manager',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'undetected-chromedriver',
        'selenium',
        'selenium-stealth',
        'webdriver-manager',
    ],
    description='Утилита для управления браузерами с использованием undetected_chromedriver.'
                'Управление браузером (инициализация, настройка драйвера, работа с прокси и т.д.).',
    author='cherseroff',
    author_email='proffitm1nd@gmail.com',
    url='https://github.com/cherseroff27/module-browser_manager.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)