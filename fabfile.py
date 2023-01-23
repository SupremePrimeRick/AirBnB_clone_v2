from fabric.api import *

def connect():
    env.hosts = ['ubuntu@100.26.233.107', 'ubuntu@18.204.8.41']

def prepare_webservers():
    put('0-setup_web_static.sh')
    sudo('chmod +x 0-setup_web_static.sh')
    sudo('./0-setup_web_static.sh')
