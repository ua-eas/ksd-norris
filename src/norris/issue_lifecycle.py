import norris

class IssueLifecycle( object ):
    
    def __init__( self, jira_issue ):
        
        self._records = []
        current_status = 'Incoming'                 ### BAD ASSUMPTION HERE, HOW TO FIX?
        start_dt = norris.Utilities.datestring_to_datetime( jira_issue.fields.created )
        for event in jira_issue.changelog.histories:
            for delta in event.items:
                if delta.field == 'status':
                    end_dt = norris.Utilities.datestring_to_datetime( event.created )
                    self._records.append( norris.IssueLifecycleRecord( current_status, start_dt, end_dt ) )
                    current_status = delta.toString
                    start_dt = end_dt
        end_dt = norris.Utilities.datestring_to_datetime( norris.Utilities.now_as_datestring() )
        self._records.append( norris.IssueLifecycleRecord( current_status, start_dt, end_dt ) )
        
        return None
        
    def __str__( self ):
        
        s = 'Lifecycle:\n'
        for record in self._records:
            s += '  %s\n' % ( record )
        s = s[:-1]
            
        return s
    
    @property
    def records( self ):
        return self._records
