from .starPlayerType import StarPlayerType
from .battleTeamsType import BattleTeamsListType

class BattleResultType:
    """
    Represents the detailed results and statistics of a completed battle.
    """
    def __init__(self, data: dict):
        """
        Initialize the BattleResultType object.

        Args:
            data (dict): Dictionary containing battle info from the API.
        """
        if data is None:
            data = {}

        self.mode: str = data.get("mode", "")
        """The game mode played (e.g., 'gemGrab', 'brawlBall', 'soloShowdown')."""

        self.type: str = data.get("type", "")
        """The type of the match (e.g., 'ranked', 'friendly')."""

        self.result: str = data.get("result", "")
        """The outcome of the match for the player (e.g., 'victory', 'defeat', 'draw')."""

        self.duration: int = data.get("duration", 0)
        """The duration of the battle in seconds."""

        self.trophyChange: int = data.get("trophyChange", 0)
        """The number of trophies gained or lost in this battle."""

        self.rank: int = data.get("rank", 0)
        """The final rank achieved (mainly for Showdown modes)."""

        self.starPlayer: StarPlayerType = StarPlayerType(data.get("starPlayer", {}))
        """The player designated as the Star Player (MVP) of the match."""

        self.teams: BattleTeamsListType = BattleTeamsListType(data.get("teams", []))
        """The composition of teams involved in the battle."""

class BattleResultType:
    """
    Represents the detailed results and statistics of a completed battle.
    """
    def __init__(self, data: dict):
        """
        Initialize the BattleResultType object.

        Args:
            data (dict): Dictionary containing battle info from the API.
        """
        if data is None:
            data = {}

        self.mode: str = data.get("mode", "")
        """The game mode played (e.g., 'gemGrab', 'brawlBall', 'soloShowdown')."""

        self.type: str = data.get("type", "")
        """The type of the match (e.g., 'ranked', 'friendly')."""

        self.result: str = data.get("result", "")
        """The outcome of the match for the player (e.g., 'victory', 'defeat', 'draw')."""

        self.duration: int = data.get("duration", 0)
        """The duration of the battle in seconds."""

        self.trophyChange: int = data.get("trophyChange", 0)
        """The number of trophies gained or lost in this battle."""

        self.rank: int = data.get("rank", 0)
        """The final rank achieved (mainly for Showdown modes)."""

        self.starPlayer: StarPlayerType = StarPlayerType(data.get("starPlayer", {}))
        """The player designated as the Star Player (MVP) of the match."""

        self.teams: BattleTeamsListType = BattleTeamsListType(data.get("teams", []))
        """The composition of teams involved in the battle."""