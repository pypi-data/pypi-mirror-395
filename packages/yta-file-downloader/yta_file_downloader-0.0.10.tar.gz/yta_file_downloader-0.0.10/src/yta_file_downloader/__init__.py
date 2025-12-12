from yta_file_downloader.downloader.audio import download_audio
from yta_file_downloader.downloader.gif import download_gif
from yta_file_downloader.downloader.image import download_image_2
from yta_file_downloader.downloader.video import download_video
from yta_file_downloader.downloader.web.facebook.downloader import download_facebook_video
from yta_file_downloader.downloader.web.instagram.downloader import download_instagram_video
from yta_file_downloader.downloader.web.tiktok.downloader import download_tiktok_video
from yta_file_downloader.utils import download_file
from yta_general.dataclasses import FileReturned
from yta_constants.file import FileType, FileExtension
from yta_programming.output import Output
from yta_programming.decorators.requires_dependency import requires_dependency
from yta_validation.parameter import ParameterValidator
from typing import Union


class Downloader:
    """
    Class to encapsulate the functionality related to downloading
    resources from the Internet.
    """

    @staticmethod
    def download_audio(
        url: str,
        output_filename: Union[str, None] = None
    ) -> FileReturned:
        """
        Download the audio file from the provided 'url' and store
        it locally as 'output_filename'.
        """
        ParameterValidator.validate_mandatory_string('url', url, False)

        return download_audio(
            url,
            # TODO: What if we don't want to force the
            # download and want to get the content
            # only (?)
            Output.get_filename(output_filename, FileType.AUDIO)
        )
    
    @staticmethod
    def download_gif(
        query: str, 
        output_filename: Union[str, None] = None
    ) -> Union[FileReturned, None]:
        """
        Search for a gif with the provided 'query' and download it,
        if existing, to a local file called 'output_filename'.

        TODO: I think this is unexpected, because it is searching
        from Giphy and not downloading a file from a url as a gif...
        and I think it would be like 'download_image' just with
        the gif extension.
        """
        ParameterValidator.validate_mandatory_string('query', query, False)

        return download_gif(
            query,
            Output.get_filename(output_filename, FileExtension.GIF)
        )
    
    @staticmethod
    @requires_dependency('yta_google_drive_downloader', 'yta_file_downloader', 'yta_google_drive_downloader')
    def download_google_drive_resource(
        google_drive_url: str,
        output_filename: Union[str, None] = None
    ) -> FileReturned:
        """
        Download the Google Drive resource from the given
        'google_drive_url', if existing and available, and
        store it locally with the provided 'output_filename'.

        This method requires the optional library
        'yta_google_drive_downloader'.
        """
        from yta_google_drive_downloader.resource import GoogleDriveResource
        
        ParameterValidator.validate_mandatory_string('google_drive_url', google_drive_url, False)

        resource = GoogleDriveResource(google_drive_url)
        filename = resource.download(Output.get_filename(output_filename))

        # The extension will be automatically detected
        # by the FileReturned based on the filename
        return FileReturned(
            content = None,
            filename = filename,
            output_filename = output_filename,
            type = None,
            is_parsed = False,
            parsing_method = None,
            extra_args = None
        )
    
    @staticmethod
    def download_image(
        url: str,
        output_filename: Union[str, None] = None
    ) -> FileReturned:
        """
        Download the image from the provided 'url' and stores it, if
        existing and available, as a local file called 'output_filename'.
        """
        ParameterValidator.validate_mandatory_string('url', url, False)
        
        return download_image_2(
            url,
            Output.get_filename(output_filename)
        )

    @staticmethod
    def download_video(
        url: str,
        output_filename: Union[str, None] = None
    ) -> FileReturned:
        """
        Download the video from the provided 'url' and stores it, if
        existing and available, as a local file called 'output_filename'.
        """
        ParameterValidator.validate_mandatory_string('url', url, False)
        
        return download_video(
            url,
            Output.get_filename(output_filename)
        )
    
    @staticmethod
    def download_file(
        url: str,
        output_filename: str
    ) -> FileReturned:
        """
        Download the file from the given 'url' and
        store it locally as 'output_filename'.
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('output_filename', output_filename, do_accept_empty = False)

        # 'output_filename' is mandatory because we don't
        # know the file extension/type
        
        return download_file(
            url,
            output_filename
        )

    # TODO: All these methods below could be in other library
    @staticmethod
    def download_tiktok(
        url: str,
        output_filename: Union[str, None, bool] = None
    ) -> Union[FileReturned, 'BytesIO']:
        """
        Download a Tiktok video from the given 'url' and
        stores it locally as the provided 'output_filename'
        (or a temporary one if not provided).
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        
        return download_tiktok_video(
            url,
            (
                Output.get_filename(output_filename)
                if output_filename is not False else
                False
            )
        )
    
    @staticmethod
    def download_facebook(
        url: str,
        output_filename: Union[str, None, bool] = None
    ) -> Union[FileReturned, 'BytesIO']:
        """
        Download a Facebook video from the given 'url' and
        stores it locally as the provided 'output_filename'
        (or a temporary one if not provided).
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        
        return download_facebook_video(
            url,
            (
                Output.get_filename(output_filename)
                if output_filename is not False else
                False
            )
        )
    
    @staticmethod
    def download_instagram(
        url: str,
        output_filename: Union[str, None, bool] = None
    ) -> Union[FileReturned, 'BytesIO']:
        """
        Download an Instagram video from the given 'url' and
        stores it locally as the provided 'output_filename'
        (or a temporary one if not provided).
        """
        ParameterValidator.validate_mandatory_string('url', url, do_accept_empty = False)
        
        return download_instagram_video(
            url,
            (
                Output.get_filename(output_filename)
                if output_filename is not False else
                False
            )
        )
