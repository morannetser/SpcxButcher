def deadtimeFilter( records, deadtime ):
    iterator = iter( records )
    previous = next( iterator )
    result = [ previous ]
    for current in iterator:
        if current.timestamp - previous.timestamp > deadtime:
            result.append( current )
            previous = current

    return result
