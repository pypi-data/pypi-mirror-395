class BrawlerBattleType:
    """
    Represents the state of a Brawler within a specific battle context (Battle Log).
    """
    def __init__(self, data: dict):
        """
        Initialize the BrawlerBattleType object.

        Args:
            data (dict): Dictionary containing brawler info from the API.
        """
        if data is None:
            data = {}

        self.id: int = data.get("id", 0)
        """The unique identifier of the brawler."""

        self.name: str = data.get("name", "")
        """The name of the brawler."""

        self.iconBrawlerUrl: str = f"https://cdn.brawlify.com/brawlers/borderless/{self.id}.png" if self.id != 0 else ""
        """The URL to the brawler's image (sourced from Brawlify)."""

        self.power: int = data.get("power", 0)
        """The power level of the brawler during this specific battle."""

        self.trophies: int = data.get("trophies", 0)
        """The number of trophies the brawler had at the time of the battle."""