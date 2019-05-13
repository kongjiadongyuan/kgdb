import gdb
import kgdb.utils.CommonUtils as utils

class whereis(gdb.Command):
    """whereis: quickly findout which file does the address belong to.
    Usage: whereis [address]
    Example: 
        (gdb) whereis 0x7ffffffff
    """
    def __init__(self):
        super(self.__class__, self).__init__("whereis", gdb.COMMAND_USER)
    
    def find(self, pid, address):
        inf = utils.vmmap(pid)
        for i in range(len(inf)):
            if address >= inf[i][0][0] and address <= inf[i][0][1]:
                return inf[i][0][0], inf[i][0][1], inf[i][5]
        return None, None, None
    
    def invoke(self, args, from_tty):
        pid = gdb.execute('pid', to_string = True)
        pid = int(pid)
        try:
            address = eval(args)
        except Exception:
            raise Exception("parameter error: " + args)
        low, high, path = self.find(pid, address)
        if not low == None:
            print(hex(low) + '-' + hex(high) + '\t\t' + path)
        else:
            print("Address Not Found.")
        
whereis()