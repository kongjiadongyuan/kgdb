from elftools.elf.elffile import *
import os
from capstone import *
from pwn import *


def get_ehframe_vaddr(elffile):
    ehframe = elffile.get_section_by_name('.eh_frame')
    vaddr = ehframe.header['sh_addr']
    return vaddr 

def logic2physic(elffile, addr):
    for s in elffile.iter_segments():
        baseaddr = s.header['p_vaddr']
        size = s.header['p_memsz']
        if addr >= baseaddr and addr <= baseaddr + size:
            offset = addr - baseaddr 
            physicaddr = s.header['p_offset'] + offset 
            return physicaddr 
    raise Exception('logic2physic: addr not found.')

def physic2logic(elffile, addr):
    for s in elffile.iter_segments():
        baseaddr = s.header['p_offset']
        size = s.header['p_memsz']
        if addr >= baseaddr and addr <= baseaddr + size:
            offset = addr - baseaddr 
            logicaddr = s.header['p_vaddr'] + offset 
            return logicaddr 
    raise Exception('physic2logic: addr not found.')

def get_call_vaddr(f, elffile, vaddr):
    paddr = logic2physic(elffile, vaddr)
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    f.seek(paddr)
    content = f.read(0x30)
    oplist = []
    for ins in md.disasm(content, vaddr):
        oplist.append(ins)
    if not oplist[0].mnemonic == 'call':
        raise Exception("get_call_vaddr: instruction is not call.")
    print oplist[0].mnemonic, oplist[0].op_str
    call_vaddr = int(oplist[0].op_str, 16)
    next_vaddr = oplist[1].address
    return call_vaddr, next_vaddr 

def generatecode(ehframevaddr, callvaddr):
    context.arch = 'i386'
    res = ''
    res += asm('push ebp')
    res += asm('mov ebp, esp')
    res += asm('push edi')
    res += asm('push esi')
    res += asm('push eax')
    res += asm('push ebx')
    res += asm('push ecx')
    res += asm('push edx')
    res += asm('sub esp, 0x8')
    res += asm('mov eax, 3')
    res += asm('mov ebx, 0')
    res += asm('lea ecx, [esp]')
    res += asm('mov edx, 1')
    res += asm('int 0x80')
    res += asm('add esp, 0x8')
    res += asm('pop edx')
    res += asm('pop ecx')
    res += asm('pop ebx')
    res += asm('pop eax')
    res += asm('pop esi')
    res += asm('pop edi')
    tmp = len(res)
    tmp += 5
    tmp += ehframevaddr 
    print hex(tmp)
    tmp = callvaddr - tmp 
    print hex(callvaddr)
    print hex(tmp)
    if tmp < 0:
        tmp = 0x100000000 + tmp 
    res += '\xe8' + p32(tmp)
    res += asm('leave')
    res += asm('ret')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    for ins in md.disasm(res, ehframevaddr):
        print ins.mnemonic, ins.op_str
    return res

def patch(f, elffile, shellcode, ehframevaddr, patchvaddr):
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    patchpaddr = logic2physic(elffile, patchvaddr)
    f.seek(patchpaddr)
    content = f.read(0x20)
    oplist = []
    for ins in md.disasm(content, patchvaddr):
        oplist.append(ins)
    tmp = oplist[1].address 
    tmp = ehframevaddr - tmp 
    if tmp < 0:
        tmp = 0x100000000 + tmp 
    offset = tmp 
    tmp = oplist[1].address 
    tmp = logic2physic(elffile, tmp)
    tmp = tmp - 4 
    f.seek(tmp)
    f.write(p32(offset))
    ehframepaddr = logic2physic(elffile, ehframevaddr)
    f.seek(ehframepaddr)
    f.write(shellcode)

def hook(binaryname, patchvaddr):
    os.system('cp ' + binaryname + ' ' + binaryname + '.bak')
    f = open(binaryname, 'r+w')
    elffile = ELFFile(f)
    ehframevaddr = get_ehframe_vaddr(elffile)
    calladdr, nextaddr = get_call_vaddr(f, elffile, patchvaddr)
    shellcode = generatecode(ehframevaddr, calladdr)
    patch(f, elffile, shellcode, ehframevaddr, patchvaddr)
    f.close()

if __name__ == '__main__':
    hook('test', 0x08048646)
