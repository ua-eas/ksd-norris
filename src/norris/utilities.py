import datetime
import norris

class Utilities( object ):

    def __init__( self ):
        return None

    @staticmethod
    def datestring_to_datetime( date_string ):
        return datetime.datetime.strptime( date_string[0:-5], '%Y-%m-%dT%H:%M:%S.000' )
    
    @staticmethod
    def now_as_datestring():
        return datetime.datetime.now().strftime( '%Y-%m-%dT%H:%M:%S.000XXXXX' )

    @staticmethod    
    def timedelta_to_days( time_delta ):
        return ( time_delta.total_seconds() / 86400 )

    @staticmethod
    def timedelta_as_interval( time_delta ):
        nsecs = int( time_delta.total_seconds() )
        if nsecs == 86400:
            return 'per day'
        elif nsecs == 604800:
            return 'per week'
        elif nsecs == 2592000:
            return 'per month'
        else:
            return ( 'per %s days' % ( norris.Utilities.timedelta_to_days( time_delta ) ) )
    
    @staticmethod
    def display_strftime( date_time ):
        return date_time.strftime( '%m/%d/%Y' )
    
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

    