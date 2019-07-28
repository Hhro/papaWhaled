import docker
import json

get_port = lambda c : c.ports['31000/tcp'][0]['HostPort']
check_port_avail = lambda p : p not in get_used_ports()

def get_chall_containers(filters=None):
    """
    Retrieve containers where challenges are running on.
    If filters is set, it would apply it.

    Parameters:
        filters (dict): filters to apply. https://docker-py.readthedocs.io/en/stable/containers.html
    
    Return:
        chall_containers (list): return containers where challenges are running on.    
    """

    client = docker.from_env()

    chall_containers = []
    for container in client.containers.list(all=True, filters=filters):
        if container.name.startswith('cappit'):
            chall_containers.append(container)

    return chall_containers

def get_used_ports():
    containers = get_chall_containers(filters={"status":"running"})
    ports =[]
    
    for container in containers:
        ports.append(get_port(container))

    return sorted(ports)

def find_avail_port():
    ports = get_used_ports()

    for port in range(31000,32000):
        if str(port) not in ports:
            break

    return str(port)

def gen_dockerfile(path,name,port,arch,ver):
    props = {}
    dockerfile=''
    run_sh=''
    build_sh=''
    term_sh=''

    with open(str(path.joinpath("props.json"))) as props_json:
        props = json.load(props_json)
        chall_bin = props["bin"]

    dockerfile = (
        "FROM nsjail:{}\n"
        "RUN useradd -m -d /home/user -s /bin/bash -u 1000 user\n"
        ).format(ver)
    if arch=="x86":
        dockerfile += (
            "RUN apt-get update\n"
            "RUN apt-get install libc6-i386\n"
        )
    dockerfile += (
    "COPY {} /home/user/{}\n"
    "COPY flag /home/user/flag\n"
    "CMD su user -c 'nsjail -Ml --port 31000 --chroot / --user 1000 --group 1000 /home/user/{}'\n"
    "EXPOSE 31000"
    ).format(chall_bin,chall_bin,chall_bin)

    build_sh = (
    "#!/bin/bash\n"
    "docker rmi {}\n"
    "docker build . -t {}"
    ).format(name,name)

    run_sh = (
    "#!/bin/bash\n"
    "docker kill cappit_{} 2>/dev/null\n"
    "docker rm cappit_{} 2>/dev/null\n"
    "docker run --privileged -p {}:31000 -dit --name cappit_{} {}"
    ).format(name,name,port,name,name)

    term_sh = (
    "#!/bin/bash\n"
    "docker kill cappit_{} 2>/dev/null\n"
    "docker rm cappit_{} 2>/dev/null\n"
    "docker rmi {} 2>/dev/null"
    ).format(name,name,name)

    with open(str(path.joinpath("Dockerfile")),"w") as f_dfile:
        f_dfile.write(dockerfile)
        f_dfile.close()

    with open(str(path.joinpath("build.sh")),"w") as f_buildsh:
        f_buildsh.write(build_sh)
        f_buildsh.close()
    
    with open(str(path.joinpath("run.sh")),"w") as f_runsh:
        f_runsh.write(run_sh)
        f_runsh.close()
    
    with open(str(path.joinpath("term.sh")),"w") as f_termsh:
        f_termsh.write(term_sh)
        f_termsh.close()
    

