#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from contents of web_static"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """creates a tar file"""
    local("mkdir versions")
    path = ("versions/web_static_{}.tgz".format(
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))
    result = local("tar -cvzf {} web_static".format(path))

    if result.failed:
        return None
    return path
