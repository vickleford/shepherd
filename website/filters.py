from time import gmtime, asctime


def ms2utc(timems):
    timestamp = gmtime(timems / 1000)
    str_timestamp = asctime(timestamp)
    
    return str_timestamp
