import os
import subprocess
import shutil
import docker
from pathlib import Path
from flask import jsonify
from .dockutils import get_chall_containers,get_port,gen_dockerfile,save_dockerfile
from .fsutils import is_dir_exist, init_chall_dir, check_chall_dir, set_chall_dir_perm
from .tester import do_chall_test
from common.comm import Message

SUPPLIER_PATH = os.environ["SUPPLIER"]
SUCCESS = 200
INVALID = 400
NOT_EXIST = 404
COLLISION = 409
TEST_FAIL = 520
BUILD_FAIL = 521
RUN_FAIL = 522
SERVER_ERROR = 500

def list_challs():
    """
    Return challenge list in json form
    """

    chall_containers = get_chall_containers(filters={"status":"running"})
    challs = []

    for chall_container in chall_containers:
        challs.append({"name": chall_container.name,
                       "status": chall_container.status, "port": get_port(chall_container)})

    return jsonify(challs)

def run_auto_chall(name,port,arch,ver,chal_file,flag):
    chal_dir_path = Path(SUPPLIER_PATH).joinpath("dock_"+name)

    if is_dir_exist(chal_dir_path):
        return Message(COLLISION, "{} is already registred. Please use another name.".format(name))

    init_chall_dir(chal_dir_path,chal_file,flag)
    if not check_chall_dir(chal_dir_path,"auto"):
        return Message(INVALID, "Request is invalid. Check your chall.zip again please.")
    
    gen_dockerfile(chal_dir_path,name,port,arch,ver)
    set_chall_dir_perm(chal_dir_path)

    if subprocess.call(str(chal_dir_path.joinpath("build.sh")),cwd=str(chal_dir_path)):
        return Message(BUILD_FAIL, "Build dockerfile is failed.")
    if subprocess.call(str(chal_dir_path.joinpath("run.sh")),cwd=str(chal_dir_path)):
        return Message(RUN_FAIL, "Run container is failed.")
    
    if do_chall_test(chal_dir_path,port,flag):
        return Message(SUCCESS, "Challenge '{}' is now running on {}".format(name,port),port)
    else:
        return Message(TEST_FAIL, "Run challenge is failed. Something wrong on your chall files or test file")

def run_cdock_chall(name,port,chal_file,dockerfile,flag):
    chal_dir_path = Path(SUPPLIER_PATH).joinpath("dock_"+name)

    if is_dir_exist(chal_dir_path):
        return Message(COLLISION, "{} is already registred. Please use another name.".format(name))

    init_chall_dir(chal_dir_path,chal_file,flag)
    if not check_chall_dir(chal_dir_path,"cdock"):
        return Message(INVALID, "Request is invalid. Check your chall.zip again please.")
    
    save_dockerfile(name,port,chal_dir_path,dockerfile)
    set_chall_dir_perm(chal_dir_path)

    if subprocess.call(str(chal_dir_path.joinpath("build.sh")),cwd=str(chal_dir_path)):
        return Message(BUILD_FAIL, "Build dockerfile is failed.")
    if subprocess.call(str(chal_dir_path.joinpath("run.sh")),cwd=str(chal_dir_path)):
        return Message(RUN_FAIL, "Run container is failed.")
    
    if do_chall_test(chal_dir_path,port,flag):
        return Message(SUCCESS, "Challenge '{}' is now running on {}".format(name,port),port)
    else:
        return Message(TEST_FAIL, "Run challenge is failed. Something wrong on your chall files or test file")

#TODO
def run_custom_chall(name,port,run_sh,stop_sh,chal_file):
    pass

def restart_challs(name):
    """
    Restart challenge 'name'

    Parameters:
        name (str): challenge's name. It must not include prefix 'cappit_'.
    Returns:
        msg (str): Success/error log.
    """
    chall_path = Path(SUPPLIER_PATH+"dock_{}".format(name))

    challs = get_chall_containers()
    names = [chall.name[7:] for chall in challs]  # discard 'cappit_' prefix

    if name in names:
        if not subprocess.call(str(chall_path.joinpath("run.sh")), shell=True):
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
    chall_path = Path(SUPPLIER_PATH+"dock_{}".format(name))

    challs = get_chall_containers()
    names = [chall.name[7:] for chall in challs]  # discard 'cappit_' prefix

    if name in names:
        if not subprocess.call(str(chall_path.joinpath("term.sh")), shell=True):
            shutil.rmtree(str(chall_path))
            return Message(SUCCESS,"Terminate {} succeed.".format(name))
        else:
            return Message(SERVER_ERROR,"Terminate {} failed. You need to report server manager.".format(name))
    else:
        return Message(NOT_EXIST,"Challenge {} is not exist.".format(name))