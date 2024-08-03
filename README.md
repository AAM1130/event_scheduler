# event_scheduler
A simple event scheduler for CircuitPython, allows creating single use and repeating events. Time values can be entered as a raw integer (in seconds), or as a time str ('1h30m15s').

I am assuming there are many ways to accomplish this task and I'm certain this is not the most efficient or 'best' way. This was created as a 'stepping stone' tool to help me continue to explore and try more projects. I am always open to constructive feedback.

# Example usage

```
import time
from event_scheduler import Scheduler

# create a scheduler
scheduler = Scheduler()

# create a single use event function to be scheduled as an event.
def single_use():
    print('Hello!')

# create another function that can be scheduled at repeated intervals.
def repeated_use():
    print('Hello, again!')

# schedule single event, 5 seconds (raw integer) after startup
scheduler.add_event(5, single_use, args=None)

# schedule a repeating event, first call 1 minute after start, then again every 1 minute after.
scheduler.add_event('1m', repeated_use, repeat_interval='1min', args=None)

while True:
    scheduler.run_pending()
    time.sleep(0.1)

```

# Breakdown

Import the event scheduler.
```
from event_scheduler import Scheduler
```

create a scheduler instance to add events to.
```
scheduler = Scheduler()
```
create a function to be used as an event, then add that event to the scheduler
```
def repeated_use():
    print('Hello, again!')

scheduler.add_event('1m', repeated_use, repeat_interval='1min', args=None)
```
Note: when creating an event.

(sheduler_instance).add_event((delay), (function_name), (repeat_interval), (function_arguments))

delay: a time, either as an int in seconds, or as a time str. Example. 5, 60, '1m', '2h5s'.

repeat_interval: a time, same as delay. time str (as the name implies) are strings and must be in quotes.

args: any required arguments passed into the function being called.

Last, call the scheduler instance, in the program loop, to run all pending events that are scheduled.
```
scheduler.run_pending()
```


This has only been tested on a teensy 4.1 running CircuitPython 9.1. It should run on nearly any hardware running circuitpython as it only uses the built-in time module.
