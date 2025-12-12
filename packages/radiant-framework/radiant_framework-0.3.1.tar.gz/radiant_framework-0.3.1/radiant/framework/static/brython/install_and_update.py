import subprocess
import shutil
import os


def dist_name():
    command = ["brython-cli", "--version"]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip().replace(" version ", "-")
    return output


def run_command_on_dir(command, dir_name):
    os.chdir(dir_name)
    subprocess.run(command)
    os.chdir("..")


dir_name = dist_name()

if not os.path.exists(dir_name):
    os.mkdir(dir_name)

    run_command_on_dir(
        [
            "brython-cli",
            "--install",
        ],
        dir_name,
    )
dir_name = "Brython-latest"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

    run_command_on_dir(
        [
            "brython-cli",
            "--install",
        ],
        dir_name,
    )

else:
    run_command_on_dir(
        [
            "brython-cli",
            "--update",
        ],
        dir_name,
    )
