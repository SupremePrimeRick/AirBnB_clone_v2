#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from contents of web_static"""
from fabric.api import local, env, put, run, runs_once, sudo
from datetime import datetime
import os

env.hosts = ['ubuntu@100.26.233.107', 'ubuntu@18.204.8.41']


@runs_once
def do_pack():
    """creates a tar file"""
    local("mkdir -p versions")
    path = ("versions/web_static_{}.tgz".format(
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))
    result = local("tar -cvzf {} web_static".format(path))

    if result.failed:
        return None
    return path


def do_deploy(archive_path):
    """Deploys static files to the host servers
    Args:
        archive_path (str): path to archived static file
    """

    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        sudo("mkdir -p {}".format(folder_path))
        sudo("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        sudo("rm -rf /tmp/{}".format(file_name))
        sudo("mv {}web_static/* {}".format(folder_path, folder_path))
        sudo("rm -rf {}web_static".format(folder_path))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {} /data/web_static/current".format(folder_path))
        print("New version is now LIVE!")
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """Archives and deploys the static files to host servers"""
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
