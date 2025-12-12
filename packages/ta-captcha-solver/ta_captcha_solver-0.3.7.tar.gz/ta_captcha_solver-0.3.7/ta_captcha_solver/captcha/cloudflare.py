from twocaptcha import TwoCaptcha
from ta_captcha_solver.captcha.captcha import Captcha
from ta_captcha_solver.exceptions import NoCaptchaException


class CloudflareTurnstile(Captcha):
    """
    Cloudflare captcha solver
    """

    def solve(self):
        self._get_data()
        solver = TwoCaptcha(self.service_provider.api_key)
        result = solver.turnstile(sitekey=self.key, url=self.page_url)
        self.token = result["code"]
        self._put_token()
        return super().solve()

    def _get_data(self):
        try:
            site_key_element = self.browser.find_element("//*[@data-sitekey]")
        except Exception as ex:
            raise NoCaptchaException("Cannot find site_key_element on the page! Error: " + str(ex))

        try:
            self.key = site_key_element.get_attribute("data-sitekey")
        except Exception as ex:
            raise NoCaptchaException("Cannot get site_key_value on the page! Error: " + str(ex))

        self.page_url = self.browser.browser.location

    def _put_token(self):
        self.browser.execute_javascript(
            f"document.querySelector('[name=\"cf-turnstile-response\"]').value = '{self.token}';"
        )
