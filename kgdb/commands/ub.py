import gdb
import kgdb.utils.CommonUtils as utils

class ub(gdb.Command):
    """ub: quickly break at the offset of some segment
    Usage: ub 0x10
    """
    def __init__(self, segmentname):
        self.segmentname = segmentname
        super(self.__class__, self).__init__("ub", gdb.COMMAND_USER)
    
    def invoke(self, args, from_tty):
        pid = gdb.selected_inferior().pid
        pid = int(pid)
        try:
            address = eval(args)
        except Exception:
            raise Exception("parameter error: " + args)
        base = utils.getbase(pid, self.segmentname)
        gdb.execute('break *' + hex(base + address))