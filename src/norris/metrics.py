import norris

class Metrics( object ):
    '''
    Metrics capture statistics on delivery structure (the various pools and
    stages in the delivery pipeline) and delivery flow (measurements of various
    rates of issue transfer between nodes in the structure).  A given metrics
    instance is always built from a schema definition pulled from the Norris
    configuration file: you apply a metrics schema to a specific set of issue,
    setting starting and ending dates for the transitions you want to count.
    You also have to specify the interval, which is the per-unit-of-time used
    for the rate calculations; e.g. specifying an interval of seven days will
    give you rates expressed as things-per-week, an interval of thirty days
    gives you things-per-month, etc.  Note that most of the twitchy details in
    terms of counting and analyzing issues are handled in the metric Structure
    and Flow classes, rather than here: the Metrics instance is just a container
    that builds structures and flows from schema definitions, then hands off
    the issues to those components for further analysis.
    '''

    def __init__( self, issues, schema, from_date, to_date, interval, config ):
        
        self._issues = issues
        self._schema = schema
        self._from_date = from_date
        self._to_date = to_date
        self._interval = interval
        
        schema_definition = config['metrics'][schema]

        # build structure objects based on configured definition
        self._structure = []
        for node in schema_definition['structure']:
            if node['type'] == 'pool':
                self._structure.append( norris.Pool( node['name'] ) )
            elif node['type'] == 'stage':
                self._structure.append( norris.Stage( node['name'] ) )
            else:
                pass            #### need to throw exception or warning or something more useful here

        # build flow objects based on configured definition
        self._flow = []
        for measure in schema_definition['flow']:
            name = measure['name']
            if measure['type'] == 'rate':
                events = []
                for e in measure['events']:
                    events.append( norris.Event( e['from'], e['to'] ) )
                self._flow.append( norris.Rate( name, from_date, to_date, interval, events ) )
            elif measure['type'] == 'pressure':
                forward_events = []
                for e in measure['forward_events']:
                    forward_events.append( norris.Event( e['from'], e['to'] ) )
                backward_events = []
                for e in measure['backward_events']:
                    backward_events.append( norris.Event( e['from'], e['to'] ) )
                self._flow.append( norris.Pressure( name, from_date, to_date, interval, forward_events, backward_events  ) )

        # for each issue being analyzed in this metric set
        for issue in self._issues:

            # analyze issue based on structure
            nodes = [ n for n in self._structure if n.name == issue.node ]
            if len( nodes ) == 1:
                nodes[0].add_issue( issue )
            else:
                pass        ### need to throw exception or log to stderr or something useful
            
            # analyze issue based on flow
            for measure in self._flow:
                measure.analyze( issue )

        return None

    def __str__( self ):
        
        return '%s Metrics [ analyzed %s issues, for %s days from %s to %s ]' % ( self.schema.title().encode( 'utf-8' ),
                                                                                  str( len( self.issues ) ).encode( 'utf-8' ),
                                                                                  str( int( norris.Utilities.timedelta_to_days( self.period ) ) ).encode( 'utf-8' ),
                                                                                  norris.Utilities.display_strftime( self.from_date ).encode( 'utf-8' ),
                                                                                  norris.Utilities.display_strftime( self.to_date ).encode( 'utf-8' ) )

    @property
    def issues( self ):
        return self._issues
    
    @property
    def schema( self ):
        return self._schema
    
    @property
    def from_date( self ):
        return self._from_date
    
    @property
    def to_date( self ):
        return self._to_date

    @property
    def period( self ):
        return self.to_date - self.from_date

    @property
    def interval( self ):
        return self._interval
    
    @property
    def structure( self ):
        return self._structure
    
    @property
    def flow( self ):
        return self._flow
    