from typing import List
from ..paging.pagingType import PagingType

class BrawlerStatsType:
    """
    Represents the statistics of a brawler.
    """

    def __init__(self, data: dict):
        """
        Initialize the BrawlerStatsType object.

        Args:
            data (dict): Dictionary containing brawler stats info from the API.
        """

        if data is None:
            data = {}
        
        self.items: BrawlerListType = BrawlerListType(data.get("items", []))
        """A list of BrawlerType objects representing the brawlers' statistics."""

        self.paging: PagingType = PagingType(data.get("paging", {}))
        """Paging information for the brawlers' statistics."""

class BrawlerType:
    """
    Represents a single brawler's information.
    """

    def __init__(self, data: dict):
        """
        Initialize the BrawlerType object.

        Args:
            data (dict): Dictionary containing brawler info from the API.
        """

        if data is None:
            data = {}

        self.id: int = data.get("id", 0)
        """The unique identifier of the brawler."""
        self.iconUrl: str = f"https://cdn.brawlify.com/brawlers/borderless/{self.id}.png"
        """The URL of the brawler's icon."""
        self.name: str = data.get("name", "")
        """The name of the brawler."""
        self.starPowers: StarPowerListType = StarPowerListType(data.get("starPowers", []))
        """The list of star powers available for the brawler."""
        self.gadgets: AccessoryListType = AccessoryListType(data.get("gadgets", []))
        """The list of gadgets available for the brawler."""

class BrawlerListType:
    """
    Represents a list of brawlers.
    """

    def __init__(self, data: List[dict]):
        """
        Initialize the BrawlerListType object.

        Args:
            data (List[dict]): List of dictionaries containing raw brawler info from the API.
        """

        if data is None:
            data = []

        self.brawlerList: List[BrawlerType] = [BrawlerType(b) for b in data if b]
        """A list of BrawlerType objects representing the brawlers."""

class AccessoryType:
    """
    Represents a single accessory's information.
    """

    def __init__(self, data: dict):
        """
        Initialize the AccessoryType object.

        Args:
            data (dict): Dictionary containing accessory info from the API.
        """

        if data is None:
            data = {}

        self.id: int = data.get("id", 0)
        """The unique identifier of the accessory."""
        self.iconUrl: str = f"https://cdn.brawlify.com/gadgets/borderless/{self.id}.png"
        """The URL of the accessory's icon."""
        self.name: str = data.get("name", "")
        """The name of the accessory."""

class AccessoryListType:
    """
    Represents a list of accessories.
    """

    def __init__(self, data: List[dict]):
        """
        Initialize the AccessoryListType object.

        Args:
            data (List[dict]): List of dictionaries containing raw accessory info from the API.
        """

        if data is None:
            data = []

        self.accessoryList: List[AccessoryType] = [AccessoryType(a) for a in data if a]
        """A list of AccessoryType objects representing the accessories."""

class StarPowerType:
    """
    Represents a single star power's information.
    """

    def __init__(self, data: dict):
        """
        Initialize the StarPowerType object.

        Args:
            data (dict): Dictionary containing star power info from the API.
        """

        if data is None:
            data = {}

        self.id: int = data.get("id", 0)
        """The unique identifier of the star power."""
        self.iconUrl: str = f"https://cdn.brawlify.com/star-powers/borderless/{self.id}.png"
        """The URL of the star power's icon."""
        self.name: str = data.get("name", "")
        """The name of the star power."""

class StarPowerListType:
    """
    Represents a list of star powers.
    """

    def __init__(self, data: List[dict]):
        """
        Initialize the StarPowerListType object.

        Args:
            data (List[dict]): List of dictionaries containing raw star power info from the API.
        """

        if data is None:
            data = []

        self.starPowerList: List[StarPowerType] = [StarPowerType(s) for s in data if s]
        """A list of StarPowerType objects representing the star powers."""