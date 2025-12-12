from yta_file_downloader.utils import download_file
from yta_general.dataclasses import FileReturned
from yta_constants.file import FileParsingMethod, FileType
from yta_programming.output import Output
from typing import Union


def download_video(
    url: str,
    output_filename: Union[str, None] = None
) -> FileReturned:
    """
    Download the video from the given 'url' (if valid) and
    store it locally as 'output_filename' if provided.
    """
    file = download_file(url, Output.get_filename(output_filename, FileType.VIDEO))

    file.parsing_method = FileParsingMethod.MOVIEPY_VIDEO

    return file