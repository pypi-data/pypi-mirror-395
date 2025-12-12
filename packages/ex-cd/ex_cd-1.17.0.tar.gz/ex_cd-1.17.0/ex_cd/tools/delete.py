import os
import shutil
from ..common import META_FOLDER
from ..meta import META_VALIDATE_COMPLETED_FILE, META_DOWNLOAD_RESUME_FILE
from ..validate import VALIDATE_COMPLETED_FILE, DOWNLOAD_RESUME_FILE
from ..deprecate import DEPRECAT_COMPLETED_FILE
from ..history import get_latest_url, put_history_placeholder, _get_gallery_dir, _get_gallery_parent_url


def _get_all_history_dirs(url, gallery_dir, config, logger):
    """Get all gallery directories in the history chain, from newest to oldest"""
    dirs = [(url, gallery_dir)]
    try:
        parent_url = _get_gallery_parent_url(url, gallery_dir, config, logger)
    except Exception as e:
        logger.debug(f"No parent for {url}: {e}")
        return dirs
    while parent_url:
        parent_gallery_dir = _get_gallery_dir(parent_url, config, logger)
        dirs.append((parent_url, parent_gallery_dir))
        try:
            parent_url = _get_gallery_parent_url(parent_url, parent_gallery_dir, config, logger)
        except Exception:
            break
    return dirs


def _delete_gallery_content(gallery_dir, logger):
    """Delete all content from a gallery in a resumable way"""
    meta_folder = os.path.join(gallery_dir, META_FOLDER)

    # Step 1: Delete download completion markers
    for marker in [VALIDATE_COMPLETED_FILE, DOWNLOAD_RESUME_FILE, DEPRECAT_COMPLETED_FILE]:
        marker_path = os.path.join(meta_folder, marker)
        if os.path.isfile(marker_path):
            os.remove(marker_path)
            logger.debug(f"Deleted marker: {marker_path}")

    # Step 2: Delete all files outside .metadata (images)
    if os.path.isdir(gallery_dir):
        for item in os.listdir(gallery_dir):
            if item == META_FOLDER:
                continue
            item_path = os.path.join(gallery_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                logger.debug(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logger.debug(f"Deleted dir: {item_path}")

    # Step 3: Delete meta completion markers
    for marker in [META_VALIDATE_COMPLETED_FILE, META_DOWNLOAD_RESUME_FILE]:
        marker_path = os.path.join(meta_folder, marker)
        if os.path.isfile(marker_path):
            os.remove(marker_path)
            logger.debug(f"Deleted meta marker: {marker_path}")

    # Step 4: Delete JSON files in .metadata
    if os.path.isdir(meta_folder):
        for item in os.listdir(meta_folder):
            if item.endswith('.json'):
                item_path = os.path.join(meta_folder, item)
                os.remove(item_path)
                logger.debug(f"Deleted json: {item_path}")

    # Step 5: Delete remaining files in .metadata (like child.url)
    if os.path.isdir(meta_folder):
        for item in os.listdir(meta_folder):
            item_path = os.path.join(meta_folder, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                logger.debug(f"Deleted remaining: {item_path}")

    # Step 6: Delete the .metadata folder
    if os.path.isdir(meta_folder):
        try:
            os.rmdir(meta_folder)
        except OSError:
            shutil.rmtree(meta_folder)
        logger.debug(f"Deleted metadata folder: {meta_folder}")

    # Step 7: Delete the gallery folder itself
    if os.path.isdir(gallery_dir):
        try:
            os.rmdir(gallery_dir)
        except OSError:
            shutil.rmtree(gallery_dir)
        logger.debug(f"Deleted gallery folder: {gallery_dir}")


def delete_gallery_history(url, config, logger):
    """Delete all history of a gallery

    Args:
        url: URL of the gallery (can be any version in the history chain)
        config: Configuration dict
        logger: Logger instance
    """
    # Step 1: Get the latest URL and create placeholder chain
    url, gallery_dir = get_latest_url(url, config, logger)
    logger.info(f"Latest gallery: {url} -> {gallery_dir}")
    put_history_placeholder(url, gallery_dir, config, logger)

    # Step 2: Collect all gallery directories (newest to oldest)
    all_dirs = _get_all_history_dirs(url, gallery_dir, config, logger)
    logger.info(f"Found {len(all_dirs)} galleries to delete:")
    for i, (dir_url, dir_path) in enumerate(all_dirs):
        logger.info(f"  [{i+1}] {dir_path}")

    # Step 3: Delete from newest to oldest
    for dir_url, dir_path in all_dirs:
        if os.path.isdir(dir_path):
            logger.info(f"Deleting: {dir_path}")
            _delete_gallery_content(dir_path, logger)
        else:
            logger.debug(f"Already deleted: {dir_path}")

    logger.info("Delete completed")
