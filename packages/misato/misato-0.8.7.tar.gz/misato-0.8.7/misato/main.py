import argparse
import os
import subprocess
from misato.logger import logger
from misato.config import MOVIE_SAVE_PATH_ROOT, RECORD_FILE, MAGIC_NUMBER
from misato.http_client import HttpClient
from misato.url_sources import AuthSource, SearchSource, FileSource, AutoUrlSource
from misato.video_downloader import VideoDownloader
from misato.utils import delete_all_subfolders, ThreadSafeCounter, exit_all

banner = """                                                                                                                                                                                                                 
                  ███                     █████            
                 ░░░                     ░░███             
 █████████████   ████   █████   ██████   ███████    ██████ 
░░███░░███░░███ ░░███  ███░░   ░░░░░███ ░░░███░    ███░░███
 ░███ ░███ ░███  ░███ ░░█████   ███████   ░███    ░███ ░███
 ░███ ░███ ░███  ░███  ░░░░███ ███░░███   ░███ ███░███ ░███
 █████░███ █████ █████ ██████ ░░████████  ░░█████ ░░██████ 
░░░░░ ░░░ ░░░░░ ░░░░░ ░░░░░░   ░░░░░░░░    ░░░░░   ░░░░░░                                                                                                                                                                                                                                                                                                                                   
"""


class DownloadTracker:
    def __init__(self, record_file: str):
        self.record_file = record_file
        self.downloaded_urls = set()
        if os.path.exists(record_file):
            with open(record_file, 'r', encoding='utf-8') as f:
                self.downloaded_urls.update(line.strip() for line in f)

    def is_downloaded(self, url: str) -> bool:
        return url in self.downloaded_urls

    def record_download(self, url: str) -> None:
        self.downloaded_urls.add(url)
        with open(self.record_file, 'a', encoding='utf-8') as f:
            f.write(url + '\n')


def check_ffmpeg_command(ffmpeg: bool) -> bool:
    if not ffmpeg:
        return True
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def validate_args(args):
    params = [args.auth, args.search, args.file, args.auto]
    if sum(param is not None for param in params) != 1:
        logger.error("Exactly one of -auto, -auth, -search, -file must be specified.")
        exit_all()
    if args.auth and len(args.auth) != 2:
        logger.error("Auth requires username and password.")
        exit_all()
    if not check_ffmpeg_command(args.ffmpeg) or not check_ffmpeg_command(args.ffcover):
        logger.error("FFmpeg command status error.")
        exit_all()
    for opt in ['limit', 'quality', 'retry', 'delay', 'timeout']:
        value = getattr(args, opt)
        if value and (not value.isdigit() or int(value) <= 0):
            logger.error(f"The -{opt} option must be a positive integer.")
            exit_all()
    if args.file and (not os.path.isfile(args.file) or os.path.getsize(args.file) == 0):
        logger.error("The -file option must be a valid non-empty file.")
        exit_all()


def main():
    parser = argparse.ArgumentParser(
        description='A tool for downloading videos from the "MissAV" website.\n'
                    '\n'
                    'Main Options:\n'
                    'Use the -auto   option to specify the video or playlist URLs to download. can be mixed.\n'
                    'Use the -auth   option to specify the username and password to download the videos collected by the account.\n'
                    'Use the -search option to search for movie by serial number and download it.\n'
                    'Use the -file   option to download video or playlist URLs in the file. ( Each line is a URL )\n'
                    '\n'
                    'Additional Options:\n'
                    'Use the -limit   option to limit the number of downloads. \n'
                    'Use the -proxy   option to configure http proxy server ip and port.\n'
                    'Use the -ffmpeg  option to get the best video quality. ( Recommend! )\n'
                    'Use the -cover   option to save the cover when downloading the video\n'
                    'Use the -ffcover option to set the cover as the video preview (ffmpeg required)\n'
                    'Use the -noban   option to turn off the misato banner when downloading the video\n'
                    'Use the -title   option to use the full title as the movie file name\n'
                    'Use the -quality option to specify the movie resolution (360, 480, 720, 1080...)\n'
                    'Use the -retry   option to specify the number of retries for downloading segments\n'
                    'Use the -delay   option to specify the delay before retry ( seconds )\n'
                    'Use the -timeout option to specify the timeout for segment download ( seconds )\n',
        epilog='Examples:\n'
               '  misato -auto "https://missav.ai/sw-950" "https://missav.ai/dm132/actresses/JULIA"\n'
               '  misato -auto "https://missav.ai/dm132/actresses/JULIA" -limit 20 -ffcover\n'
               '  misato -auto "https://missav.ai/sw-950" "https://missav.ai/dandy-917"\n'
               '  misato -auto "https://missav.ai/sw-950" -proxy localhost:7890\n'
               '  misato -auth misato@gmail.com misatoQAQ -ffmpeg -noban -limit 20\n'
               '  misato -file /home/misato/url.txt -ffmpeg -title -limit 20\n'
               '  misato -search sw-950 -ffcover -quality 720\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-auto', nargs='+', metavar='', help='Multiple movie and playlist URLs can be mixed. separate with spaces')
    parser.add_argument('-auth', nargs='+', metavar='', help='Username and password, separate with space')
    parser.add_argument('-limit', type=str, metavar='', help='Limit the number of downloads')
    parser.add_argument('-search', type=str, metavar='', help='Movie serial number')
    parser.add_argument('-file', type=str, metavar='', help='File path')
    parser.add_argument('-proxy', type=str, metavar='', help='HTTP(S) proxy')
    parser.add_argument('-ffmpeg', action='store_true', help='Enable ffmpeg processing')
    parser.add_argument('-cover', action='store_true', help='Download video cover')
    parser.add_argument('-ffcover', action='store_true', help='Set cover as preview (ffmpeg required)')
    parser.add_argument('-noban', action='store_true', help='Do not display the banner')
    parser.add_argument('-title', action='store_true', help='Full title as file name')
    parser.add_argument('-quality', type=str, metavar='', help='Specify the movie resolution')
    parser.add_argument('-retry', type=str, metavar='', help='Number of retries for downloading segments')
    parser.add_argument('-delay', type=str, metavar='', help='Delay in seconds before retry')
    parser.add_argument('-timeout', type=str, metavar='', help='Timeout in seconds for segment download')

    args = parser.parse_args()
    logger.info(str(args))
    validate_args(args)

    if not args.noban:
        print(banner)

    if args.ffcover:
        args.ffmpeg = True
        args.cover = True

    if args.proxy:
        logger.info("Network proxy enabled.")
        os.environ["http_proxy"] = f"http://{args.proxy}"
        os.environ["https_proxy"] = f"http://{args.proxy}"

    http_client = HttpClient()
    movie_counter = ThreadSafeCounter()
    source = (
        AutoUrlSource(movie_counter=movie_counter, auto_urls=args.auto, limit=args.limit) if args.auto else
        AuthSource(movie_counter=movie_counter, username=args.auth[0], password=args.auth[1], limit=args.limit) if args.auth else
        SearchSource(movie_counter=movie_counter, key=args.search) if args.search else
        FileSource(movie_counter=movie_counter, file_path=args.file, limit=args.limit) if args.file else None
    )
    if not source:
        logger.error("No source specified.")
        exit_all()

    movie_urls = source.get_urls()
    if not movie_urls:
        logger.error("No URLs to download.")
        exit_all()

    download_tracker = DownloadTracker(RECORD_FILE)
    options = {
        'download_action': True,
        'write_action': True,
        'ffmpeg_action': args.ffmpeg,
        'num_threads': os.cpu_count(),
        'cover_action': args.cover,
        'title_action': args.title,
        'cover_as_preview': args.ffcover,
        'quality': int(args.quality) if args.quality else None,
        'retry': int(args.retry) if args.retry else 5,
        'delay': int(args.delay) if args.delay else 2,
        'timeout': int(args.timeout) if args.timeout else 10
    }

    for url in movie_urls:
        if download_tracker.is_downloaded(url):
            logger.info(f"{url} already downloaded, skipping.")
            continue
        delete_all_subfolders(MOVIE_SAVE_PATH_ROOT)
        try:
            logger.info(f"Processing URL: {url}")
            downloader = VideoDownloader(url, http_client, options)
            downloader.download()
            download_tracker.record_download(url)
            logger.info(f"Processing URL Complete: {url}")
            print()
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
        delete_all_subfolders(MOVIE_SAVE_PATH_ROOT)


if __name__ == "__main__":
    main()
