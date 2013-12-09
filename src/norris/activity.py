import norris

class Activity( object ):
    
    def __init__( self, jira_instance, jira_project, jira_issue_type ):
        
        self._jira_instance = jira_instance
        self._jira_project = jira_project
        self._jira_issue_type = jira_issue_type

        self._project = self._jira_project.key
        self._name = self._jira_issue_type.name
        
        # grab issues in chunks to avoid problems with jira server global maxResults settings
        self._issues = {}
        start = 0; chunk = 500
        while True:
            results = self._jira_instance.search_issues(
                '( project = "%s" ) AND ( issuetype = "%s" )' % ( self._jira_project.key, self._jira_issue_type.name ),
                startAt = start, maxResults = chunk, expand = 'changelog'
            )
            for jira_issue in results:
                self._issues[jira_issue.key] = norris.Issue( jira_issue )
            if len( results ) == 0:
                break
            else:
                start += chunk
                continue
             
        self._flow = norris.ActivityFlow( self._issues.values(), self._name )

        return None
    
    def __str__( self ):
        return '%s %s Activity (%d issues)' % ( self._project, self._name, len( self._issues ) )

    @property
    def project( self ):
        return self._project

    @property
    def name( self ):
        return self._name

    @property
    def issues( self ):
        return self._issues

    @property
    def flow( self ):
        return self._flow

    def issue( self, key = None ):
        
        return self._issues[key]
