import base64
import os

from PIL import Image
from selenium.webdriver.common.keys import Keys

from .captcha import Captcha
from ..exceptions import NoCaptchaException, NoTokenCaptchaException


class ImageCaptcha(Captcha):
    """
    Standart image captcha
    """

    def __init__(self, **params):
        """
        :param params: Captcha settings. Possible values:
            - image_xpath: Image with captcha. Required if browser is provided.
            - input_xpath: Input token to this input field
            - click_xpath: Click button after captcha solved
            - check_xpath: Search for locator after captcha submitted
            - upper: Make solved token.upper() for image captcha
            - image_source: path to image file. Required if browser is not provided.
            - press_enter_when_solved: Press ENTER after token is solved.
        :raises ParamsException: if 'image_xpath' is not provided
        """
        super().__init__(**params)
        self.params.setdefault("press_enter_when_solved", True)

        if self.params["image_source"]:
            self.image_jpg_path = self.params["image_source"]
        else:
            self.image_jpg_path = os.path.join(os.getcwd(), "captcha_image.jpg")

    def solve(self):
        """
        Core method that performs solving according to previously provided settings

        :return: True if solved
        """
        if self.params["browser"]:
            self._get_captcha_img()

        try:
            self._encode_image()
        except Exception:
            raise NoCaptchaException("Cannot find ImageCaptcha!")

        self.service_provider.post_in(self.body)
        self.token = self.service_provider.get_res()
        if not self.token:
            raise NoTokenCaptchaException("No token was found. Please verify the credentials to service provider.")

        if self.params["upper"]:
            self.token = self.token.upper()

        if self.params["input_xpath"]:
            self._input_captcha()

        return super().solve()

    def _get_captcha_img(self):
        """
        Generate .jpg image with captcha in cwd
        """
        image_png_path = os.path.join(os.getcwd(), "captcha_image.png")
        self.browser.wait_until_page_contains_element(self.params["image_xpath"], timeout=5)
        with open(image_png_path, "wb") as f:
            image_element = self.browser.find_element(self.params["image_xpath"])
            f.write(image_element.screenshot_as_png)

        img = Image.open(image_png_path)
        rgb_im = img.convert("RGB")
        rgb_im.save(self.image_jpg_path, quality=10)
        os.remove(image_png_path)

    def _encode_image(self):
        """
        Encode existing .jpg image to base64
        """
        with open(self.image_jpg_path, "rb") as f:
            self.body = base64.b64encode(f.read())
        # Only remove temporary images created by the browser, not user-provided images
        if not self.params["image_source"]:
            os.remove(self.image_jpg_path)

    def _input_captcha(self):
        """
        Click 'input_xpath' then press all keys from token and press ENTER
        """
        self.browser.click_element_when_visible(self.params["input_xpath"])

        for d in self.token:
            self.browser.press_keys(str(d))

        if self.params["press_enter_when_solved"]:
            self.browser.press_keys(Keys.ENTER)
