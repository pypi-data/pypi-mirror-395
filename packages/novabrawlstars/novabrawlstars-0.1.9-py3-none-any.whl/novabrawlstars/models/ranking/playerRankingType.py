from typing import List
from .brawlerRankingType import PlayerRankingClubType
from ..player.playerIconType import PlayerIconType

class PlayerRankingType:
    """
    Represents a single player's ranking information.
    """

    def __init__(self, data: dict):
        """
        Initialize the PlayerRankingType object.

        Args:
            data (dict): Dictionary containing player ranking info from the API.
        """

        if data is None:
            data = {}

        self.trophyChange: int = data.get("trophyChange", 0)
        """The current number of trophies held by the member."""
        self.club: PlayerRankingClubType = PlayerRankingClubType(data.get("club", {}))
        """The club information of the player."""
        self.icon: PlayerIconType = PlayerIconType(data.get("icon", {}))
        """The icon information of the player."""
        self.tag: str = data.get("tag", "")
        """The unique player tag of the member (e.g., '#P8G9')."""
        self.name: str = data.get("name", "")
        """The display name of the member."""
        self.rank: int = data.get("rank", 0)
        """The current rank of the player in the ranking list."""
        self.nameColor: str = data.get("nameColor", "")
        """The color of the player's name."""

class PlayerRankingListType:
    """
    Represents a list of player rankings.
    """
    def __init__(self, data: List[dict]):
        """
        Initialize the PlayerRankingListType object.

        Args:
            data (List[dict]): List of dictionaries containing raw player ranking info from the API.
        """

        if data is None:
            data = []
            
        self.playerRankingList: List[PlayerRankingType] = [PlayerRankingType(p) for p in data if p]
        """A list of PlayerRankingType objects representing the player rankings."""