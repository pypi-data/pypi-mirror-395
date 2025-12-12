import subprocess


def main(*args):
    return subprocess.Popen(args=args).wait()


if __name__ == "__main__":
    import sys
    import os
    os.chdir(os.path.dirname(os.path.dirname(sys.argv[0])))
    main(
        sys.executable, "-m", "gallery_dl",
        "--no-download",
        "--write-metadata",
        "--postprocessor-option", 'directory=metadata',
        '-v',
        '--sleep-request', '1',
        '-c', '.vscode/gallery-dl.config.json',
        'https://exhentai.org/g/2752577/8ffd3778cb/'
    )
