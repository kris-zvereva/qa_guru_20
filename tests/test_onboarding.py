from allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have, be


def test_wikipedia_onboarding(mobile_management):
    """Test Wikipedia app onboarding flow - 4 screens"""

    with step('Verify Screen 1: The Free Encyclopedia'):
        browser.element((
            AppiumBy.ID,
            'org.wikipedia.alpha:id/primaryTextView'
        )).should(have.text('The Free Encyclopedia'))

    with step('Navigate to Screen 2'):
        browser.element((
            AppiumBy.ID,
            'org.wikipedia.alpha:id/fragment_onboarding_forward_button'
        )).click()

    with step('Verify Screen 2: New ways to explore'):
        browser.element((
            AppiumBy.ID,
            'org.wikipedia.alpha:id/primaryTextView'
        )).should(have.text('New ways to explore'))

    with step('Navigate to Screen 3'):
        browser.element((
            AppiumBy.ID,
            'org.wikipedia.alpha:id/fragment_onboarding_forward_button'
        )).click()

    with step('Verify Screen 3: Reading lists with sync'):
        browser.element((
            AppiumBy.ID,
            'org.wikipedia.alpha:id/primaryTextView'
        )).should(have.text('Reading lists with sync'))

    with step('Navigate to Screen 4'):
        browser.element((
            AppiumBy.ID,
            'org.wikipedia.alpha:id/fragment_onboarding_forward_button'
        )).click()

    with step('Verify Screen 4: Data & Privacy'):
        browser.element((
            AppiumBy.ID,
            'org.wikipedia.alpha:id/primaryTextView'
        )).should(have.text('Data & Privacy'))

    with step('Complete onboarding - click Get Started'):
        browser.element((
            AppiumBy.ID,
            'org.wikipedia.alpha:id/fragment_onboarding_done_button'
        )).click()

    with step('Verify main screen is displayed'):
        browser.element((
            AppiumBy.ID,
            'org.wikipedia.alpha:id/main_toolbar_wordmark'
        )).should(be.visible)
