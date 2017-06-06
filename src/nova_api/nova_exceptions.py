
class LoginFailed(Exception):
    """ Exception raised based on the result endpoint of the login request."""
    pass


class GetTokenEndpointError(Exception):
    """Exception raised when trying to obtain the access token from an endpoint which doesn't match/startswith
    the following url: http://nova.itexico.com/#/authorized/
    """
    pass


class NotEnoughArguments(Exception):
    """Exception raised when trying to call a method with less optional arguments than needed.
    """
    pass
