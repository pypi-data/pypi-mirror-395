from dataclasses import dataclass


@dataclass
class FacebookUrl:
    """
    Class to hold the information about a
    FacebookUrl.
    """

    def __init__(
        self,
        video_id: str,
        url: str
    ):
        self.video_id: str = video_id
        """
        The id of the video.
        """
        self.url: str = url
        """
        The short Facebook url of that video.
        """