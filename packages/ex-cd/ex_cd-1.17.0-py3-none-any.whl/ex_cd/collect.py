import os
import json
import hashlib
from .common import META_FOLDER, _get_gallery_metadata_filenames
from .meta import _download_gallery_meta


def _iter_metadata(gallery_dir, logger):
    meta_folder = os.path.join(gallery_dir, META_FOLDER)
    for metafile in _get_gallery_metadata_filenames(gallery_dir):
        img, meta_ext = os.path.splitext(metafile)
        if not meta_ext == '.json':
            continue
        metapath = os.path.join(meta_folder, metafile)
        try:
            with open(metapath, encoding='utf8') as fp:
                yield img, json.load(fp)
        except Exception as e:
            logger.warning(f"Cannot load exist json file {metafile}: {e}")


def _iter_imgfile_metadata(gallery_dir, logger):
    for img, meta in _iter_metadata(gallery_dir, logger):
        imgfile = os.path.join(gallery_dir, img)
        if not os.path.isfile(imgfile):
            continue
        yield imgfile, meta


def _check_img(imgfile, meta, logger):
    if 'image_token' not in meta:
        return False
    image_token = meta['image_token']
    sha1_token = None
    if not os.path.isfile(imgfile):
        return False
    try:
        with open(imgfile, mode="rb") as fp:
            sha1_token = hashlib.sha1(fp.read()).hexdigest()
    except Exception as e:
        logger.error(f"Invalid {imgfile}: cannot compute token, {e}")
        return False
    return image_token == sha1_token[0:10]


def _collect_gallery_history(gallery_dir, config, logger):
    history = {}
    for imgfile, meta in _iter_imgfile_metadata(gallery_dir, logger):
        if _check_img(imgfile, meta, logger):
            history[meta['image_token']] = imgfile
    return history


def _load_gallery_history(url, gallery_dir, config, logger, history):
    """Move deprecated images from child gallery to parent gallery"""
    _download_gallery_meta(url, gallery_dir, config, logger)
    for img, meta in _iter_metadata(gallery_dir, logger):
        if 'image_token' not in meta:
            continue
        image_token = meta['image_token']
        if image_token not in history:
            continue
        imgfile = os.path.join(gallery_dir, img)
        if _check_img(imgfile, meta, logger):
            continue
        if os.path.exists(imgfile):
            os.remove(imgfile)
        os.rename(history[image_token], imgfile)
        del history[image_token]
