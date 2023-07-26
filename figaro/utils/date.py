from datetime import datetime
import pytz


def current_date_and_time_in_pst():
    pst = pytz.timezone('America/Los_Angeles')
    current_time = datetime.now(pst)
    return current_time.strftime('%B %d, %Y: %I:%M%p PST')
