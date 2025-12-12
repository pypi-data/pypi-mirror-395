
from yta_file_downloader.utils import get_file
from yta_general.dataclasses import FileReturned
from yta_constants.file import FileType, FileParsingMethod
from yta_programming.output import Output
from yta_programming.decorators.requires_dependency import requires_dependency
from typing import Union
from io import BytesIO


@requires_dependency('yta_web_scraper', 'yta_file_downloader', 'yta_web_scraper')
def download_instagram_video(
    url: str,
    output_filename: Union[str, None, bool] = None
) -> Union[FileReturned, BytesIO]:
    """
    Gets the Instagram video (reel) from the provided 'url' (if valid)
    and returns its data or stores it locally as 'output_filename' if
    provided.
    """
    from yta_web_scraper.chrome import ChromeScraper
    # TODO: Please, export these 'By' within the
    # 'yta_web_scraper' library to import directly
    from selenium.webdriver.common.by import By

    # This method is based on the external website below, so
    # it could stop working when that website is off.
    # TODO: Try to make alternatives with other web pages.
    DOWNLOAD_INSTAGRAM_VIDEO_URL = 'https://downloadgram.org/video-downloader.php'
    
    scraper = ChromeScraper()
    scraper.go_to_web_and_wait_until_loaded(DOWNLOAD_INSTAGRAM_VIDEO_URL)

    # We need to place the url in the input and press enter
    url_input = scraper.find_element_by_id('url')
    url_input.send_keys(url)

    submit_button = scraper.find_element_by_id('submit')
    submit_button.click()

    # We need to wait until video is shown
    video_element = scraper.find_element_by_element_type_waiting('video')
    video_source_element = video_element.find_element(By.TAG_NAME, 'source')
    video_source_url = video_source_element.get_attribute('src')

    # This just downloads the thumbnail but, for what (?)
    # thumbnail_image_url = video_element.get_attribute('poster')
    # download_image(thumbnail_image_url, 'test_instagram_image.png')

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

# TODO: Implement 'get_instagram_story' (?)

"""
# Check: https://github.com/gabrielkheisa/instagram-downloader/blob/main/run.py
# He downloads with selenium
# This and the one below: https://stackoverflow.com/a/48705202
# This code (https://github.com/instaloader/instaloader/tree/master) is used
# by RocketAPI to charge you
"""