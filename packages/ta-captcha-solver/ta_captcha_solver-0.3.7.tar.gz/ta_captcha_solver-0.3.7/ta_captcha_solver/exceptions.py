class CaptchaSolverException(Exception):
    """
    Base exception for all captcha solver exceptions
    """

    pass


class APICaptchaNotReady(CaptchaSolverException):
    """
    API: Captcha is still being solved
    """

    pass


class APICaptchaUnsolvable(CaptchaSolverException):
    """
    API: Error that captcha cannot be solved
    """

    pass


class APICaptchaNoSlotAvailableException(CaptchaSolverException):
    """
    API: Error that captcha has no slot available to be solved
    """


class APICaptchaWrongCaptchaID(CaptchaSolverException):
    """
    API: Error that captcha has wrong ID
    """


class UICaptchaNotSolved(CaptchaSolverException):
    """
    UI: Cannot find xpath that indicates solved captcha
    """

    pass


class ImageCaptchaNotSolved(CaptchaSolverException):
    """
    UI: Cannot find image source for solve captcha
    """

    pass


class ParamsException(CaptchaSolverException):
    """
    Some params are missing for captcha resolving
    """

    pass


class LowBalanceException(CaptchaSolverException):
    """
    API: Tool balance is low
    """

    pass


class FrameException(CaptchaSolverException):
    """
    UI: Captcha is probably inside iframe
    """

    pass


class ServiceProviderException(CaptchaSolverException):
    """
    Service provider is down
    """

    pass


class NoCaptchaException(CaptchaSolverException):
    """
    If there is no captcha on the page
    """

    pass


class NoTokenCaptchaException(CaptchaSolverException):
    """
    If there is no token to solve captcha on the page
    """

    pass
