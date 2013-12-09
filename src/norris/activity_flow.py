import copy
import datetime
import norris

class ActivityFlow( object ):
    
    def __init__( self, issues, schema ):
        
        self._snapshot_dt = datetime.datetime.now()
        self._snapshot_period = datetime.timedelta( days = 1 )

        self._from_dt = self._snapshot_dt - self._snapshot_period
        self._to_dt = self._snapshot_dt
        
        self._issues = issues
        self._schema = schema
        
        self._stages = copy.deepcopy( ActivityFlowDefinitions.flowdef[schema] )
        
        for issue in self._issues:

            # deal with adding this issue to the appropriate stage inventory count

            r = issue.status.split( ' - ' )
            if len( r ) == 1:
                istage = r[0]
            elif len( r ) == 2:
                istage = r[0]
                istate = r[1]
            else:
                ##### DEBUG
                print "Dropped unparsable status = %s" % ( issue.status )
                ##### DEBUG

            stage = [ s for s in self._stages if s.name == istage ][0]
            
            if isinstance( stage, norris.Store ):
                stage.inventory += 1
            elif isinstance( stage, norris.Station ):
                if istate == 'Queued':
                    stage.queued += 1
                elif istate == 'Active':
                    stage.active += 1
                elif istate == 'Stalled':
                    stage.stalled += 1
                else:
                    ##### DEBUG
                    print "Dropped unrecognized state = %s" % ( istate )
                    ##### DEBUG
            else:
                ##### DEBUG
                print "Dropped unknown stage class = %s" % ( stage )
                ##### DEBUG

            # go through issue transitions and increment stage arrival and departure counts

            for record in issue.transitions.records:
                
                # filter for desired period
                if self._from_dt <= record.transition_date <= self._to_dt:
                
                    from_stage_name = record.start_status.split( ' - ' )[0]
                    to_stage_name = record.end_status.split( ' - ' )[0]

                    # ignore stage-internal transitions
                    if from_stage_name != to_stage_name:
                        
                        departed_from = [ s for s in self._stages if s.name == from_stage_name ][0]
                        departed_from.departures += 1
    
                        arrived_at = [ s for s in self._stages if s.name == to_stage_name][0]
                        arrived_at.arrivals += 1
            
        return None
    
    def __str__( self ):
        
        s = '%s Flow, %s - %s:\n' % ( self._schema, self._from_dt.strftime( '%x %X' ), self._to_dt.strftime( '%x %X' ) )
        for stage in self._stages:
            s += '  %s\n' % (stage )
        s = s[:-1]
        
        return s
    
class ActivityFlowDefinitions( object ):
    
    flowdef = {
        'Feature': [
            norris.Store( 'Incoming' ),
            norris.Station( 'Design' ),
            norris.Station( 'Code' ),
            norris.Station( 'Test' ),
            norris.Station( 'Release' ),
            norris.Store( 'Discarded' ),
            norris.Store( 'Closed' ),
        ],
        'Task': [
            norris.Store( 'Incoming' ),
            norris.Station( 'Execute' ),
            norris.Station( 'Confirm' ),
            norris.Store( 'Discarded' ),
            norris.Store( 'Closed' ),
        ]
    }
