class BattleEventType:
    """
    Represents the event details (map and game mode) of a specific battle.
    """
    def __init__(self, data: dict):
        """
        Initialize the BattleEventType object.

        Args:
            data (dict): Dictionary containing battle event info from the API.
        """
        if data is None:
            data = {}

        self.id: int = data.get("id", 0)
        """The unique identifier of the event or map."""

        self.mode: str = data.get("mode", "")
        """The name of the game mode (e.g., 'Gem Grab', 'Brawl Ball')."""

        self.modeId: int = data.get("modeId", 0)
        """The internal identifier for the game mode (used to generate the icon URL)."""

        self.modeIconUrl: str = f"https://cdn.brawlify.com/game-modes/regular/{48_000_000 + self.modeId}.png" if self.modeId != 0 else ""
        """The URL to the game mode's icon image (sourced from Brawlify)."""

        self.map: str = data.get("map", "")
        """The name of the map where the battle took place."""

        self.mapIconUrl: str = f"https://cdn.brawlify.com/maps/regular/{self.id}.png"
        """The URL to the map's preview image (sourced from Brawlify)."""