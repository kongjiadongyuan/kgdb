# kgdb
This is my first time to write gdb plugin.  
I want to implement some small interesting scripts, and try to make it looks as professional as possible.  
So far, this project is mainly used for practicing on my own, and maybe I'll choose a suitable time to refactor it.

### FEATURES

**whereis**  
This command is to find out which part does the address belong to.  
Usage:  
&emsp;(gdb) whereis 0xffff  
&emsp;&emsp;0x7ffff77dd000-0x7ffff79c4000		/lib/x86_64-linux-gnu/libc-2.27.so

**ub**  
This is a command that can be registered to add a breakpoint at offset to a segment.  
We must instantiate it before using it.  
For Example:  
&emsp;ub('/home/user/dummy.elf')  
&emsp;This is usually defined in localinit.py at the folder where the target binary exists. (You can see localinit.py.example)  
Usage:  
&emsp;(gdb) ub 0x123

**utel**  
This is a command similar to `ub`, instantiating is also essential.  
Usage:  
&emsp;(gdb) utel 0x123

**HookPoint**  
This is a class inheriting gdb.Breakpoint, which can hook an address to do something we are interested in.  
For Example:  
```python
    def hookfunc():
        gdb.execute('p 0x1000')
    HookPoint(0xdeadbeef, hookfunc)
```