import docker
import json
import base64
from papaWhale import context

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

def gen_docker_manage_scripts(path, props):
    name = props["name"]
    port = props["port"]
    build_opts = [] if "build_opts" not in props.keys() else props["build_opts"]
    run_opts = [] if "run_opts" not in props.keys() else props["run_opts"]
    prefix = context.prefix

    build_sh = (
        "#!/bin/bash\n"
        "docker rmi {name}\n"
        "docker build . -t {name} "
    ).format(name=name)
    build_sh += " ".join(build_opts)

    run_sh = (
        "#!/bin/bash\n"
        "docker kill {prefix}_{name} 2>/dev/null\n"
        "docker rm {prefix}_{name} 2>/dev/null\n"
        "docker run --privileged -p {port}:31000 -dit --name {prefix}_{name} {name} "
    ).format(name=name,port=port,prefix=prefix)
    run_sh += " ".join(run_opts)

    term_sh = (
        "#!/bin/bash\n"
        "docker kill {prefix}_{name} 2>/dev/null\n"
        "docker rm {prefix}_{name} 2>/dev/null\n"
        "docker rmi {name} 2>/dev/null"
    ).format(prefix=prefix,name=name)

    with open(str(path.joinpath("build.sh")),"w") as f_buildsh:
        f_buildsh.write(build_sh)
        f_buildsh.close()
    
    with open(str(path.joinpath("run.sh")),"w") as f_runsh:
        f_runsh.write(run_sh)
        f_runsh.close()
    
    with open(str(path.joinpath("term.sh")),"w") as f_termsh:
        f_termsh.write(term_sh)
        f_termsh.close()

def gen_dockerfile(path, props):
    name = props["name"]
    arch = props["arch"]
    os = props["ver"]
    bin_name = props["bin"]
    user = "user" if "user" not in props.keys() else props["user"]
    dock_opts = None if "dock_opts" not in props.keys() else props["dock_opts"]

    dockerfile=''

    dockerfile = (
        "FROM nsjail:{os}\n"
        "RUN useradd -m -d /home/{user} -s /bin/bash -u 1000 {user}\n"
    ).format(os=os, user=user)

    if (dock_opts != None) or (arch != "x64"):
        dockerfile += "RUN apt-get update\n"
        if arch == "x86":
            dockerfile += "RUN apt-get install libc6-i386\n"
        dockerfile += "\n".join(dock_opts)
    dockerfile += "\n"

    dockerfile += (
        "COPY {bin_name} /home/{user}/{name}\n"
        "COPY flag /home/{user}/flag\n"
        "CMD su {user} -c 'nsjail -Ml --port 31000 --chroot / --user 1000 --group 1000 /home/{user}/{name}'\n"
        "EXPOSE 31000"
    ).format(bin_name=bin_name, user=user, name=name)

    with open(str(path.joinpath("Dockerfile")),"w") as f_dfile:
        f_dfile.write(dockerfile)
        f_dfile.close()