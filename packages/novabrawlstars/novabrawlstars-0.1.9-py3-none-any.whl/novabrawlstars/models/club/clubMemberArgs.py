from .clubMember import ClubMemberList
from ..paging.pagingType import PagingType

class ClubMemberArgs:
    """
    Represents the arguments related to club members, including the list of members and pagination info.
    """

    def __init__(self, data: dict):
        """
        Initialize the ClubMemberArgs object.

        Args:
            data (dict): Dictionary containing club member args info from the API.
        """

        if data is None:
            data = {}

        self.members: ClubMemberList = ClubMemberList(data.get("items", []))
        """A list of ClubMember objects representing the members of the club."""

        self.paging: PagingType = PagingType(data.get("paging", {}))
        """An object representing the cursors for pagination."""