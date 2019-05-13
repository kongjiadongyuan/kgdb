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