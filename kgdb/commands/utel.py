import gdb
import kgdb.utils.CommonUtils as utils

class utel(gdb.Command):
    """utel: quickly telescope offset of the base
    """
    def __init__(self, segmentname):
        self.segmentname = segmentname
        super(self.__class__, self).__init__("utel", gdb.COMMAND_USER)
    
    def invoke(self, args, from_tty):
        pid = gdb.selected_inferior().pid
        pid = int(pid)
        try:
            address = eval(args)
        except Exception:
            raise Exception("parameter error: " + args)
        base = utils.getbase(pid, self.segmentname)
        gdb.execute("tel " + hex(base + address))
