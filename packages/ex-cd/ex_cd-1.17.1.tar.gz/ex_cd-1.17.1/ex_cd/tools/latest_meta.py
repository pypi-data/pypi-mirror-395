from ..common import get_gallery_one_metadata
from ..history import get_latest_url


def get_latest_gallery_metadata(url, config, logger):
    """Get metadata of the latest version of a gallery

    Args:
        url: URL of the gallery (can be any version in the history chain)
        config: Configuration dict
        logger: Logger instance

    Returns:
        tuple: (latest_url, gallery_dir, metadata)
    """
    # Step 1: Get the latest URL
    latest_url, gallery_dir = get_latest_url(url, config, logger)
    logger.info(f"Latest gallery: {latest_url} -> {gallery_dir}")

    # Step 2: Get metadata
    metadata = get_gallery_one_metadata(latest_url, gallery_dir, config, logger)
    logger.info(f"Got metadata for gid={metadata.get('gid')}, title={metadata.get('title')}")

    return latest_url, gallery_dir, metadata
