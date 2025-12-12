from dataclasses import dataclass


@dataclass
class TiktokUrl:
    """
    Class to hold the information about a
    TiktokUrl.
    """

    def __init__(
        self,
        username: str,
        video_id: str,
        url: str
    ):
        self.username: str = username
        """
        The user who the video belongs to.
        """
        self.video_id: str = video_id
        """
        The id of the video.
        """
        self.url: str = url
        """
        The long Tiktok url of that video.
        """