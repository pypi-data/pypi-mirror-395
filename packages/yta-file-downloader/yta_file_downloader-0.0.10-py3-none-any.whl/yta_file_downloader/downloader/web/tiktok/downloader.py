
from yta_file_downloader.utils import get_file
from yta_file_downloader.downloader.web.tiktok.url_parser import TiktokUrlParser
from yta_general.dataclasses import FileReturned
from yta_validation.parameter import ParameterValidator
from yta_constants.file import FileType, FileParsingMethod
from yta_programming.output import Output
from yta_file.handler import FileHandler
from typing import Union
from io import BytesIO

import requests


def _get_tiktok_video_content(
    url: str
    # TODO: If possible, set the real return type
) -> any:
    """
    Get the Tiktok video with the given 'url' as a
    content buffer that can be written into a file
    (locally or in memory).

    For internal use only.

    This method has been found by scanning this
    platform:
    - https://tikcd.com/
    """
    ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
    
    tiktok_video_info = TiktokUrlParser.parse(url)

    # TODO: The old way is not working...
    headers = {
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'origin': 'https://tikcd.com',
        'priority': 'u=1, i',
        'referer': 'https://tikcd.com/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    }

    # We force it to be large url
    params = {
        'url': tiktok_video_info.url,
        'hd': '1',
    }

    # TODO: This method has been found using this platform
    # https://tikcd.com/?srsltid=AfmBOopX4VP6_pfbANSdRaXUfnXXDDo6zIHlzgbl_QsfBR0tmWyhXjPh
    # It seems that the old tikcdn doesn't work

    return get_file(
        requests.get(
            'https://tikwm.com/api/',
            params = params,
            headers = headers
            # TODO: I should handle this if unavailable
        ).json().get('data').get('wmplay')
    )

"""
Exposed methods below.
"""

def download_tiktok_video(
    url: str,
    output_filename: Union[str, None, bool] = None
) -> FileReturned:
    """
    Get the Tiktok video with the given 'url' as a file
    that is downloaded and stored locally with the also
    provided 'output_filename' (or a temporary one if
    not provided).
    """
    ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
    
    # TODO: What if it is not available (?)
    file_in_memory = BytesIO(_get_tiktok_video_content(url))

    filename = FileHandler.write_binary(
        Output.get_filename(output_filename, FileType.VIDEO),
        file_in_memory.getvalue()
    )

    return FileReturned(
        # TODO: Make this work with videos in memory also
        # but, by now, as file because of 'moviepy'
        content = None,
        filename = filename,
        output_filename = output_filename,
        type = None,
        is_parsed = False,
        # TODO: Write the code that, when using this
        # FileParsingMethod, uses the 'output_filename'
        # as the 'filename' to read it
        parsing_method = FileParsingMethod.MOVIEPY_VIDEO,
        extra_args = None
    )

# TODO: Make this work also with video_id (?)
# TODO: This is no longer working, I think. Maybe
# restablished in a near future...
# def get_tiktok_video_old(
#     url: str,
#     output_filename: Union[str, None] = None
# ) -> FileReturn:
#     """
#     Obtains the Tiktok video from the provided 'url' if 
#     valid and stores it locally if 'output_filename' is
#     provided, or returns it if not.
#     """
#     DOWNLOAD_CDN_URL = 'https://tikcdn.io/ssstik/' # + video_id to download
#
#     if not PythonValidator.is_string(url):
#         raise Exception('The provided "url" parameter is not a string.')

#     tiktok_video_info = TiktokUrlParser.parse(url)

#     download_url = f'{DOWNLOAD_CDN_URL}{tiktok_video_info.video_id}'

#     return download_video(
#         download_url,
#         Output.get_filename(output_filename, FileType.VIDEO)
#     )