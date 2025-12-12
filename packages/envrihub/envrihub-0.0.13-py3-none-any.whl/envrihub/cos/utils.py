from datetime import datetime

def datetime_to_epos_format(dt:datetime)->str:
    return dt.isoformat()