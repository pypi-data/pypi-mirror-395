from typing import List

class ClubRankingType:
    """
    Represents a single club's ranking information.
    """
    def __init__(self, data: dict):
        """
        Initialize the ClubRankingType object.

        Args:
            data (dict): Dictionary containing club ranking info from the API.
        """

        if data is None:
            data = {}

        self.tag: str = data.get("tag", "")
        """The unique player tag of the member (e.g., '#P8G9')."""
        self.name: str = data.get("name", "")
        """The display name of the member."""
        self.trophies: int = data.get("trophies", 0)
        """The current number of trophies held by the member."""
        self.rank: int = data.get("rank", 0)
        """The current rank of the club in the ranking list."""
        self.memberCount: int = data.get("memberCount", 0)
        """"The number of members in the club."""
        self.badgeId: int = data.get("badgeId", 0)
        """The ID of the club's badge."""
        self.badgeIconUrl: str = f"https://cdn.brawlify.com/club-badges/regular/{self.badgeId}.png"
        """The URL of the club's badge icon."""

class ClubRankingListType:
    """
    Represents a list of club rankings.
    """
    def __init__(self, data: List[dict]):
        """
        Initialize the ClubRankingListType object.

        Args:
            data (List[dict]): List of dictionaries containing raw club ranking info from the API.
        """
        
        if data is None:
            data = []

        self.clubRankingList: List[ClubRankingType] = [ClubRankingType(c) for c in data if c]
        """A list of ClubRankingType objects representing the club rankings."""