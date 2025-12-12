from twocaptcha import TwoCaptcha
from ta_captcha_solver.captcha.captcha import Captcha
from ta_captcha_solver.exceptions import NoCaptchaException


class HCaptcha(Captcha):
    """HCaptcha solver."""

    def solve(self):
        self._get_data()
        solver = TwoCaptcha(self.service_provider.api_key)
        result = solver.hcaptcha(sitekey=self.key, url=self.page_url)
        self.token = result["code"]
        self._put_token()
        self._execute_callback()
        return super().solve()

    def _get_data(self):
        """Get all HCatpcha info."""
        try:
            site_key_element = self.browser.find_element("//*[@data-sitekey]")
            self.key = site_key_element.get_attribute("data-sitekey")
        except Exception as ex:
            raise NoCaptchaException("Cannot find hCaptcha HTML stuff on the page! Error: " + str(ex))

        try:
            self.callback = site_key_element.get_attribute("data-callback")
        except Exception:
            self.callback = False

        self.page_url = self.browser.browser.location

    def _put_token(self):
        """Put token to appropriate HTML tags."""
        self.browser.execute_javascript(
            "document.getElementsByName('g-recaptcha-response')[0].innerHTML='{}'".format(self.token)
        )
        self.browser.execute_javascript(
            "document.getElementsByName('h-captcha-response')[0].innerHTML='{}'".format(self.token)
        )

    def _execute_callback(self):
        """One of the parts of solving workflow after token put to appropriate HTML tag."""
        if self.callback:
            self.browser.execute_javascript("{}('{}')".format(self.callback, self.token))
