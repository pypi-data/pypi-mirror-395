
from yta_file_downloader.utils import get_file
from yta_general.dataclasses import FileReturned
from yta_constants.file import FileType, FileParsingMethod
from yta_programming.output import Output
from yta_programming.decorators.requires_dependency import requires_dependency
from typing import Union
from io import BytesIO


@requires_dependency('yta_web_scraper', 'yta_file_downloader', 'yta_web_scraper')
def download_facebook_video(
    url: str,
    output_filename: Union[str, None, bool] = None
) -> Union[FileReturned, BytesIO]:
    """
    Gets the Facebook video (reel) from the provided 'url' (if valid)
    and returns its data or stores it locally as 'output_filename' if
    provided.
    """
    from yta_web_scraper.chrome import ChromeScraper
    # TODO: Please, export these 'By' and 'Keys' within
    # the 'yta_web_scraper' library to import directly
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    DOWNLOAD_FACEBOOK_VIDEO_URL = 'https://fdownloader.net/en/facebook-reels-downloader'

    scraper = ChromeScraper()
    scraper.go_to_web_and_wait_until_loaded(DOWNLOAD_FACEBOOK_VIDEO_URL)

    # We need to wait until video is shown
    url_input = scraper.find_element_by_id('s_input')
    url_input.send_keys(url)
    url_input.send_keys(Keys.ENTER)

    # We need to click in the upper left image to activate vid popup
    image_container = scraper.find_element_by_class_waiting('div', 'image-fb open-popup')
    image = image_container.find_element(By.TAG_NAME, 'img')
    image.click()

    #video_element = scraper.find_element_by_element_type_waiting('video')
    video_element = scraper.find_element_by_id_waiting('vid')
    video_source_url = video_element.get_attribute('src')

    if output_filename is False:
        return BytesIO(get_file(video_source_url, None))
    
    output_filename = Output.get_filename(output_filename, FileType.VIDEO)
    video = get_file(video_source_url, output_filename)

    return FileReturned(
        # TODO: Make this work with videos in memory also
        # but, by now, as file because of 'moviepy'
        content = video,
        filename = None,
        output_filename = output_filename,
        type = None,
        is_parsed = False,
        # TODO: Write the code that, when using this
        # FileParsingMethod, uses the 'output_filename'
        # as the 'filename' to read it
        parsing_method = FileParsingMethod.MOVIEPY_VIDEO,
        extra_args = None
    )