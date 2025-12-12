"""
Module to handle the html file that allows us using
the web navigator speech recognition system.
"""
from yta_programming_path import DevPathHandler
from yta_file import FileHandler
from yta_file_downloader import Downloader


TRANSCRIBER_HTML_FILENAME = 'index.html'
TRANSCRIBER_HTML_ABSPATH = f'{DevPathHandler.get_project_abspath()}{TRANSCRIBER_HTML_FILENAME}'

def download_web_file():
    """
    Download the html file from Google Drive if
    not available locally.
    """
    if not FileHandler.is_file(TRANSCRIBER_HTML_ABSPATH):
        # TODO: We need 'yta_google_drive_downloader' to download it
        Downloader.download_google_drive_resource(
            'https://drive.google.com/file/d/1KQs6D7Zmd2Oj7mT4JTV8S38e2ITu_gUs/view?usp=sharing',
            TRANSCRIBER_HTML_FILENAME
        )