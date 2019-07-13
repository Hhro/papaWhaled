import os
import subprocess
import docker
from flask import jsonify
from .utils import get_chall_containers,get_port

SUPPLIER_PATH = os.environ["SUPPLIER"]
SUCCESS = 200
NOT_EXIST = 404
SERVER_ERROR = 500

def list_challs():
    """
    Return challenge list in json form
    """

    chall_containers = get_chall_containers()
    challs = []

    for chall_container in chall_containers:
        challs.append({"name": chall_container.name,
                       "status": chall_container.status, "port": get_port(chall_container)})

    return jsonify(challs)


def restart_challs(name):
    """
    Restart challenge 'name'

    Parameters:
        name (str): challenge's name. It must not include prefix 'cappit_'.
    Returns:
        msg (str): Success/error log.
    """

    challs = get_chall_containers()
    names = [chall.name[7:] for chall in challs]  # discard 'cappit_' prefix

    if name in names:
        if not subprocess.call(SUPPLIER_PATH+"dock_{}/run.sh".format(name), shell=True):
            return SUCCESS
        else:
            return SERVER_ERROR
    else:
        return NOT_EXIST
