from collections import defaultdict

from .captcha.hcaptcha import HCaptcha
from .captcha.cloudflare import CloudflareTurnstile
from .captcha.image_captcha import ImageCaptcha
from .captcha.re_captcha_v2 import ReCaptchaV2
from .captcha.fun_captcha import FunCaptcha
from .captcha.cloudflare_challenge import CloudflareTurnstileChallenge

from .exceptions import ParamsException


class TACaptchaSolver(object):
    """
    Main interface for package users

    Example:
        captcha = TACaptchaSolver.get(
            captcha_type="v2",
            browser=self.browser,
            service_provider_name="captcha.guru",
            service_provider_key=self.captcha_guru_api_key,
            click_xpath="//input[@id='recaptcha-demo-submit']",
            check_xpath="//div[@class='recaptcha-success']",
        )
        captcha.solve()
    """

    @staticmethod
    def get(**params):
        """
        Return instance of captcha according to provided params

        :param params: Captcha settings. Possible values:
            - captcha_type: 'v2' or 'image' or 'fun_captcha'. Required
            - browser: Instance of RPA.Browser.Selenium.Selenium().
                       Required for 'v2' and 'image' and 'fun_captcha' captcha in case image_source is not provided
            - captcha_guru_api_key: Valid api key. Deprecated.
                       Use 'service_provider_name' + 'service_provider_key' instead!
            - service_provider_name: 'captcha.guru' or '2captcha'. Required
            - service_provider_key: 3rd party Service Provider valid API key. Required
            - image_xpath: Image with captcha. Required for image captcha if browser is provided.
            - input_xpath: Input token to this input field. Valid for image captcha
            - click_xpath: Click button after captcha solved
            - check_xpath: Search for locator after captcha submitted
            - upper: make Solved token.upper() for image captcha. Valid for image captcha
            - image_source: path to image file. Required for 'image' captcha if browser is not provided.
        :raises ParamsException: if 'captcha_type' has unexisting captcha type
        """
        params = TACaptchaSolver.validate_params(**params)

        if "image" in params["captcha_type"]:
            return ImageCaptcha(**params)
        elif "v2" in params["captcha_type"]:
            return ReCaptchaV2(**params)
        elif "fun_captcha" in params["captcha_type"]:
            return FunCaptcha(**params)
        elif "cloudflare_turnstile" in params["captcha_type"]:
            return CloudflareTurnstile(**params)
        elif "cloudflare_challenge" in params["captcha_type"]:
            return CloudflareTurnstileChallenge(**params)
        elif "hcaptcha" in params["captcha_type"]:
            return HCaptcha(**params)
        else:
            raise ParamsException(
                "Incorrect captcha_type '{}' provided. Dont know what captcha need to solve!".format(
                    params["captcha_type"]
                )
            )

    @staticmethod
    def validate_params(**params):
        """
        Check all provided params

        :return: validated params
        :raises ParamsException: if some param has incorrect value or required param doesnt exist
        """
        params = defaultdict(str, params)

        if not params["captcha_type"] or not isinstance(params["captcha_type"], str):
            raise ParamsException(
                "No captcha_type provided or incorrect data type. Dont know what captcha need to solve!"
            )

        if params["captcha_type"] == "image":
            if not params["browser"] and (not params["image_source"]):
                raise ParamsException("No browser or image source provided. Cannot work without neither!")

            elif params["browser"] and params["image_source"]:
                raise ParamsException("Browser and image source both provided. Please submit just one.")

            elif params["browser"] and (not params["image_xpath"]):
                raise ParamsException("No image_xpath provided. Cannot work witouht image with captcha!")

            elif not (".jpg" in params["image_source"] or ".png" in params["image_source"]) and (not params["browser"]):
                raise ParamsException("No image path valid provided on image_source. Cannot work without a valid path!")

        if params["captcha_type"] == "v2" or params["captcha_type"] == "fun_captcha":
            if not params["browser"]:
                raise ParamsException("No browser provided. Cannot work wiithout any browser!")

        if not ((params["service_provider_name"] and params["service_provider_key"]) or params["captcha_guru_api_key"]):
            raise ParamsException("No Service Provider Name or Key provided. Cannot work without third party API tool!")

        return params
