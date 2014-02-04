import norris

class IssuePeople( object ):

    def __init__( self, jira_issue, config ):
        
        self._records = []
        
        # this piece needs to move out to the config file eventually -- too many magic strings
        itype = jira_issue.fields.issuetype.name
        if itype == 'Feature':
            roles = [ 'reporter', 'analyst', 'design_owner', 'code_owner',
                      'review_owner', 'test_owner', 'release_owner', 'assignee' ]
        else:
            roles = [ 'reporter', 'assignee' ]

        for role in roles:
            field = config['jira']['fieldmap'][role]
            if ( eval ( 'jira_issue.fields.%s' % ( field ) ) != None ):
                name = eval( 'norris.Utilities.to_unicode( jira_issue.fields.%s.displayName )' % ( field ) )
            else:
                name = '(none)'
            self._records.append( norris.IssuePeopleRecord( role.replace( '_', ' ' ).title(),
                                                            name ) )
        
        return None
    
    def __str__( self ):

        s = 'People:\n'
        for record in self._records:
            s += '  %s\n' % ( record )
        s = s[:-1]
            
        return s
    
    @property
    def records( self ):
        return self._records

