'''
Metrics flow objects, used to track some kind of measurement per unit time.
'''

import copy
import norris

class Measure( object ):
    '''
    The abstract base class for all measurements.  A measure has a name, a 
    period of time during which the measurement is taken (defined by the 
    starting and ending dates), and an interval (the time unit of measurement
    expressed as a Python timedelta object).
    '''
    
    def __init__( self, name, start_date, end_date, interval ):
        
        self._name = name
        self._start_date = start_date
        self._end_date = end_date
        self._interval = interval
        
        return None
    
    @property
    def name( self ):
        return self._name

    @property
    def start_date( self ):
        return self._start_date
    
    @property
    def end_date( self ):
        return self._end_date

    @property
    def duration( self ):
        return self._end_date - self._start_date

    @property
    def interval( self ):
        return self._interval

    @property
    def rate_conversion_factor( self ):
        return ( float( self.interval.total_seconds() ) / float( self.duration.total_seconds() ) )


class Event( object ):
    '''
    Events are the JIRA transitions that we want to track with our
    flow measurements.  We apply a little syntactic sugar so that
    we can check for Event equality with cleaner syntax in our
    Measure code.
    '''
    
    def __init__( self, from_status, to_status ):
        
        self._from_status = from_status
        self._to_status = to_status
        
        return None

    def __str__( self ):
        return 'Flow Event [ "%s" -> "%s" ]' % ( self.from_status.encode( 'utf-8' ),
                                                 self.to_status.encode( 'utf-8' ) )

    def __eq__( self, other ):
        if type( other ) is type( self ):
            return self.__dict__ == other.__dict__
        else:
            return False
    
    def __ne__( self, other ):
        return not self.__eq__( other )
    
    @property
    def from_status( self ):
        return self._from_status
    
    @property
    def to_status( self ):
        return self._to_status


class Rate( Measure ):
    '''
    Rate extends the Measure class to represent a simple set of transition
    events for which we want to measure unidirectional flow (count per unit
    time).  All counts are done three ways, as number of issues, sum of 
    severity points, and sum of investment points.
    '''

    def __init__( self, name, start_date, end_date, interval, events = [] ):
        super( Rate, self ).__init__( name, start_date, end_date, interval )

        self._events = copy.deepcopy( events )
        self._counts = { 'issues': 0,
                         'severity': 0,
                         'investment': 0
        }

        return None
    
    def __str__( self ):
        return '%s Rate: %s | issues = %s, severity = %s, investment = %s' % ( self.name.title().encode( 'utf-8' ),
                                                                               str( norris.Utilities.timedelta_as_interval( self.interval ) ).encode( 'utf-8' ),
                                                                               str( round( self.issue_rate, 1 ) ).encode( 'utf-8' ),
                                                                               str( round( self.severity_rate, 1 ) ).encode( 'utf-8' ),
                                                                               str( round( self.investment_rate, 1 ) ).encode( 'utf-8' ) )
        
    @property
    def csv_headers( self ):
        return [ '%s-issues' % ( self.name ),
                 '%s-severity' % ( self.name ),
                 '%s-investment' % ( self.name ) ]

    @property
    def csv_data( self ):
        return [ round( self.issue_rate, 1 ), round( self.severity_rate, 1 ), round( self.investment_rate, 1 ) ]

    @property
    def events( self ):
        return self._events

    @property
    def counts( self ):
        return self._counts

    @property
    def issue_rate( self ):
        return ( self.counts['issues'] * self.rate_conversion_factor )

    @property
    def severity_rate( self ):
        return ( self.counts['severity'] * self.rate_conversion_factor )

    @property
    def investment_rate( self ):
        return ( self.counts['investment'] * self.rate_conversion_factor )

    def add_to_counts( self, issue ):
        self.counts['issues'] += 1
        self.counts['severity'] += issue.severity
        self.counts['investment'] += issue.investment
        
    def analyze( self, issue ):
        for record in issue.transitions.records:
            if self.start_date <= record.transition_date <= self.end_date:
                ite = norris.Event( record.start_status, record.end_status )      # "ite" is "issue transition event"
                for etm in self.events:                                           # "etm" is "event to measure"
                    if ite == etm:                          # transition matched a measured event, so add to count
                        self.add_to_counts( issue )
        return None


class Pressure( Measure ):
    '''
    Pressure extends the Measure class to represent a circular flow, with
    a set of "forward" events counterposed with a set of "backward" events.
    Pragmatically, we just bury a forward Rate and backward Rate inside
    each Pressure instance, and provide some method sugar to simplify
    summing up the resulting pressure rates.
    '''

    def __init__( self, name, start_date, end_date, interval, forward_events = [], backward_events = [] ):
        super( Pressure, self ).__init__( name, start_date, end_date, interval )

        self._forward_rate = norris.Rate( name, start_date, end_date, interval, forward_events )
        self._backward_rate = norris.Rate( name, start_date, end_date, interval, backward_events )

        return None
    
    def __str__( self ):
        s = ''
        s += '%s Pressure: %s |\n' % ( self.name.title().encode( 'utf-8' ),
                                       str( norris.Utilities.timedelta_as_interval( self.interval ) ).encode( 'utf-8' ) )
        s += '  Tau: issues = %s, severity = %s, investment = %s\n' % ( str( round( self.forward.issue_rate, 1 ) ).encode( 'utf-8' ),
                                                                        str( round( self.forward.severity_rate, 1 ) ).encode( 'utf-8' ),
                                                                        str( round( self.forward.investment_rate, 1 ) ).encode( 'utf-8' ) )
        s += '  Omega: issues = %s, severity = %s, investment = %s' % ( str( round( self.backward.issue_rate, 1 ) ).encode( 'utf-8' ),
                                                                        str( round( self.backward.severity_rate, 1 ) ).encode( 'utf-8' ),
                                                                        str( round( self.backward.investment_rate, 1 ) ).encode( 'utf-8' ) )
        return s

    @property
    def csv_headers( self ):
        return [ self.name + h for h in
                    [ '-tau-issues', '-tau-severity', '-tau-investment',
                     '-omega-issues', '-omega-severity', '-omega-investment',
                     '-(skip)', '-(skip)', '-(skip)' ] ]


    @property
    def csv_data( self ):
        return [ round( self.forward.issue_rate, 1 ), round( self.forward.severity_rate, 1 ), round( self.forward.investment_rate, 1 ),
                 round( self.backward.issue_rate, 1 ), round( self.backward.severity_rate, 1 ), round( self.backward.investment_rate, 1 ),
                 '', '', '' ]

    @property
    def forward( self ):
        return self._forward_rate
    
    @property
    def tau( self ):
        return self._forward_rate.counts

    @property
    def backward( self ):
        return self._backward_rate
    
    @property
    def omega( self ):
        return self._backward_rate.counts

    @property
    def sigma( self ):
        return { 'issues': ( self.tau['issues'] - self.omega['issues'] ),
                 'severity': ( self.tau['severity'] - self.omega['severity'] ),
                 'investment': ( self.tau['investment'] - self.omega['investment'] ) }
        
    @property
    def issue_pressure( self ):
        return ( self.sigma['issues'] * self.rate_conversion_factor )

    @property
    def severity_pressure( self ):
        return ( self.sigma['severity'] * self.rate_conversion_factor )

    @property
    def investment_pressure( self ):
        return ( self.sigma['investment'] * self.rate_conversion_factor )

    def analyze( self, issue ):
        self._forward_rate.analyze( issue )
        self._backward_rate.analyze( issue )
        return None
    