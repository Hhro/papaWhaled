import json
import subprocess

def do_chall_test(chall_dir_path, props):
    test_worker = props["test"]
    port = props["port"]
    flag = props["flag"]

    if not subprocess.call(
        [str(chall_dir_path.joinpath(test_worker)),port,flag],
        cwd=str(chall_dir_path)
    ):
        return True
    else:
        return False
