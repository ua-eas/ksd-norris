import norris

class IssueTransitions( object ):

    def __init__( self, jira_issue ):
        
        self._records = []
        for event in jira_issue.changelog.histories:
            for delta in event.items:
                if delta.field == 'status':
                    start_status = delta.fromString
                    end_status = delta.toString
                    trans_dt = norris.Utilities.datestring_to_datetime( event.created )
                    self._records.append( norris.IssueTransitionsRecord( start_status, end_status, trans_dt ) )
        
        return None
        
    def __str__( self ):
        
        s = 'Transitions:\n'
        for record in self._records:
            s += '  %s\n' % ( record )
        s = s[:-1]
            
        return s
    
    @property
    def records( self ):
        return self._records
