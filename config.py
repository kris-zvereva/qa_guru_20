import os
from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from appium.options.android import UiAutomator2Options


class Config(BaseSettings):
    """Конфигурация для Appium тестов"""

    context: Literal['local_emulator', 'bstack'] = 'local_emulator'

    # Appium settings
    remote_url: str

    # Android capabilities
    platform_name: str = 'Android'
    platform_version: str
    device_name: str
    automation_name: str = 'UiAutomator2'
    app_wait_activity: Optional[str] = None

    # App path
    app: str

    # App package and activity
    app_package: Optional[str] = None
    app_activity: Optional[str] = None

    # BrowserStack specific
    bstack_username: Optional[str] = None
    bstack_access_key: Optional[str] = None
    bstack_project_name: str = 'Wikipedia_Tests'
    bstack_build_name: str = 'Onboarding_Tests'
    bstack_session_name: str = 'Wikipedia_Onboarding'

    # Timeouts
    timeout: float = 10.0

    model_config = SettingsConfigDict(
        env_file=('.env.credentials', f'.env.{os.getenv("CONTEXT", "local_emulator")}'),
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )


def to_driver_options(config: Config) -> UiAutomator2Options:
    """
    Преобразует Config в UiAutomator2Options для Appium
    """
    options = UiAutomator2Options()

    # Общие capabilities
    options.platform_name = config.platform_name
    options.platform_version = config.platform_version
    options.device_name = config.device_name
    options.automation_name = config.automation_name

    if config.app_wait_activity:
        options.set_capability('appWaitActivity', config.app_wait_activity)

    if config.app_package:
        options.app_package = config.app_package

    if config.app_activity:
        options.app_activity = config.app_activity

    # Для локального эмулятора
    if config.context == 'local_emulator':
        # Превращаем относительный путь в абсолютный
        app_path = os.path.abspath(config.app)
        options.app = app_path

    # Для BrowserStack
    elif config.context == 'bstack':
        options.app = config.app  # для bstack это может быть bs://... или URL
        options.set_capability(
            'bstack:options', {
                'projectName': config.bstack_project_name,
                'buildName': config.bstack_build_name,
                'sessionName': config.bstack_session_name,
                'userName': config.bstack_username,
                'accessKey': config.bstack_access_key,
            }
        )

    return options


# Создаем экземпляр конфига
config = Config()