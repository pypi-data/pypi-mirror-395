import requests
from retry import retry

from ..logger import logger
from ..exceptions import (
    APICaptchaNotReady,
    APICaptchaUnsolvable,
    ParamsException,
    LowBalanceException,
    ServiceProviderException,
    APICaptchaNoSlotAvailableException,
    APICaptchaWrongCaptchaID,
)

API = {"captcha.guru": "http://api.cap.guru", "2captcha": "http://2captcha.com"}


class CaptchaGuru2Captcha(object):
    """
    API Interface for captcha.guru and 2captcha.com captcha solving providers

    http://learn.captcha.guru/#/
    https://2captcha.com/2captcha-api
    """

    def __init__(self, service_provider_name, service_provider_key):
        """
        Check account money balance before initialization

        :param str service_provider_name: 'captcha.guru' or '2captcha'
        :param str service_provider_key: Valid captcha.guru or 2captcha api key
        """
        self.url = API[service_provider_name]
        self.api_key = service_provider_key
        self.api_request_id = None

        self.check_balance()

    def check_balance(self):
        """
        Check account money balance

        :raises ParamsException: if incorrect 'api_key' provided
        :raises LowBalanceException: if money account balance is low
        """
        response = requests.get("{}/res.php?action=getbalance&key={}&json=1".format(self.url, self.api_key))

        logger.info(response.text)
        if response.status_code != 200:
            raise ServiceProviderException("Request to the Service Provider has failed!")

        json = response.json()
        if json["request"] == "ERROR_WRONG_USER_KEY" or json["request"] == "ERROR_KEY_DOES_NOT_EXIST":
            raise ParamsException("Incorrect api_key provided. Cannot get data!")
        if float(json["request"]) <= 10.00:
            raise LowBalanceException(
                "Account money balance is very low: {}! Put something there".format(json["request"])
            )

    def get_in(self, payload):
        """
        Send GET to in.php endpoint. Obtain request id that should be used in get_res

        :param str payload: valid params for GET in.php request
        """
        logger.info(payload)
        response = requests.get("{}/in.php?key={}&{}&json=1".format(self.url, self.api_key, payload))

        logger.info(response.text)
        if response.status_code != 200:
            raise ServiceProviderException("Request to the Service Provider has failed!")

        json = response.json()
        self.api_request_id = json["request"]

    def post_in(self, post_body):
        """
        Send POST to in.php endpoint. Obtain request id that should be used in get_res

        :param str post_body: base64 encoded image
        """
        data = {
            "key": self.api_key,
            "method": "base64",
            "body": post_body,
            "json": 1,
        }
        response = requests.post("{}/in.php".format(self.url), data)

        logger.info(response.text)
        if response.status_code != 200:
            raise ServiceProviderException("Request to the Service Provider has failed!")

        json = response.json()
        self.api_request_id = json["request"]

    @retry(
        exceptions=(
            APICaptchaNotReady,
            APICaptchaNoSlotAvailableException,
            APICaptchaWrongCaptchaID,
        ),
        delay=3,
        tries=60,
    )
    def get_res(self):
        """
        Send GET to res.php endpoint. Return token for request id

        :return: captcha token
        :raises APICaptchaNotReady: if CAPTCHA_NOT_READY response
        :raises APICaptchaNoSlotAvailableException: if ERROR_NO_SLOT_AVAILABLE response
        :raises APICaptchaWrongCaptchaID: if ERROR_WRONG_CAPTCHA_ID response
        :raises APICaptchaUnsolvable: if ERROR_CAPTCHA_UNSOLVABLE response
        """
        response = requests.get(
            "{}/res.php?key={}&action=get&id={}&json=1".format(self.url, self.api_key, self.api_request_id)
        )

        logger.info(response.text)
        if response.status_code != 200:
            raise ServiceProviderException("Request to the Service Provider has failed!")

        json = response.json()
        # Handle both the correct spelling and the API's typo
        if json["request"] == "CAPTCHA_NOT_READY" or json["request"] == "CAPCHA_NOT_READY":
            raise APICaptchaNotReady()

        if json["request"] == "ERROR_NO_SLOT_AVAILABLE":
            raise APICaptchaNoSlotAvailableException()

        if json["request"] == "ERROR_WRONG_CAPTCHA_ID":
            raise APICaptchaWrongCaptchaID(f"Incorrect captcha ID: {self.api_request_id}")

        if json["request"] == "ERROR_CAPTCHA_UNSOLVABLE":
            raise APICaptchaUnsolvable()

        if json["status"] == 1:
            return json["request"]
