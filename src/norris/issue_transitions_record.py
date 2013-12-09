import norris

class IssueTransitionsRecord( object ):
    
    def __init__( self, start_status, end_status, transition_date ):
        
        self._start_status = start_status
        self._end_status = end_status
        self._transition_date = transition_date
        
        return None
    
    def __str__( self ):
        
        return ( '%s -> %s (%s)' % ( self._start_status,
                                     self._end_status,
                                     self._transition_date ) )

    @property
    def start_status( self ):
        return self._start_status
    
    @property
    def end_status( self ):
        return self._end_status
    
    @property
    def transition_date( self ):
        return self._transition_date
