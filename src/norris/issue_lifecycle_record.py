import norris

class IssueLifecycleRecord( object ):
    
    def __init__( self, status, start_date, end_date ):
        
        self._status = status
        self._start_date = start_date
        self._end_date = end_date
        
        return None
    
    def __str__( self ):
        
        return ( '%s: %s - %s (%.2f days)' % ( self._status,
                                               self._start_date,
                                               self._end_date,
                                               norris.Utilities.timedelta_to_days( self._end_date - self._start_date ) ) )

    @property
    def status( self ):
        return self._status
    
    @property
    def start_date( self ):
        return self._start_date
    
    @property
    def end_date( self ):
        return self._end_date
    
    