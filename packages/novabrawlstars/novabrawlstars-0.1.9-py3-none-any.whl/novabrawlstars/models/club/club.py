from .clubMember import ClubMemberList

class Club:
    """
    Represents a Brawl Stars club with its details and member list.
    """
    def __init__(self, data: dict):
        """
        Initialize the Club object.

        Args:
            data (dict): Dictionary containing club info from the API.
        """

        if data is None:
            data = {}

        self.tag: str = data.get("tag", "")
        """The unique tag of the club (e.g., '#XY123')."""

        self.name: str = data.get("name", "")
        """The name of the club."""

        self.description: str = data.get("description", "")
        """The description of the club provided by the president."""

        self.trophies: int = data.get("trophies", 0)
        """The total trophies of the club."""

        self.requiredTrophies: int = data.get("requiredTrophies", 0)
        """The minimum number of trophies required to join the club."""

        self.members: ClubMemberList = ClubMemberList(data.get("members", []))
        """A list-like object containing all members of the club."""

        self.type: str = data.get("type", "")
        """The type of the club (e.g., 'open', 'inviteOnly', 'closed')."""

        self.badgeId: int = data.get("badgeId", 0)
        """The unique identifier for the club's badge."""