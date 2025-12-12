from time import sleep, time
beginning = time()
start_time = 0
end_time = 0

def wait(millis):
    """Pause the program for the given milliseconds."""
    sleep(millis / 1000)

def stopwatch(signal):
    """
    Start or stop the stopwatch.

    Args:
        signal (str): "START" or "STOP" (case insensitive)

    Returns:
        float: elapsed time in seconds when stopped
    """
    global start_time, end_time
    s = str(signal).upper()
    if s == "START":
        start_time = time()
    elif s == "STOP":
        end_time = time()
        show = end_time - start_time
        start_time = 0
        return show
def from_start():
    """Return the time elapsed since the module was imported."""
    return time() - beginning

