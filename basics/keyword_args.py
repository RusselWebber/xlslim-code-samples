from datetime import datetime, timedelta


def hours_between(start=None, end=None, default_period=24.0, return_minutes=False):
    """A simple function to show the hours between two datetimes.
    
    start - optional - the start datetime that defaults to now. 
    end - optional - the end datetime that defaults to 24 hours after the start. 
    default_period - optional - the default number of hours to add to start if end is not supplied. 
    return_minutes - optional - return the result in hours rather than minutes. 
    
    """
    if start is None:
        start = datetime.now()
    if end is None:
        end = start + timedelta(hours=default_period)
    seconds = (end - start).total_seconds()
    hours = seconds / 60.0 / 60.0
    minutes = seconds / 60.0
    return minutes if return_minutes else hours


def hours_between_with_hints(
    start: datetime = None,
    end: datetime = None,
    default_period: float = 24.0,
    return_minutes: bool = False,
) -> float:
    """A simple function to show the hours between two datetimes.
    
    start - optional - the start datetime that defaults to now. 
    end - optional - the end datetime that defaults to 24 hours after the start. 
    default_period - optional - the default number of hours to add to start if end is not supplied. 
    return_minutes - optional - return the result in hours rather than minutes. 
    
    """
    return hours_between(start, end, default_period, return_minutes)


if __name__ == "__main__":

    print(hours_between_with_hints())
