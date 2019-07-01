import gdb

class HookPoint(gdb.Breakpoint):
    """
        HookPoint supports customizing our own function.
        The "spec" must be an address to .text.
    """
    def __init__(self, spec, func):
        self.func = func
        super(self.__class__, self).__init__(spec)

    def stop(self):
        self.func()
        return False