import httpx
from .exceptions import (
    ApiError,
    InvalidTokenError,
    RateLimitError,
    NotFoundError,
    UnexpectedError,
    ServiceErrorMaintenance
)
from .models import Player, BattleLogListType, Club, ClubMemberArgs

class NovaBrawlStars:
    """
    Asynchronous client for interacting with the official Brawl Stars API.
    
    This class handles authentication, HTTP sessions, and JSON response parsing.
    It supports usage as an asynchronous context manager (async with).
    """

    __BASE_URL = "https://api.brawlstars.com/v1"

    def __init__(self, token: str, timeout: float = 10.0):
        """
        Initializes the NovaBrawlStars client.

        Args:
            token (str): The API token obtained from the Brawl Stars developer portal.
            timeout (float): The maximum time (in seconds) to wait for a response. Defaults to 10.0.

        Raises:
            InvalidTokenError: If the provided token is empty or not a string.
        """
        if not token or not isinstance(token, str) or token.strip() == "":
            raise InvalidTokenError("API token is required")
        
        self.__token = token

        headers = {
            "Authorization": f"Bearer {self.__token}",
            "Accept": "application/json",
            "User-Agent": "NovaBrawlStarsAPI/1.0"
        }

        self.client = httpx.AsyncClient(
            headers=headers,
            timeout=timeout,
            follow_redirects=True
        )
    
    async def close(self):
        """
        Closes the underlying HTTP client and releases resources.
        """
        await self.client.aclose()

    async def __aenter__(self):
        """
        Enables use of the 'async with' context manager.
        Returns the client instance.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Enables use of the 'async with' context manager.
        Automatically closes the client when exiting the block.
        """
        await self.close()

    async def __request(self, endpoint: str):
        """
        Performs an internal HTTP GET request to the API.

        Automatically handles HTTP status codes and raises appropriate exceptions
        for errors.

        Args:
            endpoint (str): The endpoint path (e.g., "/players/...").

        Returns:
            dict: The JSON data returned by the API if successful (status 200).

        Raises:
            InvalidTokenError: If the API token is invalid (403).
            NotFoundError: If the requested resource does not exist (404).
            RateLimitError: If the request limit has been exceeded (429).
            UnexpectedError: For internal server errors (500) or network issues.
            ServiceErrorMaintenance: If the API is under maintenance (503).
            ApiError: For any other unhandled HTTP errors.
        """
        __url = f"{self.__BASE_URL}{endpoint}"

        try:
            response = await self.client.get(__url)
            status = response.status_code

            if status == 200:
                return response.json()
            if status == 403:
                raise InvalidTokenError("Invalid API token.", code=403)
            if status == 404:
                raise NotFoundError("Resource not found.", code=404)
            if status == 429:
                raise RateLimitError("Rate limit exceeded.", code=429)
            if status == 500:
                raise UnexpectedError("Internal server error.", code=500)
            if status == 503:
                raise ServiceErrorMaintenance("Service is under maintenance.", code=503)
        
            raise ApiError(response.text, code=status)
        except httpx.RequestError as e:
            raise UnexpectedError(f"Network error occurred: {str(e)}", code=0)
        
    def __clean_tag(self, tag: str) -> str:
        """
        Cleans the provided tag by removing '#' characters and spaces,
        and converting it to uppercase.

        Args:
            tag (str): The raw tag (e.g., "#PY982").

        Returns:
            str: The cleaned tag (e.g., "PY982").
        """
        return tag.strip().replace("#", "").replace(" ", "").upper()

    async def get_player(self, tag: str) -> Player:
        """
        Retrieves information about a specific player.

        Args:
            tag (str): The player tag (with or without '#').

        Returns:
            Player: An object containing the player's data.
        """
        tag = self.__clean_tag(tag)
        data = await self.__request(f"/players/%23{tag}")
        return Player(data)
    
    async def get_battlelog(self, tag: str) -> BattleLogListType:
        """
        Retrieves the battle log (recent matches) for a specific player.

        Args:
            tag (str): The player tag.

        Returns:
            BattleLogListType: An object containing a list of recent battles.
        """
        tag = self.__clean_tag(tag)
        data = await self.__request(f"/players/%23{tag}/battlelog")
        return BattleLogListType(data)
    
    async def get_player_club(self, tagClub: str) -> Club:
        """
        Retrieves information about a specific club.

        Args:
            tagClub (str): The club tag.

        Returns:
            Club: An object containing the club's data.
        """
        tagClub = self.__clean_tag(tagClub)
        data = await self.__request(f"/clubs/%23{tagClub}")
        return Club(data)
    
    async def get_club_members(self, tagClub: str, limit: int | None = None, after: str | None = None, before: str | None = None) -> ClubMemberArgs:
        """
        Retrieves the list of members in a specific club.

        Args:
            tagClub (str): The club tag.
            limit (int | None): Maxium number of members to return. Optional.
            after (str | None): Cursor for pagination to get members after this tag. Optional.
            before (str | None): Cursor for pagination to get members before this tag. Optional.

        Returns:
            ClubMemberArgs: An object containing the list of club members and pagination info.
        """

        query = ""

        if limit is not None and limit < 1:
            raise ValueError("Limit must be greater than 0.")
        if after is not None and before is not None:
            raise ValueError("Cannot use both 'after' and 'before' for pagination.")
        if after is not None:
            query += f"?after={after}"
        if before is not None:
            query += f"?before={before}"
        if limit is not None:
            if query == "":
                query += f"?limit={limit}"
            else:
                query += f"&limit={limit}"
        
        tagClub = self.__clean_tag(tagClub)
        data: dict = await self.__request(f"/clubs/%23{tagClub}/members{query}")
        return ClubMemberArgs(data)