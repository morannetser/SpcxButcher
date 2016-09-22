class PerChannelFilter:
    def __init__( self, filters ):
        self._filters = filters

    def __call__( self, record ):
        filter = self._filters[ record.channel ]
        return filter( record )
