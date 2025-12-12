import os
import re
import json
import ex_cd.gallery_dl_exec as gallery_dl
from .common import META_FOLDER, metadata_args, _get_gallery_metadata_filenames, get_gallery_one_metadata, replace_site


META_DOWNLOAD_RESUME_FILE = 'MetaDownloadResume'


def _download_gallery_meta(url, gallery_dir, config, logger):
    """download gallery metadata by gallery_dl"""
    if _valid_gallery_meta(url, gallery_dir, config, logger):  # validate the gallery
        return  # exit
    resume_url = url
    resume_file = os.path.join(gallery_dir, META_FOLDER, META_DOWNLOAD_RESUME_FILE)
    try:
        with open(resume_file, "r", encoding="utf8") as fp:
            resume_url = fp.readline()
    except:
        pass
    gallery_dl_exec = config["gallery-dl-exec"]
    gallery_dl_meta_args = config["gallery-dl-meta-args"]
    args = [
        *gallery_dl_exec, "--no-download", "--no-skip",
        *metadata_args, *gallery_dl_meta_args, replace_site(resume_url, config)
    ]
    logger.debug(f"Exec: {args}")
    returncode = gallery_dl.main(*args)
    if _valid_gallery_meta(url, gallery_dir, config, logger):  # validate the gallery
        return  # record that this gallery has been downloaded
    elif returncode != 0:
        raise RuntimeError(f"Download gallery meta failed: {url} -> {gallery_dir}")
    else:
        raise RuntimeError(f"Download gallery meta invalid: {url} -> {gallery_dir}")


url2gid_re = re.compile(r"^https://e[-x]hentai.org/g/([0-9]+)/[0-9a-z]+/*$")


def _url2gid_by_re(url):
    return re.findall(url2gid_re, url)[0]


url2site_re = re.compile(r"(^https://e[-x]hentai.org)/g/[0-9]+/[0-9a-z]+/*$")


def _url2site_by_re(url):
    return re.findall(url2site_re, url)[0]


def _get_image_tokens(url, gallery_dir, config, logger):
    # check if has enough metadata json files
    meta = get_gallery_one_metadata(url, gallery_dir, config, logger)
    if 'filecount' not in meta:
        raise ValueError(f"'filecount' not in metadata")
    metafilenames = [None] * int(meta['filecount'])
    image_tokens = [None] * int(meta['filecount'])
    should_deletes = [[] for _ in range(int(meta['filecount']))]
    site, gid = _url2site_by_re(url), _url2gid_by_re(url)
    for metafilename in _get_gallery_metadata_filenames(gallery_dir):
        metafile = os.path.join(gallery_dir, META_FOLDER, metafilename)
        try:
            with open(metafile, "r", encoding="utf8") as fp:
                meta = json.load(fp)
                if str(meta["gid"]) == gid:
                    num = meta["num"] - 1
                    # sometimes there are deperated metafiles
                    if metafilenames[num] is not None:
                        should_deletes[num].append(metafilenames[num])
                        should_deletes[num].append(metafilename)
                        image_tokens[num] = metafilenames[num] = None
                    elif len(should_deletes[num]) > 0:
                        should_deletes[num].append(metafilename)
                    else:
                        image_tokens[num] = meta["image_token"]
                        metafilenames[num] = metafilename
        except Exception as e:
            logger.error(f"Invalid metadata {metafile}: {e}")
    # delete deperated metafiles
    n = 0
    for should_delete in should_deletes:
        for delete in should_delete:
            metafile = os.path.join(gallery_dir, META_FOLDER, delete)
            if os.path.exists(metafile):
                os.remove(metafile)
            n += 1
    if n > 0:
        completefile = os.path.join(gallery_dir, META_FOLDER, META_VALIDATE_COMPLETED_FILE)
        if os.path.exists(completefile):
            os.remove(completefile)
        raise ValueError(f"There are {n} deperated metafiles! just deleted! should restart meta doanload!")
    return site, gid, image_tokens, metafilenames


META_VALIDATE_COMPLETED_FILE = 'MetaValidateCompleted'


def _valid_gallery_meta(url, gallery_dir, config, logger):
    """validate the gallery metadata"""
    ok_file = os.path.join(gallery_dir, META_FOLDER, META_VALIDATE_COMPLETED_FILE)
    if os.path.isfile(ok_file):  # if valid
        return True  # exit
    # check if has enough metadata json files
    resume_url = url
    try:
        site, gid, image_tokens, _ = _get_image_tokens(url, gallery_dir, config, logger)
        for i, image_token in enumerate(image_tokens):
            if image_token:
                resume_url = f"{site}/s/{image_token}/{gid}-{i+1}"
            else:
                break
        if None in image_tokens:
            resume_file = os.path.join(gallery_dir, META_FOLDER, META_DOWNLOAD_RESUME_FILE)
            with open(resume_file, "w", encoding='utf8') as fp:
                fp.write(resume_url)
                logger.error(f"Invalid {gallery_dir}: no enough metadata files, should resume from {resume_url}")
            return False
    except Exception as e:
        logger.error(f"Invalid {gallery_dir}: {e}")

    with open(ok_file, "w", encoding='utf8'):
        return True  # record that this gallery has been validated
