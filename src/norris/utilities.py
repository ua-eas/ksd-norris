import datetime

class Utilities( object ):

    def __init__( self ):
        return None

    @staticmethod
    def datestring_to_datetime( datestring ):
        return datetime.datetime.strptime( datestring[0:-5], '%Y-%m-%dT%H:%M:%S.000' )
    
    @staticmethod
    def now_as_datestring():
        return datetime.datetime.now().strftime( '%Y-%m-%dT%H:%M:%S.000XXXXX' )

    @staticmethod    
    def timedelta_to_days( timedelta ):
        return ( timedelta.total_seconds() / 86400 )
    
    @staticmethod
    def to_unicode( obj, encoding = 'utf-8' ):
        if isinstance( obj, basestring ):
            if not isinstance( obj, unicode ):
                obj = unicode( obj, encoding )
        return obj

    @staticmethod
    def indent( block1, n = 0 ):
        spacer = ( ' ' * n )
        block2 = spacer.join( block1.splitlines( True ) )
        block2 = spacer + block2
        return block2

    