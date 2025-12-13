class BrawlerAccessoryType:
    """
    Represents a Gadget (Accessory) unlocked for a Brawler.
    """
    def __init__(self, data: dict):
        """
        Initialize the BrawlerAccessoryType object.

        Args:
            data (dict): Dictionary containing accessory info from the API.
        """
        if data is None:
            data = {}

        self.name: str = data.get("name", "")
        """The name of the Gadget."""

        self.id: int = data.get("id", 0)
        """The unique identifier of the Gadget."""

        self.iconUrl: str = f"https://cdn.brawlify.com/gadgets/borderless/{self.id}.png" if self.id != 0 else ""
        """The URL to the Gadget's icon image (sourced from Brawlify)."""