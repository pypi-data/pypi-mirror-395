import functools
import os

import pcss_qapi.utils.fs_manager as fs_manager
from pcss_qapi.auth.auth_service import AuthorizationService


def del_non_empty(path):
    for file in os.listdir(path):
        file = os.path.join(path, file)
        if os.path.isdir(file):
            del_non_empty(file)
        else:
            os.remove(file)

    os.rmdir(path)


def inject_conf(func):
    """
    Change default storage conf file location so tests don't
    change .conf/api_configuration.json as it must remain the same
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        storage_dir = os.path.join(os.getcwd(), 'dummy_key')
        cache = fs_manager.DEFAULT_USER_CONFIG_PATH
        fs_manager.DEFAULT_USER_CONFIG_PATH = storage_dir
        try:
            func(*args, **kwargs)
        finally:
            AuthorizationService.logout()
            if os.path.exists(storage_dir):
                del_non_empty(storage_dir)
            fs_manager.DEFAULT_USER_CONFIG_PATH = cache

    return wrapper
