from yta_file_downloader.utils import download_file
from yta_general.dataclasses import FileReturned
from yta_programming.output import Output
from yta_constants.file import FileType, FileParsingMethod
from typing import Union


def download_audio(
    url: str,
    output_filename: Union[str, None] = None
) -> FileReturned:
    """
    Download an audio file from the given 'url' (if valid)
    that is stored locally as the given 'output_filename'.

    This method returns an FileReturn instance to be able
    to handle the file content with the appropriate library.
    """
    # TODO: What if not able to download it (?)
    file = download_file(url, Output.get_filename(output_filename, FileType.AUDIO))

    file.parsing_method = FileParsingMethod.PYDUB_AUDIO

    return file