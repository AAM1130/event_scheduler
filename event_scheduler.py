"""
Name: event_scheduler
Author: Handled (in collaboration with ChatGPT)
Date: 08/03/2024

Purpose: During my initial exploration of CircuitPython, I have yet to find a simple application to run events
on unique intervals without async or threading. (maybe I just haven't found it...) The module allow scheduling
single and repeated events based on a time.monotonic delay. This is currently only using a delay in seconds.

To Do: I may need to adapt a more complete time structure to the delay to use seconds, minutes, hours, and days.

"""

import time

class Event:
    def __init__(self, time_to_run, callback, repeat_interval=None, args=None, kwargs=None):
        """
        Initialize an event.

        Parameters:
        time_to_run (float): The time at which the event should run.
        callback (function): The function to call when the event runs.
        repeat_interval (float or None): The interval in seconds for repeating events.
        args (list): The positional arguments to pass to the callback.
        kwargs (dict): The keyword arguments to pass to the callback.
        """
        self.time_to_run = time_to_run
        self.callback = callback
        self.repeat_interval = repeat_interval
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}

    def run(self):
        """
        Run the event.

        Returns:
        bool: True if the event is repeating and should be rescheduled, False otherwise.
        """
        # print(f"Running event with args: {self.args} and kwargs: {self.kwargs}")
        self.callback(*self.args, **self.kwargs)
        if self.repeat_interval is not None:
            self.time_to_run = time.monotonic() + self.repeat_interval
            return True
        return False

class Scheduler:
    def __init__(self):
        """
        Initialize the scheduler.
        """
        self.events = []

    def add_event(self, delay, callback, repeat_interval=None, args=None, kwargs=None):
        """
        Add an event to the scheduler.

        Parameters:
        delay (float or str): The delay before the event should run, in seconds or as a time string (e.g., "1h30m").
        callback (function): The function to call when the event runs.
        repeat_interval (float or str or None): The interval in seconds or as a time string for repeating events. Default is None.
        args (list): The positional arguments to pass to the callback.
        kwargs (dict): The keyword arguments to pass to the callback.
        """
        delay_seconds = self._parse_time(delay)
        # print(f"Parsed delay: {delay_seconds} seconds")

        if repeat_interval is not None:
            repeat_interval_seconds = self._parse_time(repeat_interval)
        else:
            repeat_interval_seconds = None

        # print(f"Parsed repeat interval: {repeat_interval_seconds} seconds")

        time_to_run = time.monotonic() + delay_seconds
        event = Event(time_to_run, callback, repeat_interval_seconds, args, kwargs)
        self.events.append(event)

    def _parse_time(self, time_str):
        """
        Convert a time string (e.g., "1h30m") or a number (seconds) into seconds.

        Parameters:
        time_str (str or float): The time as a string or number to convert.

        Returns:
        float: The time in seconds.
        """
        if isinstance(time_str, (int, float)):
            return float(time_str)
        if isinstance(time_str, str):
            total_seconds = 0
            units = {'h': 3600, 'm': 60, 's': 1}
            time_str = time_str.lower()
            for unit, seconds in units.items():
                if unit in time_str:
                    parts = time_str.split(unit)
                    number_part = ''.join(filter(str.isdigit, parts[0]))
                    if number_part:
                        try:
                            total_seconds += int(number_part) * seconds
                        except ValueError as e:
                            print(f"ValueError: {e} - with input {number_part}")
            return total_seconds
        return 0

    def run_pending(self):
        """
        Run all events that are scheduled to run.
        """
        current_time = time.monotonic()
        for event in self.events[:]:
            if current_time >= event.time_to_run:
                if not event.run():
                    self.events.remove(event)
