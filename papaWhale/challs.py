import os
import json
import docker
import shutil
import subprocess
from pathlib import Path
from flask import jsonify
from papaWhale.bookkeeper import caching_libs
from papaWhale.props import save_props, prepare_props, check_props, load_props
from papaWhale.context import supplier
from papaWhale.rectify import handle_error
from papaWhale.dockutils import get_chall_containers, check_port_avail,gen_dockerfile, gen_docker_manage_scripts, find_avail_port, get_port
from papaWhale.fsutils import is_dir_exist, init_chall_dir, check_chall_dir, set_chall_dir_perm, make_dist
from papaWhale.tester import do_chall_test
from common.comm import Message

SUCCESS = 200
INVALID = 400
NOT_EXIST = 404
COLLISION = 409
TEST_FAIL = 520
BUILD_FAIL = 521
RUN_FAIL = 522
INIT_FAIL = 523
SERVER_ERROR = 500

def list_challs():
    """
    Return challenge list in json form
    """

    chall_containers = get_chall_containers(filters={"status":"running"})
    challs = []

    for chall_container in chall_containers:
        challs.append({"name": chall_container.name[7:],
                       "status": chall_container.status, "port": get_port(chall_container)})

    return jsonify(challs)

def prepare_chall(chall_path, props):
    chall_type = props["chall_type"]

    if chall_type == "docker":
        gen_dockerfile(chall_path, props)
        gen_docker_manage_scripts(chall_path, props)
    else:   #Full custom
        pass

def run_chall(args):
    chall_file = args["file"]
    props_json = json.load(args["props"].stream)
    chall_type = props_json["chall_type"]
    flag = props_json["flag"]
    name = props_json["name"]
    port = props_json["port"]

    if port == "auto":
        port = find_avail_port()
    elif not check_port_avail(port):
        return Message(COLLISION, "Port number {} is already used. Please use another port.".format(port))

    if chall_type == "custom":
        chall_dir_path = supplier.joinpath("custom_"+name)
    else:
        chall_dir_path = supplier.joinpath("dock_"+name)
    
    if is_dir_exist(chall_dir_path):
        return Message(COLLISION, "{} is already registred. Please use another name.".format(name))
    
    init_chall_dir(chall_dir_path, chall_file, flag)

    if props_json != None:
        prepare_props(chall_dir_path, props_json, port)
    else:
        prepare_props(chall_dir_path, args, port)
    
    if check_props(chall_dir_path) != True:
        return Message(INVALID, "'props.json' is malformed. Run with '--backup' and check 'props.json'")
    
    props = load_props(chall_dir_path)
    make_dist(chall_dir_path, props)

    if not check_chall_dir(chall_dir_path, props):
        return Message(INVALID, "'chall.zip' is invalid. Read the docs.")
    else:
        chall_dir_path.joinpath("chall.zip").unlink()
    
    prepare_chall(chall_dir_path, props)
    set_chall_dir_perm(chall_dir_path, props)


    if chall_type == "docker" or chall_type == "custom_dock":
        err = run_docker_chall(chall_dir_path, props)
        if err == BUILD_FAIL:
            handle_error(name)
            return Message(BUILD_FAIL, "Failed to build docker image.")
        elif err == RUN_FAIL:
            handle_error(name)
            return Message(RUN_FAIL, "Failed to run challenge.")
    elif chall_type == "custom":
        pass
    else:
        handle_error(name)
        return Message(INVALID, "Request is invalid.")

    if do_chall_test(chall_dir_path, props):
        if "libs" in props.keys():
            lib_hashes = caching_libs(chall_dir_path, props)
            return Message(
                SUCCESS, 
                "Challenge '{name}' is now running on {port}".format(name=name,port=port),
                port,
                lib_hashes
            )
        else:
            return Message(SUCCESS, "Challenge '{name}' is now running on {port}".format(name=name,port=port),port)
    else:
        handle_error(name)
        return Message(TEST_FAIL, "Run challenge is failed. Something wrong on your chall files or test file")

def run_docker_chall(chall_dir_path, props):
    if subprocess.call(str(chall_dir_path.joinpath("build.sh")), cwd=str(chall_dir_path)):
        return BUILD_FAIL
    if subprocess.call(str(chall_dir_path.joinpath("run.sh")), cwd=str(chall_dir_path)):
        return RUN_FAIL
    
def run_custom_chall(chall_dir_path, props):
    pass

def restart_challs(name):
    """
    Restart challenge 'name'

    Parameters:
        name (str): challenge's name. It must not include prefix 'cappit_'.
    Returns:
        msg (str): Success/error log.
    """
    chall_path = supplier.joinpath("dock_{}".format(name))

    challs = get_chall_containers()
    names = [chall.name[7:] for chall in challs]  # discard 'cappit_' prefix

    if name in names:
        if not subprocess.call(str(chall_path.joinpath("run.sh"))):
            return Message(SUCCESS,"Restart {} succeed.".format(name))
        else:
            return Message(SERVER_ERROR,"Restart {} failed. You need to report server manager.".format(name))
    else:
        return Message(NOT_EXIST,"Challenge {} is not exist.".format(name))

def terminate_challs(name):
    """
    Terminate challenge 'name'

    Parameters:
        name (str): challenge's name. It must not include prefix 'cappit_'.
    Returns:
        msg (str): Success/error log.
    """
    chall_path = supplier.joinpath("dock_{}".format(name))

    challs = get_chall_containers()
    names = [chall.name[7:] for chall in challs]  # discard 'cappit_' prefix

    if name in names:
        if not subprocess.call(str(chall_path.joinpath("term.sh"))):
            shutil.rmtree(str(chall_path))
            return Message(SUCCESS,"Terminate {} succeed.".format(name))
        else:
            return Message(SERVER_ERROR,"Terminate {} failed. You need to report server manager.".format(name))
    else:
        return Message(NOT_EXIST,"Challenge {} is not exist.".format(name))