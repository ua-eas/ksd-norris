import norris

class Project( object ):

    def __init__( self, jira_instance, jira_project ):

        self._jira_instance = jira_instance
        self._jira_project = jira_project

        self._name = self._jira_project.name
        self._key = self._jira_project.key

        return None

    def __str__( self ):
        return '%s Project (%s)' % ( self._name, self._key )

    @property
    def name( self ):
        return self._name
    
    @property
    def key( self ):
        return self._key

    def activity( self, key = None ):
        
        jira_issue_type = next( t for t in self._jira_project.issueTypes if t.name == key )
        
        return norris.Activity( self._jira_instance, self._jira_project, jira_issue_type )
