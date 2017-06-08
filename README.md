# nova_api
Module that implements a class with methods to interact with nova API via http requests.

## Changelog

## Installation
```
pip install git+https://github.com/chaps/nova_api
```
or clone and install
```
git clone https://github.com/chaps/nova_api
cd nova_api
python setup.py install
```
## Usage
```
from nova_api.api import NovaAPI
nova = NovaAPI("yer_username","yer_password")
# Handles all the login hastle
nova.login()
# Sets all relevant info from the service to the respective attribute
nova.build_info()
# Access your profile info:
nova.profile
# Access the system data
nova.project_types
nova.project_statuses
nova.activity_types
nova.users
nova.accounts
nova.projects
nova.technologies
nova.employee_types
# Your current activities and projects
nova.my_activities
nova.my_projects

# Add a new activity
novaapi.post_activity(6,14,comments="test_api")
# Access the new activity details
new_activity = nova.post_activity_response.json()
# Edit the previous activity:
#  Options available to edit as named arguments are:
#   comments, value (hours) and ticket 
new_comments = "testing_changes"
nova.edit_activity(new_activity["activityId"], comments=new_comments)
# Check your changes
nova.edit_activity_response.json()["comments"] == new_comments
# Delete the previous activity
nova.delete_activity(new_activity["activityId"])
nova.delete_activity_response.json()
```

## Testing


First you will need a pair of valid credentials for testing 
against the service.
- Clone the repo
- Locate at the root of the repo.

Create a file named _credentials.py under the test package 
in it you will need to define your username and password.
```
# _credentials.py
username = "yerusername"
password = "yerpassword"
```
Run pytest for testing.
```
pytest
```



