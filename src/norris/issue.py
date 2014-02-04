import norris

class Issue( object ):
    '''
    The Issue class represents a translator that converts extracted JIRA issues
    into a non-JIRA-specific neutral format that can then be manipulated further
    down the CLI pipeline.  Details of the field mapping done during the conversion
    are pulled from the Norris configuration file.  We also convert JIRA change
    logs into two easier-to-handle formats (issue lifecycle and transitions).
    '''

    def __init__( self, jira_issue, config ):

        self._name = norris.Utilities.to_unicode( jira_issue.key ).lower()
        self._type = norris.Utilities.to_unicode( jira_issue.fields.issuetype.name ).lower()
        self._summary = norris.Utilities.to_unicode( jira_issue.fields.summary ).lower()

        r = ( norris.Utilities.to_unicode( jira_issue.fields.status.name ) ).split( ' - ' )
        if len( r ) == 2:
            self._node = r[0].lower()
            self._state = r[1].lower()
        elif len( r ) == 1:
            self._node = r[0].lower()
            self._state = None
        else:
            self._node = '(unknown)'
            self._state = '(unknown)'
        
        self._severity = eval( 'int( float( jira_issue.fields.%s ) )' % ( config['jira']['fieldmap']['severity'] ) )
        self._investment = eval( 'int( float( jira_issue.fields.%s ) )' % ( config['jira']['fieldmap']['investment'] ) )
        
        self._people = norris.IssuePeople( jira_issue, config )
        self._lifecycle = norris.IssueLifecycle( jira_issue )
        self._transitions = norris.IssueTransitions( jira_issue )

        return None

    def __str__( self ):
        
        return '%s %s, "%s" [ severity = %s, investment = %s, node = %s, state = %s ]' % ( self.type.title().encode( 'utf-8' ),
                                                                                           self.name.upper().encode( 'utf-8' ),
                                                                                           self.summary.encode( 'utf-8' ),
                                                                                           str( self.severity ).encode( 'utf-8' ),
                                                                                           str( self.investment ).encode( 'utf-8' ),
                                                                                           self.node.encode( 'utf-8' ),
                                                                                           ( '(n/a)' if self.state == None else str( self.state ) ).encode( 'utf-8' ) )
    
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
    def node( self ):
        return self._node
    
    @property
    def state( self ):
        return self._state
    
    @property
    def severity( self ):
        return self._severity
    
    @property
    def investment( self ):
        return self._investment

    @property
    def people( self ):
        return self._people
    
    @property
    def lifecycle( self ):
        return self._lifecycle
    
    @property
    def transitions( self ):
        return self._transitions
