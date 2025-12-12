from ..player.playerIconType import PlayerIconType
from typing import List

class ClubMember:
    """
    Represents a single member within a Brawl Stars club.
    """
    def __init__(self, data: dict):
        """
        Initialize the ClubMember object.

        Args:
            data (dict): Dictionary containing member info from the API.
        """

        if data is None:
            data = {}

        self.icon: PlayerIconType = PlayerIconType(data.get("icon", {}))
        """An object representing the member's profile icon."""

        self.tag: str = data.get("tag", "")
        """The unique player tag of the member (e.g., '#P8G9')."""

        self.name: str = data.get("name", "")
        """The display name of the member."""

        self.trophies: int = data.get("trophies", 0)
        """The current number of trophies held by the member."""

        self.role: str = data.get("role", "")
        """The member's role in the club (e.g., 'member', 'senior', 'vicePresident', 'president')."""

        self.nameColor: str = data.get("nameColor", "")
        """The hex code of the member's name color."""

class ClubMemberList:
    """
    Represents a list of members belonging to a club.
    """
    def __init__(self, data: List[dict]):
        """
        Initialize the ClubMemberList object.

        Args:
            data (List[dict]): List of dictionaries containing raw member info from the API.
        """
        
        self.clubMemberList: List[ClubMember] = [ClubMember(m) for m in data if m]
        """A list of ClubMember objects representing the members of the club."""