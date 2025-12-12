from ..exceptions import ParamsException
from .captcha_guru_2_captcha import CaptchaGuru2Captcha


class ServiceProvider(object):
    """
    Factory that returns Service Provider for captcha solving
    """

    @staticmethod
    def get(**params):
        """
        Factory method that returns Service Provider for captcha solving

        :param params: Captcha settings. Required values here:
            - service_provider_name
            - service_provider_key
        """
        if params["service_provider_name"] == "captcha.guru" or params["service_provider_name"] == "2captcha":
            return CaptchaGuru2Captcha(params["service_provider_name"], params["service_provider_key"])
        else:
            raise ParamsException("Unknown Service Provider: {}".format(params["service_provider_name"]))
