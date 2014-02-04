'''
Metrics structure objects, used to track status of issues in the delivery pipeline.
'''
import copy


class Node( object ):
    '''
    The abstract base class for all structure nodes.  A node has a name; all
    remaining functionality is implemented in the subclasses.
    '''

    def __init__( self, name ):
        
        self._name = name
        
        return None
    
    @property
    def name( self ):
        return self._name


class Pool( Node ):
    '''
    Pool extends the Node class to represent a simple pool of issues, with
    associated counts for number of issues, sum of severity points, and
    sum of investment points residing in the pool.
    '''

    def __init__( self, name, issues = [] ):
        super( Pool, self ).__init__( name )
        
        self._pooled = copy.deepcopy( issues )

        return None
    
    def __str__( self ):
        
        return '%s Pool: %s issues, %s severity, %s investment' % ( self.name.title().encode( 'utf-8' ),
                                                                    self.size['issues'],
                                                                    self.size['severity'],
                                                                    self.size['investment'] )

    @property
    def csv_headers( self ):
        return [ '%s-pooled-issues' % ( self.name ),
                 '%s-pooled-severity' % ( self.name ),
                 '%s-pooled-investment' % ( self.name ) ]
    
    @property
    def csv_data( self ):
        return [ self.pooled_accum['issues'],
                 self.pooled_accum['severity'],
                 self.pooled_accum['investment' ] ]

    def add_issue( self, issue ):
        
        self.pooled.append( copy.deepcopy( issue ) )
        
        return True

    @property
    def pooled( self ):
        return self._pooled
        
    @property
    def pooled_accum( self ):
        
        a = { 'issues': 0, 'severity': 0, 'investment': 0 }
        for issue in self.pooled:
            a['issues'] += 1
            a['severity'] += issue.severity
            a['investment'] += issue.investment
        
        return a

    @property
    def size( self ):
        
        return self.pooled_accum


class Stage( Node ):
    '''
    Stage extends the Node class to represent one stage in the
    delivery process, with internally-differentiated sets of queued, 
    active, and stalled issues, and their associated counts (number,
    severity, investment).  The sum of all issues is referred to
    as the load for the stage.
    '''

    def __init__( self, name, issues = [] ):
        super( Stage, self ).__init__( name )

        self._queued = []
        self._active = []
        self._stalled = []
        for issue in issues:
            if issue.state == 'queued':
                self._queued.append( copy.deepcopy( issue ) )
            elif issue.state == 'active':
                self._active.append( copy.deepcopy( issue ) )
            elif issue.state == 'stalled':
                self._stalled.append( copy.deepcopy( issue ) )
            else:
                pass        #### need to do something better here
                
        return None
        
    def __str__( self ):
        s = ''
        s += '%s Stage:\n' % ( self.name.title().encode( 'utf-8' ) )
        s += '  Queued: %s issues, %s severity, %s investment\n' % ( self.queued_accum['issues'],
                                                                     self.queued_accum['severity'],
                                                                     self.queued_accum['investment']  )
        s += '  Active: %s issues, %s severity, %s investment\n' % ( self.active_accum['issues'],
                                                                     self.active_accum['severity'],
                                                                     self.active_accum['investment']  )
        s += '  Stalled: %s issues, %s severity, %s investment' % ( self.stalled_accum['issues'],
                                                                    self.stalled_accum['severity'],
                                                                    self.stalled_accum['investment']  )
        return s
    
    @property
    def csv_headers( self ):
        return [ self.name + h for h in 
                    [ '-queued-issues', '-queued-severity', '-queued-investment',
                      '-active-issues', '-active-severity', '-active-investment',
                      '-stalled-issues', '-stalled-severity', '-stalled-investment',
                      '-(skip)', '-(skip)', '-(skip)' ] ]
    
    @property
    def csv_data( self ):
        return [ self.queued_accum['issues'], self.queued_accum['severity'], self.queued_accum['investment'],
                 self.active_accum['issues'], self.active_accum['severity'], self.active_accum['investment'],
                 self.stalled_accum['issues'], self.stalled_accum['severity'], self.stalled_accum['investment'],
                 '', '', '' ]

    def add_issue( self, issue ):
        
        if issue.state == 'queued':
            self.queued.append( copy.deepcopy( issue ) )
        elif issue.state == 'active':
            self.active.append( copy.deepcopy( issue ) )
        elif issue.state == 'stalled':
            self.stalled.append( copy.deepcopy( issue ) )
        else:
            return False    ### or maybe throw an exception?

        return True

    @property
    def queued( self ):
        return self._queued
        
    @property
    def queued_accum( self ):
        
        q = { 'issues': 0, 'severity': 0, 'investment': 0 }
        for issue in self.queued:
            q['issues'] += 1
            q['severity'] += issue.severity
            q['investment'] += issue.investment
        
        return q

    @property
    def active( self ):
        return self._active

    @property        
    def active_accum( self ):
        
        a = { 'issues': 0, 'severity': 0, 'investment': 0 }
        for issue in self.active:
            a['issues'] += 1
            a['severity'] += issue.severity
            a['investment'] += issue.investment
        
        return a
    
    @property
    def stalled( self ):
        return self._stalled

    @property
    def stalled_accum( self ):
        
        s = { 'issues': 0, 'severity': 0, 'investment': 0 }
        for issue in self.stalled:
            s['issues'] += 1
            s['severity'] += issue.severity
            s['investment'] += issue.investment
        
        return s

    @property
    def load( self ):
        
        return { 
            'issues': ( self.queued_accum['issues'] + self.active_accum['issues'] + self.stalled_accum['issues'] ),
            'severity': ( self.queued_accum['severity'] + self.active_accum['severity'] + self.stalled_accum['severity'] ),
            'investment': ( self.queued_accum['investment'] + self.active_accum['investment'] + self.stalled_accum['investment'] ),
        }
