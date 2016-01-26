#!/usr/bin/env python
import logging
import os

from sftp_server.sftp import SFTPServer
from sftp_server.permissions_manager import PermissionsManager
from sftp_server.permissions_file import read_permissions_file

logger = logging.getLogger(__name__)


SSH_PORT = 2222

development_root = os.path.join(os.path.dirname(__file__), 'tmp')
FILE_ROOT = os.path.realpath(os.environ.get('FILESERVER_ROOT', development_root))
# Note, you can generate a new host key like this:
# ssh-keygen -t rsa -N '' -f host_key
HOST_KEY = os.path.join(os.path.dirname(__file__), 'config/host_key')
PERMISSIONS_FILE = os.path.join(os.path.dirname(__file__), 'config/permissions.ini')


def auth(username, password):
    logger.info('authed with: %s / pw: %s', username, password)
    return ['superusers']


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    permissions = read_permissions_file(PERMISSIONS_FILE)
    manager = PermissionsManager(permissions, authenticate=auth)
    server = SFTPServer(FILE_ROOT, HOST_KEY, get_user=manager.get_user)
    server.serve_forever('0.0.0.0', SSH_PORT)
