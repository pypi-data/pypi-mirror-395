class PlayerClubType:
    """
    Represents the basic information of a club associated with a player.
    """
    def __init__(self, data: dict):
        """
        Initialize the PlayerClub object.

        Args:
            data (dict): Dictionary containing club info from the API.
        """
        if data is None:
            data = {}
        
        self.tag: str = data.get("tag", "")
        """The unique tag of the club (e.g., '#8J9U2')."""

        self.name: str = data.get("name", "")
        """The name of the club."""