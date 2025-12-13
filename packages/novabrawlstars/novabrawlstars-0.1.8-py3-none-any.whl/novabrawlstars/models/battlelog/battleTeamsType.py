from typing import List
from .brawlerBattleType import BrawlerBattleType

class BattlePlayerType:
    """
    Represents a player participating in a specific battle.
    """
    def __init__(self, data: dict):
        """
        Initialize the BattlePlayerType object.

        Args:
            data (dict): Dictionary containing player info from the API.
        """
        if data is None:
            data = {}
        
        self.tag: str = data.get("tag", "")
        """The unique player tag (e.g., '#P8G9')."""

        self.name: str = data.get("name", "")
        """The display name of the player."""

        self.brawler: BrawlerBattleType = BrawlerBattleType(data.get("brawler", {}))
        """The Brawler used by the player in this battle."""

class BattleTeamType:
    """
    Represents a single team consisting of one or more players in a battle.
    """
    def __init__(self, data: List[dict]):
        """
        Initialize the BattleTeamType object.

        Args:
            data (list): List of dictionaries containing player info for this team.
        """
        if data is None:
            data = []
        
        self.players: List[BattlePlayerType] = [BattlePlayerType(p) for p in data if p]
        """A list of BattlePlayerType objects representing the players in this team."""

class BattleTeamsListType:
    """
    Represents the collection of conflicting teams in a battle.
    """
    def __init__(self, data: List[dict]):
        """
        Initialize the BattleTeamsListType object.

        Args:
            data (list): List of lists (representing teams) containing player info.
        """
        if data is None:
            data = []
        
        self.teamsList: List[BattleTeamType] = [BattleTeamType(t) for t in data if t]
        """A list of BattleTeamType objects representing all teams involved in the match."""