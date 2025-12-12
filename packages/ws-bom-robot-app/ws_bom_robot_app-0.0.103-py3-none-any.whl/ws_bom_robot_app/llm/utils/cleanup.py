import os, logging
from ws_bom_robot_app.config import config
from datetime import datetime, timedelta

def _cleanup_data_file(folders: list[str], retention: float) -> dict:
    """
    clean up old data files in the specified folder

    Returns:
    - Dictionary with cleanup statistics
    """
    _deleted_files = []
    _deleted_dirs = []
    _freed_space = 0

    for folder in folders:
        if not os.path.exists(folder):
            logging.warning(f"Folder does not exist: {folder}")
            continue

        # delete old files
        for root, dirs, files in os.walk(folder, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_stat = os.stat(file_path)
                    file_creation_time = datetime.fromtimestamp(file_stat.st_mtime)
                    if file_creation_time < datetime.now() - timedelta(days=retention):
                        _freed_space += file_stat.st_size
                        os.remove(file_path)
                        _deleted_files.append(file_path)
                except (OSError, IOError) as e:
                    logging.error(f"Error deleting file {file_path}: {e}")

        # clean up empty directories (bottom-up)
        for root, dirs, files in os.walk(folder, topdown=False):
            # skip the root folder itself
            if root == folder:
                continue
            try:
                # check if directory is empty
                if not os.listdir(root):
                    os.rmdir(root)
                    _deleted_dirs.append(root)
            except OSError as e:
                logging.debug(f"Could not remove directory {root}: {e}")
    logging.info(f"Deleted {len(_deleted_files)} files; Freed space: {_freed_space / (1024 * 1024):.2f} MB")

    return {
        "deleted_files_count": len(_deleted_files),
        "deleted_dirs_count": len(_deleted_dirs),
        "freed_space_mb": _freed_space / (1024 * 1024)
    }

def kb_cleanup_data_file() -> dict:
    """
    clean up vector db data files
    """

    folders = [
        os.path.join(config.robot_data_folder, config.robot_data_db_folder, config.robot_data_db_folder_out),
        os.path.join(config.robot_data_folder, config.robot_data_db_folder, config.robot_data_db_folder_store),
        os.path.join(config.robot_data_folder, config.robot_data_db_folder, config.robot_data_db_folder_src)
    ]
    return _cleanup_data_file(folders, config.robot_data_db_retention_days)

def chat_cleanup_attachment() -> dict:
    """
    clean up chat attachment files
    """
    folders = [
        os.path.join(config.robot_data_folder, config.robot_data_attachment_folder)
        ]
    return _cleanup_data_file(folders, config.robot_data_attachment_retention_days)

def task_cleanup_history() -> None:
    """
    clean up task queue
    """
    from ws_bom_robot_app.task_manager import task_manager
    task_manager.cleanup_task()
