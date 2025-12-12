class BrawlerStarPowerType:
    """
    Represents a Star Power unlocked for a Brawler.
    """
    def __init__(self, data: dict):
        """
        Initialize the BrawlerStarPowerType object.

        Args:
            data (dict): Dictionary containing star power info from the API.
        """
        if data is None:
            data = {}

        self.name: str = data.get("name", "")
        """The name of the Star Power."""

        self.id: int = data.get("id", 0)
        """The unique identifier of the Star Power."""

        self.iconUrl: str = f"https://cdn.brawlify.com/star-powers/borderless/{self.id}.png" if self.id != 0 else ""
        """The URL to the Star Power's icon image (sourced from Brawlify)."""