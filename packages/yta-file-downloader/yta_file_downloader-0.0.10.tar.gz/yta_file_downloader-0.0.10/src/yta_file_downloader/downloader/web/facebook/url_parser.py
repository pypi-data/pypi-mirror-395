"""
In this file we handle Facebook url and we parse
them to obtain basic information and check if
they are valid ones or not.

We have different types of valid urls:
- 'https://www.facebook.com/watch/?v=499831560618548'
- 'https://www.facebook.com/RolandGarros/videos/10155404760334920/FOO'
- 'https://www.facebook.com/RolandGarros/videos/FOO/10155404760334920'

But by now I'm only accepting reel urls
- Short (shared reel): 'https://www.facebook.com/share/r/1ZBKSvZZVr/'
"""
from yta_file_downloader.downloader.web.facebook.dataclasses import FacebookUrl
from yta_constants.regex import GeneralRegularExpression
from yta_validation.parameter import ParameterValidator


class FacebookUrlParser:
    """
    Class to simplify the way we parse Facebook
    videos urls.
    """

    @staticmethod
    def is_valid(
        url: str
    ) -> bool:
        """
        Check if the provided Facebook video 'url' is
        valid or not. A valid Facebook url can be a 
        short url or a long url.
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        
        return _is_short_facebook_url(url)
    
    @staticmethod
    def parse(
        url: str
    ) -> FacebookUrl:
        """
        Parse the provided 'url' and return a FacebookUrl
        dataclass instance containing the video id and the
        short-format url, or raises an Exception if the
        given 'url' is not valid.
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)

        if not FacebookUrlParser.is_valid(url):
            raise Exception('The provided "url" is not a valid Facebook video url.')
        
        url = _clean(url)
        aux = url.split('/')

        return FacebookUrl(
            video_id = aux[len(aux) - 1],
            url = url
        )
    
def _is_short_facebook_url(
    url: str
) -> bool:
    ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
    
    return GeneralRegularExpression.FACEBOOK_SHORT_REEL_URL.parse(url)

def _clean(
    url: str
) -> str:
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