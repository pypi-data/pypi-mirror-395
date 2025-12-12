"""File manager"""
import inspect
import os
from pathlib import Path
import json
from platformdirs import user_config_dir

current_frame = inspect.currentframe()
if current_frame is None:
    raise RuntimeError("Unable to get current frame")

this_file_path = inspect.getfile(current_frame)
this_file_dir = os.path.dirname(os.path.abspath(this_file_path))

DEFAULT_USER_CONFIG_PATH = Path(user_config_dir('pcss_qapi'))

API_KEY_FILE_NAME = 'pcss-apikey.json'

TASK_SAVE_FOLDER = 'jobs'


class FSManager:
    """File related functions"""
    @staticmethod
    def update_credentials(
        connection_hash: str,
        credentials: dict[str, str]
    ):
        """Add or update credentials for connection with a given hash"""
        filepath = os.path.join(FSManager.get_storage_path(), API_KEY_FILE_NAME)
        data = {}
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='UTF-8') as f:
                data = json.loads(f.read())
        data[connection_hash] = credentials
        with open(filepath, 'w+', encoding='UTF-8') as f:
            f.write(json.dumps(data))

    @staticmethod
    def remove_credentials(connection_hash: str):
        """Remove credentials for a given connection hash"""
        filepath = os.path.join(FSManager.get_storage_path(), API_KEY_FILE_NAME)
        if not os.path.exists(filepath):
            return
        data = {}
        with open(filepath, 'r', encoding='UTF-8') as f:
            data: dict = json.loads(f.read())
        data.pop(connection_hash, 0)
        with open(filepath, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(data))

    @staticmethod
    def get_fixed_path(storage_location: str | Path) -> Path:
        """Resolve common path quirks"""
        return (Path(storage_location) if isinstance(storage_location, str) else storage_location).expanduser().resolve()

    @staticmethod
    def get_storage_path():
        """Get storage path of the auth token and job metadata"""
        os.makedirs(FSManager.get_fixed_path(DEFAULT_USER_CONFIG_PATH), exist_ok=True)
        return str(FSManager.get_fixed_path(DEFAULT_USER_CONFIG_PATH))

    @staticmethod
    def get_task_directory(task_type: str):
        """Get directory of job metadata for a specific task type"""
        return os.path.join(FSManager.get_storage_path(), TASK_SAVE_FOLDER, task_type)
