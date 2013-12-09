import norris

class Instance( object ):

    def __init__( self, jira_instance ):
        
        self._jira_instance = jira_instance

        self._title = self._jira_instance.server_info()['serverTitle']
        self._version = self._jira_instance.server_info()['version']
        
        return None
        
    def __str__( self ):
        return '%s Instance (Jira v%s)' % ( self._title, self._version )
    
    @property
    def title( self ):
        return self._title
    
    @property
    def version( self ):
        return self._version
    
    def project( self, key = None ):
        
        jira_project = self._jira_instance.project( key )
        
        return norris.Project( self._jira_instance, jira_project )
