from abc import ABC
from collections import defaultdict

from ..exceptions import UICaptchaNotSolved

from ..browser.browser import Browser
from ..service_provider.service_provider import ServiceProvider
from urllib.parse import unquote_plus


class Captcha(ABC):
    """
    Abstract base class for all captchas in this package
    """

    def __init__(self, **params):
        """
        :param params: Captcha settings
        """

        self.params = defaultdict(str, params)

        # Respect deprecated param
        if self.params["captcha_guru_api_key"]:
            self.params["service_provider_name"] = "captcha.guru"
            self.params["service_provider_key"] = self.params["captcha_guru_api_key"]

        self.service_provider = ServiceProvider.get(**self.params)

        if not self.params["image_source"]:
            self.browser = Browser(params["browser"])

        self.token = None

    def solve(self):
        """
        Core method that actually solves captcha according to settings
        """
        if self.params["click_xpath"]:
            self.click_solve_captcha()

        if self.params["check_xpath"]:
            self.check_captcha()

        return True

    def click_solve_captcha(self):
        """
        Click 'click_xpath' element after captcha solved
        """
        self.browser.click_element_when_visible(self.params["click_xpath"])

    def check_captcha(self):
        """
        Check page contains 'check_xpath'. The last step of captcha solving workflow

        :raises UICaptchaNotSolved: if 'check_xpath' not found. This means that captcha is not solved
        """
        try:
            self.browser.wait_until_page_contains_element(self.params["check_xpath"], timeout=5)
        except Exception:
            raise UICaptchaNotSolved()

    def _get_url(self):
        self.page_url = unquote_plus(
            self.browser.execute_javascript(
                """
                let page_url = window.location.href;
                return page_url;
                """
            )
        )
