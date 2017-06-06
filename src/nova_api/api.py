import requests
import uuid
import re
import datetime
from nova_exceptions import LoginFailed, GetTokenEndpointError, NotEnoughArguments


class NovaAPI(object):
    """Class with methods to interact with nova API via http requests.
    """
    client_id = "56cccded013d35a3949308d7"
    acccess_token_pattern = re.compile("^.*access_token=(\w+)&.*")
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
        self.activity_types_response = None
        self.activities_response = None
        self.projects_response = None
        self.project_assignments_response = None
        self.technologies_response = None
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
        if not self.authorization_url in self.login_response.url:
            raise LoginFailed()
        pass

    def go_authorized(self):
        """

        :return:
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

    def get_auth_token(self):
        """
        Sends the http request to obtain the endpoint in which the access token should be
         as a get parameter.
        Sets the response in the get_token_response attribute.
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

    def parse_token_response(self):
        """
        Obtains and sets the access_token from the get_token_response attribute endpoint (url)
        Sets the access_token attribute to the obtained token.
        Sets the Authorization HTTP header for bearer/token authentication in further requests.
        :return: None
        """
        url_prefix = self.authorized_url
        if not self.get_token_response.url.startswith(url_prefix):
            raise GetTokenEndpointError()
            pass
        match = self.acccess_token_pattern.match(self.get_token_response.url)
        self.access_token = match.groups()[0]
        self.ses.headers["Authorization"] = "bearer " + self.access_token
        pass

    def login(self):
        """
        Calls all methods in order to login with the given credentials.
        :return:
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
        :return:
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

    def get_profile(self):
        """
        Sends the http request to get the logged in user's profile.
        Stores the response in the profile_response attribute.
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

    def set_profile(self):
        """
        Sets the profile attribute to the JSON response from the profile_response
        attribute.
        :return: None
        """
        self.profile = self.profile_response.json()
        pass

    def set_profile_id(self):
        """
        Sets the profile id attribute based on the value from the id key
        in the response obtained with the get_profile method.
        :return: None
        """
        self.profile_id = self.profile_response.json()["id"]
        pass

    def get_users(self):
        """
        Sends the http request to get a list of users.
        Stores the response in the users_response attribute.
        :return: None
        """
        self.users_response = self.ses.get(self.users_url)
        pass

    def set_users(self):
        """
        Sets the users attribute to the json array parsed from the
         users_response attribute.
        :return: None
        """
        self.users = self.users_response.json()
        pass

    def get_accounts(self):
        """
        Sends the http request to get a list of accounts.
        Stores the response in the accounts_response attribute.
        :return: None
        """
        self.accounts_response = self.ses.get(self.accounts_url)
        pass

    def set_accounts(self):
        """
        Sets the accounts attribute to the json array parsed from the
         users_response attribute.
        :return: None
        """
        self.accounts = self.users_response.json()
        pass

    def get_projects(self):
        """"""
        self.projects_response = self.ses.get(self.projects_url)
        pass

    def set_projects(self):
        """"""
        self.projects = self.projects_response.json()
        pass

    def get_project_types(self):
        """
        Sends the http request to get a list of project types.
        Stores the response in the accounts_response attribute.
        :return: None
        """
        self.project_types_response = self.ses.get(self.project_types_url)
        pass

    def set_project_types(self):
        """
        Sets the project_types attribute to the json array parsed from the
         project_types_response attribute.
        :return: None
        """
        self.project_types = self.project_types_response.json()
        pass

    def get_project_status(self):
        """
        Sends the http request to get a list of project status.
        Stores the response in the project_statuses_response attribute.
        :return: None
        """
        self.project_statuses_response = self.ses.get(self.project_statuses_url)
        pass

    def set_project_statuses(self):
        """
        Sets the project_statuses to the json array parsed from the
         project_statuses_response attribute.
        :return: None
        """
        self.project_statuses = self.project_statuses_response.json()
        pass

    def get_technologies(self):
        """
        Sends the http request to get a list of technologies.
        Stores the response in the technologies_response attribute.
        :return: None
        """
        self.technologies_response = self.ses.get(self.technologies_url)
        pass

    def set_technologies(self):
        """
        Sets the technologies attribute to the json array parsed from the
         technologies_response attribute.
        :return: None
        """
        self.technologies = self.technologies_response.json()
        pass

    def get_activity_types(self):
        """
        Sends the http request to get a list of activity types.
        Stores the response in the activity_types_response attribute.
        :return: None
        """
        self.activity_types_response = self.ses.get(self.activity_types_url)
        pass

    def set_activity_types(self):
        """
        Sets the activity_types attribute to the json array parsed from the
         activity_types_response attribute.
        :return: None
        """
        self.activity_types = self.activity_types_response.json()
        pass

    def get_org_structures(self):
        """
        Sends the http request to get a list of activity types.
        Stores the response in the activity_types_response attribute.
        :return: None
        """
        self.org_structures_response = self.ses.get(self.org_structures_url)
        pass

    def set_org_structures(self):
        """
        :return: None
        """
        self.org_structures = self.org_structures_response.json()
        pass

    def get_employee_types(self):
        """

        :return: None
        """
        self.employee_types = self.ses.get(self.employee_types_url)
        pass

    def set_employee_types(self):
        """
        Sends the http request to get a list of employee_types assigned to employees.
        Sets the result to employee_types attribute.
        :return: None
        """
        self.employee_types = self.employee_types.json()
        pass

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
            params["filter"] = params["filter"] % ( employee_id,)
        self.project_assignments_response = self.ses.get(
            self.project_assignments_url,
            params=params
        )
        pass

    ###
    # CRUD for activities.
    ###

    def get_activities(self, params=None, userid=None):
        """
        Sends the http request to get a list of activites assigned to employees.
        Sets the result to activities_response attribute.
        :param params: dictionary
        :param userid: integer
        :return: None
        """
        if not params:
            params = {"filter": '{"where":{"employeeId": %d}}'}
        if not userid:
            userid = self.profile_id
        if "filter" in params:
            params["filter"] = params["filter"] % (userid,)
        self.activities_response = self.ses.get(
            self.activities_url,
            params=params
        )

    def delete_activity(self, activity_id):
        """
        Sends a request to delete an activity
        :param activity_id:
        :return: None
        """
        self.delete_activity_response = self.ses.delete(
            "/".join([self.activities_url, str(activity_id)])
        )
        # Returns JSON with "count" key set to 1
        pass

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

