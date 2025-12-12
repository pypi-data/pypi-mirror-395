from yta_general.dataclasses import FileReturned
from yta_validation.parameter import ParameterValidator
from yta_file.handler import FileHandler
from typing import Union

import requests


def get_file(
    url: str,
    output_filename: Union[str, None] = None
) -> Union[bytes, any]:
    """
    This method sends a request to the provided 'url'
    (if provided) and obtains the file content (if 
    possible). It will write the obtained file locally
    as 'output_filename' if provided.

    This method returns the file content data as 
    obtained from the requested (.content field).
    """
    # TODO: What if nothing on the response (?)
    content = requests.get(url).content

    if output_filename:
        FileHandler.write_binary(output_filename, content)

    return content

def get_file_by_chunks(
    url: str,
    output_filename: Union[str, None] = None
) -> bytes:
    """
    Download the file from the given 'url' chunk
    by chunk to be able to handle big files.

    This method returns the file content data as 
    obtained from the requested (.content field).
    """
    CHUNK_SIZE = 8192

    with requests.get(url, stream = True) as response:
        response.raise_for_status()
        content = b''.join(response.iter_content(CHUNK_SIZE))

    # content = b''
    # with requests.get(url, stream = True) as response:
    #     response.raise_for_status()

    #     #with open(output_filename, 'wb') if output_filename else nullcontext() as file:
    #         for chunk in response.iter_content(CHUNK_SIZE):
    #             content += chunk
    #             # if file:
    #             #     file.write(chunk)

    if output_filename:
        FileHandler.write_binary(output_filename, content)

    return content

def download_file(
    url: str,
    output_filename: str
) -> FileReturned:
    """
    Download the file from the given 'url' (if valid) and
    store it locally as the provided 'output_filename'.
    """
    # TODO: Maybe make it possible to return without
    # writing it locally (?)
    ParameterValidator.validate_mandatory_string('output_filename', output_filename, do_accept_empty = False)
    
    file = get_file(url, output_filename)

    # The type has to be determined by the extension
    # in the 'output_filename' by the FileReturned
    return FileReturned(
        content = file,
        filename = None,
        output_filename = output_filename,
        type = None,
        is_parsed = False,
        parsing_method = None,
        extra_args = None
    )