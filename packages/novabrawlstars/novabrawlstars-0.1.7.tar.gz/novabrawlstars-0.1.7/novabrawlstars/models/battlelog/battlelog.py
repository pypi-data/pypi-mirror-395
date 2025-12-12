from .battleEventType import BattleEventType
from .battleResultType import BattleResultType
from typing import List

class BattleLogType:
    """
    Represents a single entry in a player's battle log.
    """
    def __init__(self, data: dict):
        """
        Initialize the BattleLogType object.

        Args:
            data (dict): Dictionary containing battle info from the API.
        """
        if data is None:
            data = {}
        
        self.battleTime: str = data.get("battleTime", "")
        """The timestamp of when the battle occurred (ISO 8601 format, e.g., '20231027T143000.000Z')."""

        self.event: BattleEventType = BattleEventType(data.get("event", {}))
        """Details about the event, such as the map and game mode ID."""

        self.battle: BattleResultType = BattleResultType(data.get("battle", {}))
        """The detailed results of the battle, including teams, winner, and trophy changes."""

class BattleLogListType:
    """
    Represents a collection of battle log entries (recent matches).
    """
    def __init__(self, data: dict):
        """
        Initialize the BattleLogListType object.

        Args:
            data (dict): Dictionary containing the list of battles under the 'items' key.
        """
        if data is None:
            data = {}
        
        self.battlesLogList: List[BattleLogType] = [BattleLogType(b) for b in data.get("items", []) if b]
        """A list of BattleLogType objects representing the player's recent matches."""