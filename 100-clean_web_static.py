#!/usr/bin/python3
'''deletes out-of-date archives, using the function do_clean'''
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['54.86.220.207', '54.175.137.217']


@runs_once
def do_pack():
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """Archives and deploys the static files to the host servers.
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False

OA
OAdef do_clean(number=0):
OA    """Deletes out-of-date archives of the static files.
    Args:
OAOA        number (Any): The number of archives to keep.
OA    """
OAOA    archives = os.listdir('versions/')
OA    archives.sort(reverse=True)
    start = int(number)
OAOA    if not start:
OAOA        start += 1
OAOA    if start < len(archives):
        archives = archives[start:]
    else:
OA        archives = []
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
OAOA    cmd_parts = [
OAOA        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
OAOA        " '/data/web_static/releases/web_static_.*'",
OAOA        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
OAOAOA    run(''.join(cmd_parts))
