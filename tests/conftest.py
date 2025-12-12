import os
import pytest
from appium import webdriver
from selene import browser
from dotenv import load_dotenv
from config import Config, to_driver_options
from utils.allure_attach import attach_bstack_video


def pytest_addoption(parser):
    """Добавляем опцию --context для выбора окружения"""
    parser.addoption(
        '--context',
        action='store',
        default='local_emulator',
        help='Контекст запуска: local_emulator или bstack'
    )


def pytest_configure(config):
    """Загружаем .env файл ДО создания конфига"""
    context = config.getoption('--context')

    # Загружаем credentials (если есть)
    if os.path.exists('.env.credentials'):
        load_dotenv('.env.credentials')

    # Загружаем основной .env файл
    env_file = f'.env.{context}'
    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)

    # Устанавливаем переменную окружения для Config
    os.environ['CONTEXT'] = context


@pytest.fixture(scope='session')
def context(request):
    """Получаем context из командной строки"""
    return request.config.getoption('--context')


@pytest.fixture(scope='session')
def config_instance():
    """Загружаем конфигурацию (уже загружена в pytest_configure)"""
    return Config()


@pytest.fixture(scope='function')
def mobile_management(config_instance, context):
    """
    Фикстура для управления Appium сессией
    Запускает драйвер перед тестом, закрывает после
    """
    # Получаем options из конфига
    options = to_driver_options(config_instance)

    # Создаем Appium драйвер
    driver = webdriver.Remote(
        command_executor=config_instance.remote_url,
        options=options
    )

    # Настраиваем Selene для работы с мобильным драйвером
    browser.config.driver = driver
    browser.config.timeout = config_instance.timeout

    yield driver

    # Сохраняем session_id для BrowserStack видео
    session_id = driver.session_id

    # Закрываем сессию после теста
    browser.quit()

    if context == 'bstack' and config_instance.bstack_username:
        attach_bstack_video(
            session_id=session_id,
            bstack_username=config_instance.bstack_username,
            bstack_access_key=config_instance.bstack_access_key
        )
