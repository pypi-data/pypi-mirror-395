from twocaptcha import TwoCaptcha
from ta_captcha_solver.captcha.captcha import Captcha
from time import sleep
import requests
from ..logger import logger
from ..exceptions import APICaptchaNotReady, NoCaptchaException
from retry import retry


class CloudflareTurnstileChallenge(Captcha):
    """
    Cloudflare Challenge captcha solver
    """

    def solve(self):
        self._get_url()
        self._inject_script()
        data = self._get_data()

        if data is None:
            raise NoCaptchaException("Cloudflare Turnstile Challenge captcha is missing")

        solver = TwoCaptcha(self.service_provider.api_key)
        result = solver.turnstile(
            sitekey=data["sitekey"],
            action=data["action"],
            data=data["data"],
            pagedata=data["pagedata"],
            url=self.page_url,
        )
        id_captcha = result["captchaId"]
        self._put_token(id_captcha=id_captcha)
        return super().solve()

    def _get_data(self):
        self.browser.go_to(self.page_url)
        sleep(1)
        website_data = self.browser.execute_javascript("return values")
        return website_data

    @retry(APICaptchaNotReady, delay=5, tries=5)
    def _put_token(self, id_captcha):
        url = f"https://2captcha.com/res.php?key={self.service_provider.api_key}&action=get&id={id_captcha}&json=1"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            logger.info(data)
        else:
            raise APICaptchaNotReady("Failure in resolving the captcha.")

        solved_captcha = data["request"]
        self.browser.execute_javascript(f" tsCallback('{solved_captcha}');")

    def _inject_script(self):
        js_code = """
        let values;
        const i = setInterval(() => {
            if (window.turnstile) {
                clearInterval(i)
                window.turnstile.render = (a, b) => {
                    values = {
                        method: "turnstile",
                        key: "%s",
                        sitekey: b.sitekey,
                        pageurl: window.location.href,
                        data: b.cData,
                        pagedata: b.chlPageData,
                        action: b.action,
                        userAgent: navigator.userAgent,
                        json: 1
                    }
                    console.log(JSON.stringify(values))
                    window.tsCallback = b.callback
                    return 'foo'
                }
            }
        }, 50)
        """ % (
            self.service_provider.api_key
        )
        self.browser.execute_cdp("Page.addScriptToEvaluateOnNewDocument", {"source": js_code})
        self.browser.go_to(self.page_url)
