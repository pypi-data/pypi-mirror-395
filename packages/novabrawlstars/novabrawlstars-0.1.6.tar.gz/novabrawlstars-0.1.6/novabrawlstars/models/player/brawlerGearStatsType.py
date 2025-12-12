class BrawlerGearStatsType:
    """
    Represents a Gear equipped on a Brawler.
    """
    def __init__(self, data: dict):
        """
        Initialize the BrawlerGearStatsType object.

        Args:
            data (dict): Dictionary containing gear stats info from the API.
        """
        if data is None:
            data = {}

        self.name: str = data.get("name", "")
        """The name of the Gear."""

        self.id: int = data.get("id", 0)
        """The unique identifier of the Gear."""

        self.iconUrl: str = f"https://cdn.brawlify.com/gears/regular/{self.id}.png" if self.id != 0 else ""
        """The URL to the Gear's icon image (sourced from Brawlify)."""