
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


class AuthorizationHeaderNotSet(Exception):
    """Exception raised when calling a method that requires the Authorization header set so the requested
    endpoint response can be successful.
    """
    pass


class AttributeIsNotResponseType(Exception):
    """
    Raised when isinstance fails when checking an
    attribute against requests.models.Response
    """
    pass
