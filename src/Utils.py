import threading
from functools import wraps

def delay(delay=0.):
    """
    Decorator delaying the execution of a function for a while.
    """
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = threading.Timer(delay, f, args=args, kwargs=kwargs)
            timer.start()
        return delayed
    return wrap

class Timer():
    toClearTimer = False
    def setTimeout(self, fn, time):
        isInvokationCancelled = False
        @delay(time)
        def some_fn():
                if (self.toClearTimer is False):
                        fn()
                else:
                    print('Invokation is cleared!')        
        some_fn()
        return isInvokationCancelled
    def setClearTimer(self):
        self.toClearTimer = True