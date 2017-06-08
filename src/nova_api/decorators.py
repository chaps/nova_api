from functools import wraps
from nova_exceptions import AuthorizationHeaderNotSet, AttributeIsNotResponseType
from requests.models import Response


def set_to_json_response(attr_to_set, response_attr_name):
    """
    Receives two strings that will be used in the returned decorator
    for getting and setting the specified attributes.
    :param attr_to_set: string, the attribute name that will have it's value set.
    :param response_attr_name: string, the attribute name that returns the json parsed response
    :return: function that acts as a decorator
    """

    def set_to_json_outer_decorator(f):
        @wraps(f)
        def set_to_json_inner_wrapper(instance):
            """
            The actual decorator that can access the first decorator's received arguments.
            Assigns the json response from the response attribute to the attribute to set.
            :param instance: a class (NovaAPI) instance.
            :return: result of the received function.
            """
            setattr(instance, attr_to_set, getattr(instance, response_attr_name).json())
            return f(instance)
        return set_to_json_inner_wrapper
    return set_to_json_outer_decorator
    pass


def has_authentication_header(func):
    """
    Decorator that will check if the instance of the given function,
    contains an HTTP Authorization header before calling the given function
    :param func: the function to wrap.
    :return: function The decorated function.
    """
    @wraps(func)
    def has_auth_header_wrapper(instance, *args, **kwargs):
        """
        Checks if the instance of the given function contains a
        HTTP Authorization header before calling the given function if not
        raises an AuthorizationHeaderNotSet Exception.
        :param instance: the given function instance. (NovaAPI instance)
        :param args: extra arguments
        :param kwargs: extra keyword arguments.
        :raises AuthorizationHeaderNotSet:
        :return: The result of the given function.
        """
        if "Authorization" not in instance.ses.headers:
            raise AuthorizationHeaderNotSet()
        return func(instance, *args, **kwargs)
    return has_auth_header_wrapper


def check_attr_response_type(attribute_name):
    """
    Receives an attribute name to reference the
    :param attribute_name:
    :return: function, the decorator.
    """
    def outer_check_attr_response_wrapper(func, *args, **kwargs):
        """
        decorates the received function with the function defined.
        :param func:
        :param args:
        :param kwargs:
        :return: function, the decorated function
        """
        @wraps(func)
        def inner_check_attr_response_wrapper(instance, *args, **kwargs):
            """
            Gets the attribute from the received function's instance
            using the first function's attribute_name parameter.
            Checks if the obtained attribute inherits from requests.models.Response.
            :param instance: the received function instance.
            :param args:
            :param kwargs:
            :raise AttributeIsNotResponseType:
            :return: the result of the received function
            """
            attr = getattr(instance, attribute_name)
            if not isinstance(attr, Response):
                raise AttributeIsNotResponseType(attribute_name, type(attr))
            return func(instance, *args, **kwargs)
        return inner_check_attr_response_wrapper
    return outer_check_attr_response_wrapper
    pass
