import os.path
import gdb
import re

def getbase(pid, content):
    mapspath = os.path.join('/proc', str(pid), 'maps')
    if not os.path.exists(mapspath):
        return 0
    info = open(mapspath).read()
    info = info.split('\n')
    res = -1
    for s in info:
        if not content in s:
            continue
        base = s.split('-')[0]
        base = int(base, 16)
        if res == -1:
            res = base
        elif res > base:
            res = base
    if res == -1:
        return 0
    return res

def getaddr(sym):
    if not type(sym) == str:
        raise Exception("getaddr Error: sym must be string")
    res = gdb.execute('x/x &' + sym, to_string = True)
    if 'No symbol' in res:
        return 0
    else:
        res = re.search('0x.*[0-9a-fA-F] ', res)
        res = res.group()
        res = int(res[:-1], 16)
    return res


def vmmap(pid):
    """
    [
        [
            [start, end],
            access,
            offset,
            dev,
            inode,
            pathname
        ],

        [
            [start, end],
            access,
            offset,
            dev,
            inode,
            pathname
        ],
        ...
    ]
    """
    def clearlist(l):
        res = []
        for i in l:
            if not i == '':
                res.append(i)
        return res 

    mapspath = os.path.join('/proc', str(pid), 'maps')
    if not os.path.exists(mapspath):
        return None
    info = open(mapspath).read()
    info = info.split('\n')
    info = clearlist(info)
    for i in range(len(info)):
        info[i] = clearlist(info[i].split(' '))
    for i in range(len(info)):
        info[i][0] = info[i][0].split('-')
        info[i][0][0] = int(info[i][0][0], 16)
        info[i][0][1] = int(info[i][0][1], 16)
    for inf in info:
        if len(inf) == 5:
            inf.append('System Mmap Areas')
    return info
    
    
def to_int(s):
    try:
        return int(s, 16)
    except ValueError:
        pass
    try:
        return int(s, 10)
    except ValueError:
        pass
    try:
        return int(s, 8)
    except ValueError:
        pass
    try:
        return int(s, 2)
    except ValueError:
        raise ValueError("invalid literal for to_int(): " + s)
        
