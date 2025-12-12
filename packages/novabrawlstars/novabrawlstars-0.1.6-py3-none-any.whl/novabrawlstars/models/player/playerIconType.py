class PlayerIconType:
    """
    Represents the player's profile icon.
    """
    def __init__(self, data: dict):
        """
        Initialize the PlayerIconType object.

        Args:
            data (dict): Dictionary containing icon info from the API.
        """
        if data is None:
            data = {}
        
        self.id: int = data.get("id", 0)
        """The unique identifier of the profile icon."""

        self.iconUrl: str = f"https://cdn.brawlify.com/profile-icons/regular/{self.id}.png"
        """The URL to the profile icon image (sourced from Brawlify)."""