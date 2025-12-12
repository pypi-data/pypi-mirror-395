from RPA.Browser.Selenium import Selenium


class Browser(object):
    """
    Wrapper for all used broweser / driver
    """

    def __init__(self, browser):
        """
        :param browser: Instance of RPA.Browser.Selenium.Selenium()
        :raises NotImplementedError: if browser type is not supported
        """
        self.browser = browser

        if isinstance(browser, Selenium):
            self.browser_type = "Selenium"
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def wait_until_page_contains_element(self, xpath, timeout):
        """
        :param str xpath: What xpath search for
        :param int timeout: Wait time in seconds
        :raises NotImplementedError: if browser type is not supported
        """
        if self.browser_type == "Selenium":
            return self.browser.wait_until_page_contains_element(xpath, timeout)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def click_element_when_visible(self, xpath):
        """
        :param str xpath: Xpath that will be clicked
        :raises NotImplementedError: if browser type is not supported
        """
        if self.browser_type == "Selenium":
            self.browser.click_element_when_visible(xpath)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def press_keys(self, key):
        """
        :param selenium.webdriver.common.keys.Keys key: Simulate pressing of particular key
        :raises NotImplementedError: if browser type is not supported
        """
        if self.browser_type == "Selenium":
            self.browser.press_keys(None, key)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def execute_javascript(self, code):
        """
        :param str code: Valid JS code that will be executed
        :raises NotImplementedError: if browser type is not supported
        """
        if self.browser_type == "Selenium":
            return self.browser.execute_javascript(code)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def find_element(self, xpath):
        """
        Tries to find element on the page

        :param str xpath
        :raises NotImplementedError: if browser type is not supported
        """
        if self.browser_type == "Selenium":
            return self.browser.find_element(xpath)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def select_frame(self, xpath):
        """
        Selects frame

        :param str xpath
        :raises NotImplementedError: if browser type is not supported
        """
        if self.browser_type == "Selenium":
            return self.browser.select_frame(xpath)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def unselect_frame(self):
        """
        Sets frame to the main frame

        :param str xpath
        :raises NotImplementedError: if browser type is not supported
        """
        if self.browser_type == "Selenium":
            return self.browser.unselect_frame()
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def go_to(self, url):
        """
        Goes to specific URL

        :param str url
        :raises NotImplementedError: if browser type is not supported
        """
        if self.browser_type == "Selenium":
            return self.browser.go_to(url)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")

    def execute_cdp(self, param_name, param_property):
        """
        Executes Commands on the driver

        :param str param_name
        :param str param_property
        :raises NotImplementedError: if browser type is not supported
        """
        if self.browser_type == "Selenium":
            return self.browser.execute_cdp(param_name, param_property)
        else:
            raise NotImplementedError("Currently only Selenium is supported!")
