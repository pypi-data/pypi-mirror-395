from retry import retry
from urllib.parse import unquote_plus
from .captcha import Captcha
from ..exceptions import FrameException, NoCaptchaException
from ..logger import logger


class FunCaptcha(Captcha):
    """
    Arkose Labs Fun Captcha solver
    """

    def solve(self):
        """
        Core method that performs solving according to previously provided settings

        :return: True if solved
        """
        try:
            self._get_data()
        except Exception:
            raise NoCaptchaException("Cannot find FunCaptcha on the page!")

        payload = "method=funcaptcha&publickey={}&surl={}&pageurl={}".format(self.key, self.surl, self.page_url)
        self.service_provider.get_in(payload)
        self.token = self.service_provider.get_res()

        self._put_token()
        self._execute_callback()

        return super().solve()

    @retry(FrameException, delay=1, tries=10)
    def _get_value(self):
        """
        Tries to get captcha information going through nested iframes

        :return: value with all information
        """
        frame_count = 0
        try:
            value = self.browser.execute_javascript(
                """
                let data = document.getElementsByName('fc-token')[0].value;
                return data;
                """
            )
        except Exception:
            self.browser.select_frame("(//iframe)[1]")
            frame_count = frame_count + 1
            raise FrameException("Selecting next frame...")

        for i in range(frame_count + 1):
            self.browser.unselect_frame()

        return value

    def _get_data(self):
        """
        Get all info required for captcha solving
        """
        self.page_url = self._get_url()

        value = self._get_value()
        logger.info(value)
        data = {k: v for (k, v) in [i.split("=") for i in value.split("|")[1:]]}
        self.key = data["pk"]
        self.surl = unquote_plus(data["surl"])

    def _put_token(self):
        """
        Tries to put final solving token to any possible place
        This is a best method to add a support for a new site with captcha
        """
        try:
            self.browser.execute_javascript(
                """
                let places = [];

                places.push(document.getElementsByName('captchaUserResponseToken')[0]);
                places.push(document.getElementById('fc-token'));
                places.push(document.getElementsByName('fc-token')[0]);

                for (const p of places) {{
                  if (typeof(p) != 'undefined' && p!= null) {{
                      p.value='{token}';
                      break;
                  }}
                }}
                """.format(
                    token=self.token
                )
            )
        except Exception:
            raise RuntimeError("Failed to put Fun Captcha token! Please contact LABs team!")

    def _execute_callback(self):
        """
        Tries to submit possible form
        Big chance to not work and in most cases should be solved by user
        """
        try:
            self.browser.execute_javascript(
                """
                try {
                  document.getElementById("captcha-challenge").submit();
                }
                catch (e) {
                  document.getElementsByTagName('form')[0].submit();
                }
                """
            )
        except Exception:
            logger.info("Failed to submit final form. Do it somehow else by yourown")
