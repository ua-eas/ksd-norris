import norris

class IssuePeopleRecord( object ):
    
    def __init__( self, role, name ):
        
        self._role = role.lower()
        self._name = name.lower()
        
        return None
    
    def __str__( self ):
        
        return ( '%s: %s' % ( self._role, self._name ) )

    @property
    def role( self ):
        return self._role
    
    @property
    def name( self ):
        return self._name
    
