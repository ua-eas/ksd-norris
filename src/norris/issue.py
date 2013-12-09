import norris

class Issue( object ):

    def __init__( self, jira_issue ):

        self._jira_issue = jira_issue

        self._name = self._jira_issue.key
        self._type = self._jira_issue.fields.issuetype.name
        self._summary = self._jira_issue.fields.summary
        self._status = self._jira_issue.fields.status.name
        
        self._lifecycle = norris.IssueLifecycle( self._jira_issue )
        self._transitions = norris.IssueTransitions( self._jira_issue )

        return None

    def __str__( self ):
        
        return '%s %s, "%s" [ %s ]' % ( self._type, self._name, self._summary, self._status )
    
    @property
    def name( self ):
        return self._name
    
    @property
    def type( self ):
        return self._type
    
    @property
    def summary( self ):
        return self._summary
    
    @property
    def status( self ):
        return self._status
    
    @property
    def lifecycle( self ):
        return self._lifecycle
    
    @property
    def transitions( self ):
        return self._transitions
