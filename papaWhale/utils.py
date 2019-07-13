import docker

get_port = lambda c : c.ports['31000/tcp'][0]['HostPort']

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