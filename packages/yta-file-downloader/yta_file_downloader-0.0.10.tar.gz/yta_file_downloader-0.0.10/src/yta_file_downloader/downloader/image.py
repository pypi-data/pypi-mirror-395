from yta_file_downloader.utils import download_file
from yta_general.dataclasses import FileReturned
from yta_constants.file import FileParsingMethod, FileType
from yta_programming.output import Output
from yta_validation.parameter import ParameterValidator
from yta_general_utils.url.validator import UrlValidator
from typing import Union

import requests


def download_image(
    url: str,
    output_filename: Union[str, None] = None
) -> FileReturned:
    """
    Download the image from the provided 'url' and stores it
    locally as 'output_filename' if provided, or as a
    temporary file if not.
    
    This method sends two requests. The first one is to check
    if the provided 'url' contains a valid image, and the
    second one is to download it.

    TODO: Maybe rename to 'download_with_check'.
    """
    image_extension = UrlValidator.verify_image_url(url)
    if not image_extension:
        raise Exception('Url "' + url + '" is not a valid image url.')

    image_extension = image_extension.replace('.', '')

    # TODO: Maybe we want to return the content instead of the filename
    # so, if they don't provide 'output_filename' we could return the
    # content instead, and only download it if 'output_filename' is 
    # provided (fixing it if is wrong) and return the final 
    # 'output_filename' in this last case.
    file = download_file(url, Output.get_filename(output_filename, image_extension))

    file.parsing_method = FileParsingMethod.PILLOW_IMAGE

    return file

def download_image_2(
    url: str,
    output_filename: str
) -> FileReturned:
    """
    Download the image from the provided 'url' and store it
    locally as 'output_filename'.

    This method doesn't check if the url contains a valid 
    image, so the only request done is the one which downloads
    it.

    This method returns an UnparsedFile instance to be able
    to handle the file content with the appropriate library.

    TODO: Maybe rename to 'download_without_check'.
    """
    ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
    
    output_filename = Output.get_filename(output_filename, FileType.IMAGE)

    import shutil
    
    res = requests.get(url, stream = True)

    if res.status_code == 200:
        with open(output_filename, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
    else:
        raise Exception(f'Something went wrong when trying to download the image from "{url}".')

    return FileReturned(
        content = res.raw,
        filename = None,
        output_filename = output_filename,
        type = FileType.IMAGE,
        is_parsed = False,
        parsing_method = FileParsingMethod.PILLOW_IMAGE,
        extra_args = {
            'mode': 'RGBA'
        }
    )