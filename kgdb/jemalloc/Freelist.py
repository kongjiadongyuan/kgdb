from kgdb.jemalloc.jemalloc_utils import *

class Freelist:
    def __init__(self):
        self._bin = {}
        for idx in range(len(sztable)):
            self._bin[bin2size(idx)] = []
    
    def __add__(self, other):
        tmpkeys = self._bin.keys()
        if not tmpkeys == other._bin.keys():
            raise Exception("Freelist False.")
        res = Freelist()
        for k in other._bin.keys():
            res._bin[k] = self._bin[k] + other._bin[k]
        return res
    
    def add(self, size, addr):
        if size not in self._bin.keys():
            raise Exception("Size Error.")
        if type(addr) == int:
            if addr in self._bin[size]:
                raise Exception("Free region exists.")
            self._bin[size].append(addr)
        if type(addr) == list:
            for a in addr:
                if a in self._bin[size]:
                    raise Exception("Free region exists.")
                self._bin[size].append(a)
    
    def __str__(self):
        res = ''
        for sz in self._bin.keys():
            res += '=' * 15 + '\n'
            res += hex(sz) + ':\n'
            if len(self._bin[sz]) == 0:
                res += 'Empty\n'
                continue
            self._bin[sz].sort()
            for addr in self._bin[sz]:
                res += hex(addr) + '\n'
        res += '=' * 15
        return res