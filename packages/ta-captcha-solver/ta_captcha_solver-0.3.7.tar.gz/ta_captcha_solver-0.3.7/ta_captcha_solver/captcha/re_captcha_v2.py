from ..logger import logger
from .captcha import Captcha
from ..exceptions import NoCaptchaException
import time


class ReCaptchaV2(Captcha):
    """
    Google reCaptchaV2 solver
    """

    def solve(self):
        """
        Core method that performs solving according to previously provided settings

        :return: True if solved
        """
        try:
            self._get_data()
        except Exception:
            raise NoCaptchaException("Cannot find ReCaptchaV2 on the page!")

        payload = "method=userrecaptcha&googlekey={}&pageurl={}".format(self.key, self.page_url)
        self.service_provider.get_in(payload)
        self.token = self.service_provider.get_res()
        self._put_token()
        self._execute_callback()

        time.sleep(2)

        return super().solve()

    def _get_data(self):
        """
        Get all Google reCatpcha info. Obtains info for v2 and v3 captchas
        """
        data = self.browser.execute_javascript(
            """
        function findRecaptchaClients() {
  // eslint-disable-next-line camelcase
  if (typeof (___grecaptcha_cfg) !== 'undefined') {
    // eslint-disable-next-line camelcase, no-undef
    return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => {
      const data = { id: cid, version: cid >= 10000 ? 'V3' : 'V2' };
      const objects = Object.entries(client).filter(([_, value]) => value && typeof value === 'object');

      objects.forEach(([toplevelKey, toplevel]) => {
        const found = Object.entries(toplevel).find(([_, value]) => (
          value && typeof value === 'object' && 'sitekey' in value && 'size' in value
        ));

        if (typeof toplevel === 'object' && toplevel instanceof HTMLElement && toplevel['tagName'] === 'DIV'){
            data.pageurl = toplevel.baseURI;
        }

        if (found) {
          const [sublevelKey, sublevel] = found;

          data.sitekey = sublevel.sitekey;
          const callbackKey = data.version === 'V2' ? 'callback' : 'promise-callback';
          const callback = sublevel[callbackKey];
          if (!callback) {
            data.callback = null;
            data.function = null;
          } else {
            data.function = callback;
            const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `['${key}']`).join('');
            data.callback = `___grecaptcha_cfg.clients${keys}`;
          }
        }
      });
      return data;
    });
  }
  return [];
}

let res = findRecaptchaClients();
return res
        """
        )
        logger.info(data)
        self.key = data[0]["sitekey"]
        self.page_url = data[0]["pageurl"]
        self.function = data[0]["function"]
        self.callback = data[0]["callback"]

    def _put_token(self):
        """
        Put token to appropriate HTML tag
        """
        self.browser.execute_javascript(
            "document.getElementById('g-recaptcha-response').innerHTML='{}'".format(self.token)
        )

    def _execute_callback(self):
        """
        One of the parts of solving workflow after token put to appropriate HTML tag
        """
        if self.function:
            self.browser.execute_javascript("{}('{}')".format(self.function, self.token))
            return
        if self.callback:
            self.browser.execute_javascript("{}('{}')".format(self.callback, self.token))
