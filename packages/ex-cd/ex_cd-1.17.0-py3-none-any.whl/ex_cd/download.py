import os
import ex_cd.gallery_dl_exec as gallery_dl
from .validate import _validate_gallery, DOWNLOAD_RESUME_FILE, VALIDATE_COMPLETED_FILE
from .collect import _load_gallery_history
from .common import metadata_args, META_FOLDER, replace_site
from .history import _get_gallery_parent_url, _get_gallery_dir
from .deprecate import _deprecate_gallery_history
from .collect import _collect_gallery_history


def _gather_gallery_history(url, gallery_dir, config, logger):
    this_history = {}
    ok_file = os.path.join(gallery_dir, META_FOLDER, VALIDATE_COMPLETED_FILE)
    if not os.path.isfile(ok_file):  # if not complete
        this_history = _collect_gallery_history(gallery_dir, config, logger)  # collect existing history
    parent_url = _get_gallery_parent_url(url, gallery_dir, config, logger)
    if parent_url == '':  # if no parent
        return this_history  # just return it
    parent_gallery_dir = _get_gallery_dir(parent_url, config, logger)
    return {**this_history, **_gather_gallery_history(parent_url, parent_gallery_dir, config, logger)}


def download_gallery_history(url, gallery_dir, config, logger, history={}, depth=0):
    """Download all the history of the gallery"""
    parent_url = _get_gallery_parent_url(url, gallery_dir, config, logger)
    if parent_url == '':  # if no parent
        return _download_gallery(url, gallery_dir, config, logger, history)  # just download it
    # if has parent
    parent_gallery_dir = _get_gallery_dir(parent_url, config, logger)
    if depth >= config["depth"]:
        return _download_gallery(url, gallery_dir, config, logger,
                                 {**history, **_gather_gallery_history(parent_url, parent_gallery_dir, config, logger)})
    ok_file = os.path.join(gallery_dir, META_FOLDER, VALIDATE_COMPLETED_FILE)
    if not os.path.isfile(ok_file):  # if not complete
        history = {**history, **_collect_gallery_history(gallery_dir, config, logger)}  # collect existing history
        # in this process, the VALIDATE_COMPLETED_FILE will be placed from old history to new
        # if VALIDATE_COMPLETED_FILE is placed here, there is two condition:
        # 1. all the old gallery is downloaded
        # 2. this gallery is download by download_gallery_latest and there is old gallery not downloaded
        # both these two conditions, this gallery should not use as history
    download_gallery_history(parent_url, parent_gallery_dir, config, logger, history, depth+1)  # download parent
    _deprecate_gallery_history(parent_url, parent_gallery_dir, url, gallery_dir,
                               config, logger)  # deprecate from parent
    return _download_gallery(url, gallery_dir, config, logger, history)  # download the rest


def _download_gallery(url, gallery_dir, config, logger, history={}):
    """download by gallery_dl and validate"""
    if _validate_gallery(url, gallery_dir, config, logger):  # validate the gallery
        return  # exit
    _load_gallery_history(url, gallery_dir, config, logger, history)  # load existing history
    if _validate_gallery(url, gallery_dir, config, logger):  # validate the gallery
        return  # record that this gallery has been downloaded
    resume_url = url
    resume_file = os.path.join(gallery_dir, META_FOLDER, DOWNLOAD_RESUME_FILE)
    try:
        with open(resume_file, "r", encoding="utf8") as fp:
            resume_url = fp.readline()
    except:
        pass
    gallery_dl_exec = config["gallery-dl-exec"]
    gallery_dl_meta_args = config["gallery-dl-meta-args"]
    args = [
        *gallery_dl_exec,
        *metadata_args, *gallery_dl_meta_args, replace_site(resume_url, config)
    ]
    logger.debug(f"Exec: {args}")
    returncode = gallery_dl.main(*args)
    if _validate_gallery(url, gallery_dir, config, logger):  # validate the gallery
        return  # record that this gallery has been downloaded
    elif returncode != 0:
        raise RuntimeError(f"Download failed: {url} -> {gallery_dir}")
    else:
        raise RuntimeError(f"Download not valid: {url} -> {gallery_dir}")
