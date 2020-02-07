# Deploy options

To deal with many kind of challenge dependencies, papaWhaled supports variety of deployment options.

**Contents**

---

### 1. chall_type - required str

Papawhaled is basically deploying challenge with **docker.** However some challenges don't need any server resources, or sometimes they can't be deployed with docker. If **chall_type** is set as `docker` then challenge would be deployed with docker, else if **chall_type** is set as `non-docker`, it would not be.

**Options**

- **docker:** Challenge would be deployed with docker.
- **non-docker:** Challenge would not be deployed with docker. (TBI)

### 2. arch - required str

Now only two architectures are supported.

**Options**

- x86: intel x86
- x64: intel x86_64

### 3. os - required str

Now only two OS are supported.

**Options**

- ub1804: Ubuntu 18.04
- ub1604: Ubuntu 16.04

### 4. name - required str

Challenge name. If it is already used, upload would be failed.

### 5. port - required str

Challenge would be run on this port.

**Options**

- auto: papaWhaled will automatically select port that is not used.
- [31000-32000]: If port is aleready in used, error occurs.

### 6. flag - required str

Solver would get this flag. 

### 7. dist - default: ["bin"] list

FIles to be distributed to challenger. Values are passed as **list**, and each element must not be file name, but key of props.json.

**ex)** 

    {
    	...
    	"dist":["bin","libs"],
    	...
    }

### 8. libs - list

If challenge has dependency on some library, you must include them with `file`, and specify their name. Values must be passed as **list.**

**ex)**

    {
    	...
    	"libs":["libc-2.27.so", "libcrypto.so"]
    	...
    }

### 9. test - default: "test.py" str

Name of test file. It must be included in `file`. It would be executed to test whether deployment is successfully done or not.

### 10. bin - default: "bin" str

`bin` would be deployed.

### 11. dock_opts - list

If challenge cannot run with default generated Dockerfile, use this option. 

Passed value would be appended at HERE:

    FROM nsjail:[os]
    RUN useradd -m -d /home/user -s /bin/bash -u 1000 user
    RUN apt-get update
    ########HERE#########
    COPY [bin] /home/[user]/[name]
    COPY flag /home/[user]/flag
    CMD su user -c 'nsjail -Ml --port 31000 --chroot / --user 1000 --group 1000 /home/user/zerotask'
    EXPOSE 3100}

**ex)**

    {
    	...
    	"dock_opts":["COPY libcrypto.so.1.0.0 /usr/lib/"],
    	...
    }

### 12. build_opts - list

Passed value would be appended at HERE:

    docker build . -t [name] #HERE#

### 13. run_opts - list

Passed value would be appended at HERE:

    docker run --privileged -p [port]:31000 -dit --name [prefix]_[name] [name] #HERE#