import subprocess
from papaWhale import context
from papaWhale.fsutils import backup, cleanup

def handle_error(name):
    chall_path = context.supplier.joinpath("dock_{}".format(name))
    subprocess.call(str(chall_path.joinpath("term.sh")))

    if context.backup:
        backup(chall_path)
    else:
        cleanup(chall_path)