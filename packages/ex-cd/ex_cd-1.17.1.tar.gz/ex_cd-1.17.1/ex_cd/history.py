import os
import re
from .common import get_gallery_one_metadata, _download_gallery_metadata_and_extract_gallery_dir
from .common import META_FOLDER

CHILD_NAME = 'child.url'


def _get_gallery_dir_by_re(url, path_re, root):
    dirname = re.findall(path_re, url)[0]
    return os.path.join(root, dirname)


def _get_gallery_dir_by_gdl(url, config, logger):
    return _download_gallery_metadata_and_extract_gallery_dir(url, config, logger)


def _get_gallery_dir(url, config, logger):
    try:
        if config['gallery-root'] and config['path-re']:
            return _get_gallery_dir_by_re(url, config['path-re'], config['gallery-root'])
    except Exception as e:
        logger.warn("Should parse by path-re and gallery-root, but error: %s" % e)
    return _get_gallery_dir_by_gdl(url, config, logger)


url2gid_re = re.compile(r"^https://e[-x]hentai.org/g/([0-9]+)/[0-9a-z]+/*$")


def _isparent(url, gallery_dir, child_url, child_gallery_dir, config, logger):
    metadata = get_gallery_one_metadata(url, gallery_dir, config, logger)
    child_metadata = get_gallery_one_metadata(child_url, child_gallery_dir, config, logger)
    return str(metadata['gid']) == re.findall(url2gid_re, child_metadata['parent'])[0]


def get_latest_url(url, config, logger):
    '''Find url of the latest child of `url`'''
    gallery_dir = _get_gallery_dir(url, config, logger)
    child_path = os.path.join(gallery_dir, META_FOLDER, CHILD_NAME)
    if not os.path.isfile(child_path):
        return url, gallery_dir
    with open(child_path, encoding='utf8') as fp:
        child_url = fp.read().strip()
        child_gallery_dir = None
        try:
            if config['gallery-root'] and config['path-re']:
                child_gallery_dir = _get_gallery_dir_by_re(child_url, config['path-re'], config['gallery-root'])
        except Exception as e:
            logger.warn("Should parse by path-re and gallery-root, but error: %s" % e)
        if not _isparent(url, gallery_dir, child_url, child_gallery_dir, config, logger):  # 交叉验证
            raise ValueError(f"{url} is not the parent of {child_url}")
        return get_latest_url(child_url, config, logger)


def _get_gallery_parent_url(url, gallery_dir, config, logger):
    metadata = get_gallery_one_metadata(url, gallery_dir, config, logger)
    if 'parent' not in metadata:
        raise ValueError(f"No 'parent' in {url}")
    return metadata['parent']


def put_history_placeholder(url, gallery_dir, config, logger):
    '''Find and tag all the parent galleries of `url`'''
    parent_url = _get_gallery_parent_url(url, gallery_dir, config, logger)
    if parent_url == '':
        return
    parent_gallery_dir = _get_gallery_dir(parent_url, config, logger)
    child_file = os.path.join(parent_gallery_dir, META_FOLDER, CHILD_NAME)
    os.makedirs(os.path.join(parent_gallery_dir, META_FOLDER), exist_ok=True)
    if os.path.isfile(child_file):
        with open(child_file, 'r', encoding='utf8') as fp:
            if url == fp.read().strip():
                return put_history_placeholder(parent_url, parent_gallery_dir, config, logger)
    with open(child_file, 'w', encoding='utf8') as fp:
        fp.write(url)
    return put_history_placeholder(parent_url, parent_gallery_dir, config, logger)
