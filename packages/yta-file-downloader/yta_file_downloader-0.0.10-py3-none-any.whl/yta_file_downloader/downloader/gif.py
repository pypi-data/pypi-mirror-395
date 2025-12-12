from yta_file_downloader.downloader.image import download_image
from yta_general.dataclasses import FileReturned
from yta_programming.output import Output
from yta_programming_env import Environment
from yta_constants.file import FileExtension
from random import choice
from typing import Union

import requests


GIPHY_API_KEY = Environment.get_current_project_env('GIPHY_API_KEY')

def download_gif(
    query: str,
    output_filename: Union[str, None] = None
) -> Union[FileReturned, None]:
    """
    Download a random gif from the Giphy platform using the API
    key. The gif is stored locally as the given 'output_filename'
    forced to be a .webp file.

    This method returns None if no gif found or an UnparsedFile
    instance to be able to handle the file content with the
    appropriate library.

    Check this logged in: https://developers.giphy.com/dashboard/
    """
    limit = 5

    url = "http://api.giphy.com/v1/gifs/search"
    url += '?q=' + query + '&api_key=' + GIPHY_API_KEY + '&limit=' + str(limit)

    response = requests.get(url)
    response = response.json()

    if (
        not response or
        len(response['data']) == 0
    ):
        # TODO: Raise exception of no gif found
        print('No gif "' + query + '" found')
        return None
    
    element = choice(response['data'])
    gif_url = 'https://i.giphy.com/' + element['id'] + '.webp'

    return download_image(gif_url, Output.get_filename(output_filename, FileExtension.WEBP))