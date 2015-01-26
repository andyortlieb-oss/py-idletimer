import sys
import logging
from . import *
rootLogger = logging.getLogger()
log = logging.getLogger("idletimer_test")

if __name__ == '__main__':
    stdo = logging.StreamHandler(sys.stdout)
    stdo.setLevel(logging.DEBUG)
    stdo.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s : %(message)s"))
    rootLogger.addHandler(stdo)  # Root logger.
    rootLogger.setLevel(logging.DEBUG)

    log.info("Starting Tests")

    delayer = IdleTimer(5, callback=None)
    log.info("Running (not starting) delayer.")
    delayer.run()
    log.info("Delayer returned.")


    # Test the thing.
    i_2sec = IdleTimer(3, callback=None)
    i_7sec_3sec = IdleTimer(7, 3, callback=None)

    def i_8sec_cb(timer):
        timer.customcb="Done"
    i_8sec = IdleTimer(8, callback=i_8sec_cb)

    i_11sec = IdleTimer(11)
    i_300sec = IdleTimer(12)

    starttime = now()
    i_2sec.start()
    i_7sec_3sec.start()
    i_8sec.start()
    i_11sec.start()
    i_300sec.start()

    i_11sec.bump()
    i_2sec.join()
    log.info("i_2sec lasted for %s sec", (now() -starttime).total_seconds())

    i_11sec.bump()
    i_7sec_3sec.join()
    log.info("i_7sec_3sec lasted for %s sec", (now() -starttime).total_seconds())

    i_11sec.bump()
    i_8sec.join()
    log.info("i_8sec lasted for %s sec", (now() -starttime).total_seconds())
    log.info("Did custom cb work? %s" % i_8sec.customcb)

    log.info("Going to let 11 second timer kill us.")
    i_11sec.bump()    
    i_300sec.join()
    log.error("You should never see this!")

