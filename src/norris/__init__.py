from .instance import Instance
from .project import Project
from .activity_flow_stages import Store, Station
from .activity_flow import ActivityFlow
from .activity import Activity
from .issue import Issue
from .issue_lifecycle import IssueLifecycle
from .issue_lifecycle_record import IssueLifecycleRecord
from .issue_transitions import IssueTransitions
from .issue_transitions_record import IssueTransitionsRecord
from .utilities import Utilities
#from .flow import Flow

from jira.client import JIRA

def configure_and_connect( **kwargs ):

    url = kwargs['url']
    user = kwargs['user']
    passwd = kwargs['passwd']
    
    return Instance( JIRA( basic_auth = ( user, passwd ),
                           options = { 'server': url } ) )
