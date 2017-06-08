import pytest
from nova_api.api import NovaAPI
from nova_api.nova_exceptions import LoginFailed
from _credentials import username, password
from functools import wraps


def asserts_status_code(apiinstance, response_attribute_str, status_code):
    """
    Returns a decorated function which calls the received function and asserts
    to check the status_code against the expected status_code.
    :param apiinstance: NovaAPI instance
    :param response_attribute_str: string, attribute name expecting to be a requests.models.Response instance.
    :param status_code: integer, Status code of the instance's obtained attribute.
    :return: function, The decorated function.
    """
    def outer_asserts_status_code_wrapper(function):
        @wraps(function)
        def inner_asserts_status_code_wrapper(instance, *args, **kwargs):
            function(instance)
            assert getattr(apiinstance, response_attribute_str).status_code == status_code
        return inner_asserts_status_code_wrapper
    return outer_asserts_status_code_wrapper


def asserts_json_response(apiinstance, response_attribute_str, arg_type):
    """
    Returns a decorated function which calls the received function and asserts
    to check if the response's body returns a json object of type equal to the expected arg_type.
    :param apiinstance: NovaAPI instance
    :param response_attribute_str: string, attribute name expecting to be a requests.models.Response instance.
    :param status_code: integer, Status code of the instance's obtained attribute.
    :return: function, The decorated function.
    """
    def outer_asserts_status_code_wrapper(function):
        @wraps(function)
        def inner_asserts_status_code_wrapper(instance, *args, **kwargs):
            function(instance)
            assert isinstance(getattr(apiinstance, response_attribute_str).json(), arg_type)
        return inner_asserts_status_code_wrapper
    return outer_asserts_status_code_wrapper


nova = NovaAPI(username, password)
nova.post_login()
nova.get_auth_token()
nova.parse_token_response()


class TestNovaAPI(object):

    def test_wrong_login(self):
        """
        Asserts that trying to login with probably wrong credentials,
        will raise a LoginFailed exception.
        :return: None
        """
        print "test_wrong_login"
        nova = NovaAPI("userihopeneverexists", "password")
        with pytest.raises(LoginFailed):
            nova.login()
            pass
        pass

    @asserts_status_code(nova, "login_response", 200)
    def test_post_login(self):
        """
        Asserts that the login_response endpoint (url) matches the
        expected one for a successful login.
        :return: None
        """
        assert NovaAPI.authorization_url in nova.login_response.url
        pass

    @asserts_status_code(nova, "get_token_response", 200)
    def test_get_auth_token(self):
        """
        Asserts getting a 200 status code from the server after sending a POST
        request and being redirected to the endpoint which contains the authtoken
        in a GET param.
        :return: None
        """
        assert nova.get_token_response.url.startswith(NovaAPI.authorized_url)
        pass

    def test_parse_token_response(self):
        """
        Asserts the api instance session contains an Authorization header set
        :return: None
        """
        assert isinstance(nova.access_token, unicode)
        assert len(nova.access_token) == 128
        assert "Authorization" in nova.ses.headers
        assert nova.ses.headers["Authorization"].startswith("bearer ")
        pass

    @asserts_status_code(nova, "profile_response", 200)
    @asserts_json_response(nova, "profile_response", dict)
    def test_get_profile(self):
        """
        Asserts a successful json response of type dict.
        :return: None
        """
        nova.get_profile()
        assert isinstance(nova.profile_response.json(), dict)
        self._test_set_profile()
        pass

    @staticmethod
    def _test_set_profile():
        """
        Asserts the profile attribute contains the expected profile.
        :return:
        """
        nova.set_profile()
        assert "email" in nova.profile
        assert nova.profile["email"] == username
        assert isinstance(nova.profile, dict)
        pass

    @asserts_status_code(nova, "users_response", 200)
    @asserts_json_response(nova, "users_response", list)
    def test_get_users(self):
        nova.get_users()
        self._test_set_users()
        pass

    @staticmethod
    def _test_set_users():
        nova.set_users()
        assert isinstance(nova.users, list)
        pass

    @asserts_status_code(nova, "accounts_response", 200)
    @asserts_json_response(nova, "accounts_response", list)
    def test_get_accounts(self):
        nova.get_accounts()
        self._test_set_accounts()
        pass

    @staticmethod
    def _test_set_accounts():
        nova.set_accounts()
        assert isinstance(nova.accounts, list)
        pass

    @asserts_status_code(nova, "projects_response", 200)
    @asserts_json_response(nova, "projects_response", list)
    def test_get_projects(self):
        nova.get_projects()
        self._test_set_projects()
        pass

    @staticmethod
    def _test_set_projects():
        nova.set_projects()
        assert isinstance(nova.projects, list)
        pass

    @asserts_status_code(nova, "projects_response", 200)
    @asserts_json_response(nova, "projects_response", list)
    def test_get_projects_types(self):
        nova.get_project_types()
        self._test_set_projects_types()
        pass

    @staticmethod
    def _test_set_projects_types():
        nova.set_project_types()
        assert isinstance(nova.project_types, list)
        pass

    @asserts_status_code(nova, "project_statuses_response", 200)
    @asserts_json_response(nova, "project_statuses_response", list)
    def test_get_project_status(self):
        nova.get_project_status()
        self._test_set_projects_status()
        pass

    @staticmethod
    def _test_set_projects_status():
        nova.set_project_statuses()
        assert isinstance(nova.project_statuses, list)
        pass

    @asserts_status_code(nova, "technologies_response", 200)
    @asserts_json_response(nova, "technologies_response", list)
    def test_get_technologies(self):
        nova.get_technologies()
        self._test_set_technologies()
        pass

    @staticmethod
    def _test_set_technologies():
        nova.set_technologies()
        assert isinstance(nova.technologies, list)
        pass

    @asserts_status_code(nova, "activity_types_response", 200)
    @asserts_json_response(nova, "activity_types_response", list)
    def test_get_activity_types(self):
        nova.get_activity_types()
        self._test_set_activity_types()
        pass

    @staticmethod
    def _test_set_activity_types():
        nova.set_activity_types()
        assert isinstance(nova.activity_types, list)
        pass

    @asserts_status_code(nova, "org_structures_response", 200)
    @asserts_json_response(nova, "org_structures_response", list)
    def test_get_org_structures(self):
        nova.get_org_structures()
        self._test_set_org_structures()
        pass

    @staticmethod
    def _test_set_org_structures():
        nova.set_org_structures()
        assert isinstance(nova.org_structures, list)
        pass

    @asserts_status_code(nova, "employee_types_response", 200)
    @asserts_json_response(nova, "employee_types_response", list)
    def test_get_employee_types(self):
        nova.get_employee_types()
        self._test_set_employee_types()
        pass

    @staticmethod
    def _test_set_employee_types():
        nova.set_employee_types()
        assert isinstance(nova.employee_types, list)
        pass

    def test_new_session_existing_token(self):
        """
        Asserts that an instance can access endpoints that require an Authorization token
        by just setting the Authorization header with a valid token in a clean instance session's attribute.
        :return: None
        """
        tmp_api = NovaAPI()
        tmp_api.ses.headers["Authorization"] = "bearer " + nova.access_token
        tmp_api.get_profile()
        tmp_api.set_profile()
        assert tmp_api.profile["email"] == username
        pass

    pass


