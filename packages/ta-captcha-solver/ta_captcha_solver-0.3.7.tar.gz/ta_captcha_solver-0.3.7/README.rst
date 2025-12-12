==================
ta-captcha-solver
==================


.. image:: https://img.shields.io/pypi/v/ta_captcha_solver.svg
        :target: https://pypi.python.org/pypi/ta_captcha_solver

.. image:: https://img.shields.io/travis/macejiko/ta_captcha_solver.svg
        :target: https://travis-ci.com/macejiko/ta_captcha_solver

.. image:: https://readthedocs.org/projects/ta-captcha/badge/?version=latest
        :target: https://ta-captcha.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

|

Thoughtful Captcha Solver

|

Installation
------------

::

   python3 -m virtualenv venv
   source venv/bin/activate
   pip install ta-captcha-solver

|

How to Use
----------

1. Make sure your browser instance is on the page with captcha or provide a correct path to image in *image_source* param
2. Use **TACaptchaSolver.get()** method with appropriate *params*
3. Call **captcha.solve()** method that would do all the magic

|

Supported Browsers
------------------

Currently only **RPA.Browser.Selenium.Selenium()** is supported. In future we will add a **Playwright** support as well

|

Supported Service Providers
---------------------------

Currently we support these:

1. http://learn.captcha.guru/#/
2. https://2captcha.com/2captcha-api

You should have valid API key that could be obtained from web version of service after you put some money to the account balance

|

Supported Captcha Types
---------------------------

Currently we support these:

1. CloudFlare
2. CloudFlare Challenge
3. Arkose Labs Fun Captcha
4. HCaptcha
5. ReCaptcha v2
6. Image Captcha

|

Available Settings
------------------

If param is not required and not set then this action would not be performed and you a responsible for it. E.g. if you dont provide *check_xpath* then you should check that captcha has been solved by you own.

+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| Param                | Required          | Type  | Description                                                             |
+======================+===================+=======+=========================================================================+
| captcha_type         | Yes               | All   | One of supported captcha types                                          |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| browser              | Yes for 'v2' and  | All   | Supported browser instance with opened captcha page                     |
|                      | 'fun_captcha'     |       |                                                                         |
|                      | For 'image' only  |       |                                                                         |
|                      | when image_source |       |                                                                         |
|                      | is not provided.  |       |                                                                         |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| captcha_guru_api_key | No                | All   | Deprecated. Use 'service_provider_name' + 'service_provider_key' instead|
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| service_provider_name| Yes               | All   | Value should be: 'captcha.guru' or '2captcha'                           |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| serivce_provider_key | Yes               | All   | Valid API key of appropriate Service Provider                           |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| image_xpath          | Yes if            | Image | Locator of <img> with captcha pic                                       |
|                      | browser           |       |                                                                         |
|                      | is provided       |       |                                                                         |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| input_xpath          | No                | Image | Locator of input field for token                                        |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| click_xpath          | No                | All   | Locator of submit button                                                |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| check_xpath          | No                | All   | Locator that should be verified after solving                           |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| upper                | No                | Image | Perform token.upper()                                                   |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+
| image_source         | Yes if browser    | Image | Path to .png or .jpg image with captcha to solve                        |
|                      | not provided      |       |                                                                         |
+----------------------+-------------------+-------+-------------------------------------------------------------------------+

|

Examples
--------

.. code:: python

   from RPA.Browser.Selenium import Selenium
   from ta_captcha_solver.ta_captcha_solver import TACaptchaSolver

   browser = Selenium()
   browser.open_browser("http://url_with_captcha")

   captcha = TACaptchaSolver.get(
       captcha_type="v2",
       browser=browser,
       service_provider_name="captcha.guru",
       service_provider_key="captcha.guru API KEY",
   )
  captcha.solve()

.. code:: python

   from RPA.Browser.Selenium import Selenium
   from ta_captcha_solver.ta_captcha_solver import TACaptchaSolver

   browser = Selenium()
   browser.open_browser("http://url_with_captcha")

   captcha = TACaptchaSolver.get(
       captcha_type="image",
       browser=browser,
       service_provider_name="captcha.guru",
       service_provider_key="captcha.guru API KEY",
       image_xpath="//img[@id='demoCaptcha_CaptchaImage']",
       input_xpath="//input[@id='captchaCode']",
       click_xpath="//input[@id='validateCaptchaButton']",
       check_xpath="//span[@id='validationResult']/span[@class='correct']",
       upper=False,
   )
  captcha.solve()

.. code:: python

   from RPA.Browser.Selenium import Selenium
   from ta_captcha_solver.ta_captcha_solver import TACaptchaSolver

   browser = Selenium()
   browser.open_browser("http://url_with_captcha")

   captcha = TACaptchaSolver.get(
       captcha_type="fun_captcha",
       browser=self.browser,
       service_provider_name="2captcha",
       service_provider_key="2captcha API KEY"
       check_xpath="//input[@id='username']",
   )
   captcha.solve()

.. code:: python

   from ta_captcha_solver.ta_captcha_solver import TACaptchaSolver

   captcha = TACaptchaSolver.get(
       captcha_type="image",
       service_provider_name="2captcha",
       service_provider_key="2captcha API KEY",
       image_source= "C:/your-path-to-image-captcha.png",
       upper=False,
   )
  captcha.solve()
  token = captcha.token

Development
-----------

**Prepare local dev env:**

::

   python3 -m virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt

**Testing:**

::

   CAPTCHA_GURU_API_KEY=XXX TWO_CAPTCHA_API_KEY=YYY pytest
