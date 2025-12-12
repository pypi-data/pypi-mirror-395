import os
import json
from .common import META_FOLDER, _get_gallery_metadata_filenames
from .validate import _validate_gallery
from .meta import _download_gallery_meta


DEPRECAT_COMPLETED_FILE = 'DeprecateCompleted'


def _deprecate_gallery_history(parent_url, parent_gallery_dir, child_url, child_gallery_dir, config, logger):
    """Move deprecated images from parent gallery to child gallery (reverse of _load_gallery_history)"""
    ok_file = os.path.join(parent_gallery_dir, META_FOLDER, DEPRECAT_COMPLETED_FILE)
    if os.path.isfile(ok_file):
        return
    if not _validate_gallery(parent_url, parent_gallery_dir, config, logger):
        raise RuntimeError(f"Cannot deprecate from a invalid gallery {parent_gallery_dir}")
    _download_gallery_meta(child_url, child_gallery_dir, config, logger)
    # move from parent_gallery_dir
    parent_metadata_files = _get_gallery_metadata_filenames(parent_gallery_dir)
    src = {}
    for metafile in parent_metadata_files:
        imgfile = metafile[0:-5]
        metapath = os.path.join(parent_gallery_dir, META_FOLDER, metafile)
        imgpath = os.path.join(parent_gallery_dir, imgfile)
        with open(metapath, 'r', encoding='utf8') as fp:
            meta = json.load(fp)
            src[meta['image_token']] = imgpath
    # move to child_gallery_dir
    child_metadata_files = _get_gallery_metadata_filenames(child_gallery_dir)
    dst = {}
    for metafile in child_metadata_files:
        imgfile = metafile[0:-5]
        metapath = os.path.join(child_gallery_dir, META_FOLDER, metafile)
        imgpath = os.path.join(child_gallery_dir, imgfile)
        with open(metapath, 'r', encoding='utf8') as fp:
            meta = json.load(fp)
            dst[meta['image_token']] = imgpath
    # move them
    for src_image_token, src_imgpath in src.items():
        if src_image_token in dst:
            os.replace(src_imgpath, dst[src_image_token])
    with open(ok_file, "w", encoding='utf8'):
        return  # record that this gallery has been validated
