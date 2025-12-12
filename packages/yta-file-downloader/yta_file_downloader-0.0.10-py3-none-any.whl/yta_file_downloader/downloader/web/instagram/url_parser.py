"""
In this file we handle Facebook url and we parse
them to obtain basic information and check if
they are valid ones or not.

But by now I'm only accepting reel urls
- Short (shared reel): 'https://www.instagram.com/reel/DHQf6RmMFtf/?igsh=ZBDzeTA4cWkwbW4w'
"""
from yta_file_downloader.downloader.web.instagram.dataclasses import InstagramUrl
from yta_constants.regex import GeneralRegularExpression
from yta_validation.parameter import ParameterValidator


class InstagramUrlParser:
    """
    Class to simplify the way we parse Instagram
    videos urls.
    """

    @staticmethod
    def is_valid(
        url: str
    ) -> bool:
        """
        Check if the provided Instagram video 'url' is
        valid or not. A valid Instagram url can be a 
        short url or a long url.
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        
        return _is_short_instagram_url(url)
    
    @staticmethod
    def parse(
        url: str
    ) -> InstagramUrl:
        """
        Parse the provided 'url' and return a InstagramUrl
        dataclass instance containing the author username,
        the video id and the long-format url, or raises
        an Exception if the given 'url' is not valid.
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)

        if not InstagramUrlParser.is_valid(url):
            raise Exception('The provided "url" is not a valid Instagram video url.')
        
        url = _clean(url)
        aux = url.split('/')

        return InstagramUrl(
            video_id = aux[len(aux) - 1],
            url = url
        )
    
def _is_short_instagram_url(
    url: str
) -> bool:
    ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
    
    return GeneralRegularExpression.INSTAGRAM_SHORT_REEL_URL.parse(url)

def _clean(
    url: str
) -> bool:
    """
    Removes any additional parameter that is after a
    question mark sign.
    """
    ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
    
    return (
        url.split('?')[0]
        if '?' in url else
        url
    )