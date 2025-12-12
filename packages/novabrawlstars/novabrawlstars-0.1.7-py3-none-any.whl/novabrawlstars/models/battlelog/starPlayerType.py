from .brawlerBattleType import BrawlerBattleType

class StarPlayerType:
    """
    Represents the player designated as the 'Star Player' (MVP) in a battle.
    """
    def __init__(self, data: dict):
        """
        Initialize the StarPlayerType object.

        Args:
            data (dict): Dictionary containing star player info from the API.
        """
        if data is None:
            data = {}

        self.tag: str = data.get("tag", "")
        """The unique player tag (e.g., '#P8G9')."""

        self.name: str = data.get("name", "")
        """The display name of the star player."""

        self.brawler: BrawlerBattleType = BrawlerBattleType(data.get("brawler", {}))
        """The Brawler used by the star player during the match."""