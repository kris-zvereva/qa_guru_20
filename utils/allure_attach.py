import requests
from allure_commons.types import AttachmentType
import allure


def attach_bstack_video(session_id: str, bstack_username: str, bstack_access_key: str):
    """Получает ссылку на видео из BrowserStack и прикрепляет к Allure отчету"""
    bstack_session_url = f'https://api.browserstack.com/app-automate/sessions/{session_id}.json'

    try:
        response = requests.get(
            bstack_session_url,
            auth=(bstack_username, bstack_access_key),
            timeout=10
        )
        response.raise_for_status()

        session_data = response.json()
        video_url = session_data.get('automation_session', {}).get('video_url')

        if video_url:
            allure.attach(
                body=f'<a href="{video_url}">BrowserStack Video</a>',
                name='Test Video',
                attachment_type=AttachmentType.HTML
            )
    except requests.exceptions.RequestException as e:
        print(f"Failed to get BrowserStack video: {e}")

def add_screenshot(browser):
    """Attach screenshot to Allure report"""
    png = browser.driver.get_screenshot_as_png()
    allure.attach(
        body=png,
        name='screenshot',
        attachment_type=AttachmentType.PNG,
        extension='.png'
    )
