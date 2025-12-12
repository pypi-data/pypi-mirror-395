from .playerClubType import PlayerClubType
from .playerIconType import PlayerIconType
from .brawlerStatsType import BrawlerStatsListType

class Player:
    """
    Represents a Brawl Stars player with their statistics and profile information.
    """

    def __init__(self, data: dict):
        """
        Initialize the Player object.

        Args:
            data (dict): Dictionary containing player info from the API.
        """
        if data is None:
            data = {}

        self.tag: str = data.get("tag", "")
        """The unique player tag (e.g., '#P8G9')."""

        self.name: str = data.get("name", "")
        """The player's display name."""

        self.nameColor: str = data.get("nameColor", "")
        """The hex code of the player's name color (e.g., '0xffffffff')."""

        self.trophies: int = data.get("trophies", 0)
        """The current number of trophies the player has."""

        self.highestTrophies: int = data.get("highestTrophies", 0)
        """The highest number of trophies the player has ever achieved."""

        self.soloVictories: int = data.get("soloVictories", 0)
        """The number of victories in Solo Showdown mode."""

        self.duoVictories: int = data.get("duoVictories", 0)
        """The number of victories in Duo Showdown mode."""

        self.threeVsThreeVictories: int = data.get("3vs3Victories", 0)
        """The number of victories in 3vs3 game modes."""

        self.bestRoboRumbleTime: int = data.get("bestRoboRumbleTime", 0)
        """The best time achieved in Robo Rumble (usually in seconds/level id)."""

        self.bestTimeAsBigBrawler: int = data.get("bestTimeAsBigBrawler", 0)
        """The best time survived as the Big Brawler in Big Game mode."""

        self.expLevel: int = data.get("expLevel", 0)
        """The player's current experience level."""

        self.expPoints: int = data.get("expPoints", 0)
        """The player's current experience points."""

        self.isQualifiedFromChampionshipChallenge: bool = data.get("isQualifiedFromChampionshipChallenge", False)
        """Indicates if the player has qualified for the Championship Challenge."""

        self.club: PlayerClubType = PlayerClubType(data.get("club", {}))
        """An object containing information about the player's club."""

        self.icon: PlayerIconType = PlayerIconType(data.get("icon", {}))
        """An object representing the player's selected profile icon."""

        self.brawlers: BrawlerStatsListType = BrawlerStatsListType(data.get("brawlers", []))
        """A collection of statistics for the brawlers unlocked by the player."""