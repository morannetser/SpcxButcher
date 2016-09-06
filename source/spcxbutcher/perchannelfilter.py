class PerChannelFilter:
    def __init__( self, records, filters ):
        results = []
        for record in records:
            filter = filters[ record.channel ]
            if filter( record ):
                results.append( record )

        self._results = results

    @property
    def results( self ):
        return self._results
