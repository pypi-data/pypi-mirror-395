import json
from .config import build_parser
from .delete import delete_gallery_history
from .latest_meta import get_latest_gallery_metadata
from ..history import put_history_placeholder
from ..config import read_config
from ..output import initialize_logging


def main():
    parser = build_parser()
    args = parser.parse_args()
    logger = initialize_logging(args.loglevel)
    config = read_config(args, logger)
    logger.info(f"Parsed config: {args}")

    if args.command == "delete":
        delete_gallery_history(args.url, config, logger)

    elif args.command == "latest-meta":
        latest_url, gallery_dir, metadata = get_latest_gallery_metadata(args.url, config, logger)
        put_history_placeholder(latest_url, gallery_dir, config, logger)
        output = json.dumps(metadata, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf8") as fp:
                fp.write(output)
            logger.info(f"Metadata saved to {args.output}")
        else:
            print(output)
