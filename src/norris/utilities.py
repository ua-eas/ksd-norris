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

