import norris

class Issue( object ):

    def __init__( self, jira_issue, config ):

        self._name = norris.Utilities.to_unicode( jira_issue.key )
        self._type = norris.Utilities.to_unicode( jira_issue.fields.issuetype.name )
        self._summary = norris.Utilities.to_unicode( jira_issue.fields.summary )
        self._status = norris.Utilities.to_unicode( jira_issue.fields.status.name )
        
        self._people = norris.IssuePeople( jira_issue, config )
        self._lifecycle = norris.IssueLifecycle( jira_issue )
        self._transitions = norris.IssueTransitions( jira_issue )

        return None

    def __str__( self ):
        
        return '%s %s, "%s" [ %s ]' % ( self._type.encode( 'utf-8' ),
                                        self._name.encode( 'utf-8' ),
                                        self._summary.encode( 'utf-8' ),
                                        self._status.encode( 'utf-8' ) )
    
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
    def people( self ):
        return self._people
    
    @property
    def lifecycle( self ):
        return self._lifecycle
    
    @property
    def transitions( self ):
        return self._transitions
