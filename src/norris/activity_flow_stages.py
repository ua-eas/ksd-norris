class ActivityFlowStage( object ):
    
    def __init__( self, name, arrivals = 0, departures = 0 ):
        
        self._name = name
        self._arrivals = arrivals
        self._departures = departures

        return None
    
    @property
    def name( self ):
        return self._name
    
    @property
    def arrivals( self ):
        return self._arrivals
    
    @arrivals.setter
    def arrivals( self, value ):
        self._arrivals = value
        return None
    
    @property
    def departures( self ):
        return self._departures

    @departures.setter
    def departures( self, value ):
        self._departures = value
        return None

class Store( ActivityFlowStage ):
    
    def __init__( self, name, arrivals = 0, departures = 0, inventory = 0 ):
        super( Store, self ).__init__( name, arrivals, departures )
        
        self._inventory = inventory
        
        return None
    
    def __str__( self ):
        return '%s: +%d / -%d; %d' % ( self.name, self.arrivals, self.departures, self.inventory )
    
    @property
    def inventory( self ):
        return self._inventory

    @inventory.setter
    def inventory( self, value ):
        self._inventory = value
        return None

class Station( ActivityFlowStage ):
    
    def __init__( self, name, arrivals = 0, departures = 0, queued = 0, active = 0, stalled = 0 ):
        super( Station, self ).__init__( name, arrivals, departures )
        
        self._queued = queued
        self._active = active
        self._stalled= stalled
        
        return None

    def __str__( self ):
        return '%s: +%d / -%d; %d (q = %d, a = %d, s = %d)' % ( self.name, self.arrivals, self.departures, self.inventory,
                                                                self.queued, self.active, self.stalled )

    @property
    def queued( self ):
        return self._queued

    @queued.setter
    def queued( self, value ):
        self._queued = value
        return None

    @property
    def active( self ):
        return self._active

    @active.setter
    def active( self, value ):
        self._active = value
        return None

    @property
    def stalled( self ):
        return self._stalled
    
    @stalled.setter
    def stalled( self, value ):
        self._stalled = value
        return None

    @property
    def inventory( self ):
        return ( self._queued + self._active + self._stalled )
