# https://github.com/andyortlieb/py-idletimer

import os
import sys
import time
import random
import logging
import datetime
import threading
now = datetime.datetime.now
log = logging.getLogger("idletimer")


def exit(code=1):
    def _exit(timer):
        os._exit(code)
    return _exit


class IdleTimer(threading.Thread):
    daemon = True
    end = None

    def __init__(self, wait, deviation=0, callback=None, *args, **kwargs):
        self.timeout_handlers = []
        self.bump_handlers = []
        self.ret = []
        self.timeout = wait + random.randint(-deviation, deviation)

        if callback:
            self.timeout_handlers.append(callback)

        super(IdleTimer, self).__init__(*args, **kwargs)

    def bump(self):
        old = self.end
        self.end = now() + datetime.timedelta(seconds=self.timeout)
        log.debug("[%s] Bumping from %s to %s" % (self.name, old, self.end))

        bump_ret = []
        for cb in self.bump_handlers:
            bump_ret.append(cb(self))
        return bump_ret

    def run(self):
        self.bump()
        log.debug("[%s] Starting the timer %s" % (self.name, self))

        while (self.end > now()):
            howlong = (self.end-now()).total_seconds()
            if howlong < 0:
                break
            log.debug("[%s] Going to sleep for %s" % (self.name, howlong))
            time.sleep(howlong)

        log.debug("[%s] No longer waiting. It's %s, end time was %s" % (self.name, now(), self.end))

        # We're out of the loop, so we must have idled long enough
        for cb in self.timeout_handlers:
            self.ret.append(cb(self))

    # A decorator to add timeout_handlers
    def timeout_handler(self, fn):
        self.timeout_handlers.append(fn)
        return fn

    def bump_handler(self, fn):
        self.bump_handlers.append(fn)
        return fn
