from typing import List
from .brawlerAccessoryType import BrawlerAccessoryType
from .brawlerStarPowerType import BrawlerStarPowerType
from .brawlerGearStatsType import BrawlerGearStatsType

class BrawlerStatsType:
    """
    Represents the statistics of a specific Brawler for a player.
    """
    def __init__(self, data: dict):
        """
        Initialize the BrawlerStatsType object.

        Args:
            data (dict): Dictionary containing brawler stats info from the API.
        """
        if data is None:
            data = {}

        self.id: int = data.get("id", 0)
        """The unique identifier of the brawler."""

        self.name: str = data.get("name", "")
        """The name of the brawler."""

        self.rank: int = data.get("rank", 0)
        """The current rank of the brawler."""

        self.trophies: int = data.get("trophies", 0)
        """The current number of trophies for this brawler."""

        self.highestTrophies: int = data.get("highestTrophies", 0)
        """The highest number of trophies ever achieved with this brawler."""

        self.power: int = data.get("power", 0)
        """The power level of the brawler (e.g., 1-11)."""

        self.maxWinStreak: int = data.get("maxWinStreak", 0)
        """The maximum win streak achieved with this brawler."""

        self.currentWinStreak: int = data.get("currentWinStreak", 0)
        """The current active win streak with this brawler."""

        self.iconUrl: str = f"https://cdn.brawlify.com/brawlers/borderless/{self.id}.png" if self.id != 0 else ""
        """The URL to the brawler's image (sourced from Brawlify)."""

        self.gadgets: List[BrawlerAccessoryType] = [BrawlerAccessoryType(a) for a in data.get("gadgets", []) if a]
        """A list of gadgets unlocked for this brawler."""

        self.starPowers: List[BrawlerStarPowerType] = [BrawlerStarPowerType(sp) for sp in data.get("starPowers", []) if sp]
        """A list of star powers unlocked for this brawler."""

        self.gears: List[BrawlerGearStatsType] = [BrawlerGearStatsType(g) for g in data.get("gears", []) if g]
        """A list of gears equipped or unlocked for this brawler."""

class BrawlerStatsListType:
    """
    Represents a collection of Brawler statistics.
    """
    def __init__(self, data: List[dict]):
        """
        Initialize the BrawlerStatsListType object.

        Args:
            data (List[dict]): List of dictionaries containing brawler stats info from the API.
        """
        self.brawlersList: List[BrawlerStatsType] = [BrawlerStatsType(b) for b in data if b]
        """A list of BrawlerStatsType objects representing the player's brawlers."""