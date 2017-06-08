import requests
import uuid
import re
import datetime
from nova_exceptions import LoginFailed, GetTokenEndpointError, NotEnoughArguments
from decorators import set_to_json_response, has_authentication_header, check_attr_response_type


class NovaAPI(object):
    """Class with methods to interact with nova API via http requests.
    """
    # noinspection SpellCheckingInspection
    client_id = "56cccded013d35a3949308d7"
    access_token_pattern = re.compile("^.*access_token=(\w+)&.*")
    authorized_url = "http://nova.itexico.com/#/authorized/"
    login_url = "http://nova.cloudapp.net/login"
    authorization_url = "http://nova.cloudapp.net/authorization"
    accounts_url = "http://nova.cloudapp.net/api/Accounts"
    profile_url = "http://nova.cloudapp.net/api/employees/profile"
    projects_url = "http://nova-api.itexico.com/api/Projects"
    project_types_url = "http://nova.cloudapp.net/api/ProjectTypes"
    project_statuses_url = "http://nova.cloudapp.net/api/ProjectStatuses"
    project_assignments_url = "http://nova.cloudapp.net/api/ProjectAssignments"
    activity_types_url = "http://nova.cloudapp.net/api/activityTypes"
    account_statuses_url = "http://nova.cloudapp.net/api/AccountStatuses"
    activities_url = "http://nova.cloudapp.net/api/Activities"
    users_url = "http://nova.cloudapp.net/api/employees"
    logout_url = "http://nova.cloudapp.net/api/employees/logout"
    employee_types_url = "http://nova.cloudapp.net/api/employeeTypes"
    org_structures_url = "http://nova-api.itexico.com/api/OrgStructures"
    technologies_url = "http://nova-api.itexico.com/api/Technologies"
    # activity log

    def __init__(self, username="", password=""):
        """ Initializes attributes.
        """
        self.username = username
        self.password = password
        self.ses = requests.session()
        self.ses.headers["User-Agent"] = "Go-http-client/1.1"
        self.access_token = None
        self.profile_id = None
        self.state = str(uuid.uuid4())
        # Attributes:
        self.profile = None
        self.project_types = None
        self.project_statuses = None
        self.activity_types = None
        self.users = None
        self.accounts = None
        self.projects = None
        self.technologies = None
        self.employee_types = None
        self.org_structures = None
        # Account specific set on build_info
        self.my_activities = None
        self.my_projects = None
        # Login Process Responses
        self.login_response = None
        self.authorized_response = None
        self.get_token_response = None
        # Responses
        self.profile_response = None
        self.users_response = None
        self.accounts_response = None
        self.project_types_response = None
        self.project_statuses_response = None
        self.employee_types_response = None
        self.activity_types_response = None
        self.activities_response = None
        self.projects_response = None
        self.project_assignments_response = None
        self.technologies_response = None
        self.org_structures_response = None
        # Activity CUD responses.
        self.delete_activity_response = None
        self.post_activity_response = None
        self.edit_activity_response = None
        pass

    ###
    # Login Process.
    ###

    def post_login(self):
        """Sends the http request to login
        Stores the response in the login_response attribute.
        :return: None
        """
        data = {
            "username": self.username,
            "password": self.password
        }
        params = {
            "redirect_uri": self.authorized_url,
            "response_type": "token",
            "state": self.state,
            "client_id": self.client_id,
            "backUrl": "/authorization"

        }
        self.login_response = self.ses.post(
            self.login_url,
            data=data,
            params=params
        )
        if self.authorization_url not in self.login_response.url:
            raise LoginFailed()
        pass

    def go_authorized(self):
        """Makes an http request to be redirected to the authorization endpoint.
        Assigns the response to the authorized_response attribute.
        :return: None
        """
        params = {
            "response_type": "token",
            "state": self.state,
            "redirect_uri": self.authorized_url + "&client_id=" + self.client_id,
            "client_id": self.client_id,
        }
        self.authorized_response = self.ses.get(
            self.authorization_url,
            params=params
        )
        pass

    @check_attr_response_type("login_response")
    def get_auth_token(self):
        """
        Sends the http request to obtain the endpoint in which the access token should be
         as a get parameter.
        Assigns the response to the get_token_response attribute.
        :return: None
        """
        params = {
            "client_id": self.client_id,
            "response_type": "token",
            "state": self.state,
            "redirect_uri": self.authorized_url,
            "backUrl": "/authorization"
        }
        data = {"decision": 1}
        self.get_token_response = self.ses.post(
            self.authorization_url,
            params=params,
            data=data
        )
        pass

    @check_attr_response_type("get_token_response")
    def parse_token_response(self):
        """
        Obtains and sets the access_token from the get_token_response attribute endpoint (url)
        Assigns the obtained token to the access_token attribute.
        Sets the Authorization HTTP header for bearer/token authentication in further requests.
        :return: None
        """
        url_prefix = self.authorized_url
        if not self.get_token_response.url.startswith(url_prefix):
            raise GetTokenEndpointError()
            pass
        match = self.access_token_pattern.match(self.get_token_response.url)
        self.access_token = match.groups()[0]
        self.ses.headers["Authorization"] = "bearer " + self.access_token
        pass

    def login(self):
        """
        Calls all methods in order to login with the given credentials.
        :return: None
        """
        self.post_login()
        self.go_authorized()
        self.get_auth_token()
        self.parse_token_response()
        self.get_profile()
        self.set_profile()
        self.set_profile_id()
        pass

    def build_info(self):
        """
        Make the calls to set all
        attributes with the service's relevant information.
        :return: None
        """
        self.get_project_types()
        self.set_project_types()
        self.get_project_status()
        self.set_project_statuses()
        self.get_activity_types()
        self.set_activity_types()
        self.get_users()
        self.set_users()
        self.get_accounts()
        self.set_accounts()
        self.get_projects()
        self.set_projects()
        self.get_technologies()
        self.set_technologies()
        self.get_employee_types()
        self.set_employee_types()
        self.get_activities()
        self.my_activities = self.activities_response.json()
        self.get_project_assignments()
        self.my_projects = self.project_assignments_response.json()
        pass

    @has_authentication_header
    def get_profile(self):
        """
        Sends the http request to get the logged in user's profile.
        Assigns the response to the profile_response attribute.
        :return: None
        """
        params = {
            "filter": '{"include":["contract"]}'
        }
        self.profile_response = self.ses.get(
            self.profile_url,
            params=params
        )
        pass

    @check_attr_response_type("profile_response")
    @set_to_json_response("profile", "profile_response")
    def set_profile(self):
        """
        Assigns the JSON response from the profile_response to the profile attribute.
        :return: None
        """
        pass

    @check_attr_response_type("profile_response")
    def set_profile_id(self):
        """
        Sets the profile id attribute based on the value from the id key
        in the response obtained in the get_profile method.
        :return: None
        """
        self.profile_id = self.profile_response.json()["id"]
        pass

    @has_authentication_header
    def get_users(self):
        """
        Sends the http request to get a list of users.
        Assigns the response to the users_response attribute.
        :return: None
        """
        self.users_response = self.ses.get(self.users_url)
        pass

    @check_attr_response_type("users_response")
    @set_to_json_response("users", "users_response")
    def set_users(self):
        """
        Assigns the json array parsed from the
         users_response attribute to the users attribute.
        :return: None
        """
        self.users = self.users_response.json()
        pass

    @has_authentication_header
    def get_accounts(self):
        """
        Sends the http request to get a list of accounts.
        Assigns the response to the accounts_response attribute.
        :return: None
        """
        self.accounts_response = self.ses.get(self.accounts_url)
        pass

    @check_attr_response_type("accounts_response")
    @set_to_json_response("accounts", "accounts_response")
    def set_accounts(self):
        """
        Assigns the json array parsed from the
         accounts_response attribute to the accounts attribute.
        :return: None
        """
        pass

    @has_authentication_header
    def get_projects(self):
        """
        Sends the http request to get a list of existing projects.
        Assigns the response to the projects_response attribute.
        :return: None
        """
        self.projects_response = self.ses.get(self.projects_url)
        pass

    @check_attr_response_type("projects_response")
    @set_to_json_response("projects", "projects_response")
    def set_projects(self):
        """
        Assigns the json parsed from the
         projects_response attribute to the projects attribute.
        :return: None
        """
        pass

    @has_authentication_header
    def get_project_types(self):
        """
        Sends the http request to get a list of project types.
        Assigns the response to the project_types_response attribute.
        :return: None
        """
        self.project_types_response = self.ses.get(self.project_types_url)
        pass

    @check_attr_response_type("project_types_response")
    @set_to_json_response("project_types", "project_types_response")
    def set_project_types(self):
        """
        Assigns the json array parsed from the
         project_types_response attribute to the project_types attribute.
        :return: None
        """
        pass

    @has_authentication_header
    def get_project_status(self):
        """
        Sends the http request to get a list of project status.
        Stores the response in the project_statuses_response attribute.
        :return: None
        """
        self.project_statuses_response = self.ses.get(self.project_statuses_url)
        pass

    @check_attr_response_type("project_statuses_response")
    @set_to_json_response("project_statuses", "project_statuses_response")
    def set_project_statuses(self):
        """
        Sets the project_statuses to the json array parsed from the
         project_statuses_response attribute.
        :return: None
        """
        pass

    @has_authentication_header
    def get_technologies(self):
        """
        Sends the http request to get a list of technologies.
        Stores the response in the technologies_response attribute.
        :return: None
        """
        self.technologies_response = self.ses.get(self.technologies_url)
        pass

    @check_attr_response_type("technologies_response")
    @set_to_json_response("technologies", "technologies_response")
    def set_technologies(self):
        """
        Sets the technologies attribute to the json array parsed from the
         technologies_response attribute.
        :return: None
        """
        pass

    @has_authentication_header
    def get_activity_types(self):
        """
        Sends the http request to get a list of activity types.
        Assigns the response to the activity_types_response attribute.
        :return: None
        """
        self.activity_types_response = self.ses.get(self.activity_types_url)
        pass

    @check_attr_response_type("activity_types_response")
    @set_to_json_response("activity_types", "activity_types_response")
    def set_activity_types(self):
        """
        Assigns the json array parsed from the activity_types_response attribute
        to the activity_types attribute.
        :return: None
        """
        pass

    @has_authentication_header
    def get_org_structures(self):
        """
        Sends the http request to get a list of organization structures.
        Stores the response in the org_structures_response attribute.
        :return: None
        """
        self.org_structures_response = self.ses.get(self.org_structures_url)
        pass

    @check_attr_response_type("org_structures_response")
    @set_to_json_response("org_structures", "org_structures_response")
    def set_org_structures(self):
        """
        Assigns the json array parsed from the org_structures_response attribute
        to the org_structures attribute.
        :return: None
        """
        pass

    @has_authentication_header
    def get_employee_types(self):
        """
        Sends the http request to get a list of employee types.
        Stores the response in the employee_types_response attribute.
        :return: None
        """
        self.employee_types_response = self.ses.get(self.employee_types_url)
        pass

    @check_attr_response_type("employee_types_response")
    @set_to_json_response("employee_types", "employee_types_response")
    def set_employee_types(self):
        """
        Sets the employee_types attribute to the json array parsed from the
         employee_types_response attribute.
        :return: None
        """
        pass

    @has_authentication_header
    def get_project_assignments(self, params=None, employee_id=None):
        """
        Sends the http request to get project_assignments based on
        the get arguments sent with the request.
        Sets the response to the project_assignments_response attribute.
        :return: None
        """
        if not params:
            params = {
                "filter": '{"where":{"employeeId":"%d"},"include":{"project":"account"}}'
            }
        if not params:
            params = {"filter": '{"where":{"employeeId": %d}}'}
        if not employee_id:
            employee_id = self.profile["id"]
        if "filter" in params:
            params["filter"] %= (employee_id,)
        self.project_assignments_response = self.ses.get(
            self.project_assignments_url,
            params=params
        )
        pass

    ###
    # CRUD for activities.
    ###

    @has_authentication_header
    def get_activities(self, params=None, user_id=None):
        """
        Sends the http request to get a list of activites assigned to employees.
        Sets the result to activities_response attribute.
        :param params: dictionary
        :param user_id: integer
        :return: None
        """
        if not params:
            params = {"filter": '{"where":{"employeeId": %d}}'}
        if not user_id:
            user_id = self.profile_id
        if "filter" in params:
            params["filter"] %= (user_id,)
        self.activities_response = self.ses.get(
            self.activities_url,
            params=params
        )

    @has_authentication_header
    def delete_activity(self, activity_id):
        """
        Sends a request to delete an activity and assigns the response
        to delete_activity_response attribute.
        :param activity_id: The activity id
        :return: None
        """
        self.delete_activity_response = self.ses.delete(
            "/".join([self.activities_url, str(activity_id)])
        )
        # Returns JSON with "count" key set to 1
        pass

    # noinspection SpellCheckingInspection
    @has_authentication_header
    def post_activity(
        self,
        project_id,
        activitytype_id,
        date=None,
        employee_id=None,
        comments="",
        hours=1,
        ticket=""
    ):
        """
        Sends the http request to create a new activity with the given parameters.
        :return: None
        """
        if not date:
            date = datetime.datetime.today()
        if not employee_id:
            employee_id = self.profile_id
        data = {
            "activityDate": date.strftime("%Y-%m-%dT00:00:00Z"),
            # Hours worked for this activity.
            "value": hours,
            # Hours worked for this activity.
            "billablevalue": hours,
            "comments": comments,
            "task": ticket,
            "employeeId": employee_id,
            "stepId": 1,
            "typeId": activitytype_id,
            "projectId": project_id,
        }
        self.post_activity_response = self.ses.post(
            self.activities_url,
            data=data
        )
        pass

    @has_authentication_header
    def edit_activity(
            self,
            activity_id,
            value=None,
            comments=None,
            ticket=None
    ):
        """
        Sends the http request to edit an activity
        based on the parameters sent.
        :return: None
        """
        data = {"activityId": activity_id}
        if(
            not value and
            not comments and
            not ticket
        ):
            raise NotEnoughArguments()
            pass
        if value:
            data["value"] = value
            # noinspection SpellCheckingInspection
            data["billablevalue"] = value
        if comments:
            data["comments"] = comments
        if ticket:
            data["ticket"] = ticket
        self.edit_activity_response = self.ses.put(
            self.activities_url + "/" + str(activity_id),
            data=data
        )
        # Returns json with activityData
        pass

    pass
