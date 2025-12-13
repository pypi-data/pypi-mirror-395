import logging
import os
import sys
from threading import Thread
from time import time, sleep


class SafeThread(Thread):
    crashed = None

    def run(self):
        try:
            self.run_safely()
        except:
            self.crashed = "%s: %s" % (sys.exc_info()[0].__name__, sys.exc_info()[1])
            logging.exception(sys.exc_info()[0])

    def run_safely(self):
        super().run()


class ThreadsWatcher:
    running = True

    def __init__(self):
        self.threads = []
        self.on_exception = self.log_and_exit

    def start(self, thread):
        thread.start()
        self.register(thread)

    def register(self, thread):
        self.threads.append(thread)

    def watch(self, interval=1, stop_after_threads=False):
        begin = time()
        interval = float(interval)
        while self.running:
            self.check()

            if stop_after_threads and len(self.threads) == 0:
                break

            sleep(interval - ((time() - begin) % interval))

    def check(self):
        for thread in self.threads:
            remove = False
            if isinstance(thread, SafeThread):
                if thread.crashed:
                    self.on_exception(thread, thread.crashed)
                    remove = True
                elif not thread.is_alive():
                    remove = True

            elif not thread.is_alive():
                self.on_exception(thread)
                remove = True

            if remove:
                self.threads.remove(thread)

    def stop(self):
        self.running = False

    def log_and_exit(self, thread, exception=None):
        if exception:
            message = "thread '%s' crashed with exception '%s'" % (thread, exception)
            message += ", see stacktrace abode for details"
        else:
            message = "thread '%s' ended gracefully because of logic error" % str(thread)
            message += " or crashed with unknown exception, see complete log for possible details"

        message += ", application will exit now"

        logging.error(message)
        exit(1)


class CrashThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_exception = self.log_and_crash

    def run(self):
        try:
            super().run()
        except:
            self.on_exception(sys.exc_info()[0])

    def log_and_crash(self, exception):
        logging.exception(exception)
        message = "thread '%s' crashed with exception '%s'" % (self, exception)
        message += ", see stacktrace abode for details, application will be killed now"
        logging.error(message)
        os._exit(1)
