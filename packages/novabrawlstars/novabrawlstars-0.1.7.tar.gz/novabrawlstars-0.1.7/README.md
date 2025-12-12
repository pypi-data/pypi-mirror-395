# NovaBrawlStarsApi

A Python library to easily interact with the Brawl Stars API and fetch player information.

## Features

- Retrieve detailed player information
- Supports multiple player tags
- Easy Python integration
- Secure API key management with .env

## Installation

You can install NovaBrawlStarsApi via pip:

```bash
pip install novabrawlstars
```

Or clone the repo and installation dependencies manually:

```bash
git clone https://github.com/NovaFenice/NovaBrawlStarsApi.git
cd NovaBrawlStarsApi

```

## Usage

### How to get players info

```py
from novabrawlstars.client import NovaBrawlStars
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_bs = os.getenv("api_bs") # Your Brawl Stars API token
    tag_p1 = os.getenv("tag_p1") # Brawl Stars Player tag (es. #12345678 or 12345678)
    nb = NovaBrawlStars(api_bs) # Initialize the Brawl Stars API client
    
    async with nb as client:
        player = await client.get_player(tag_p1)  # Get a Player object from the API

    await nb.close() # Close the HTTP client session

if __name__ == "__main__":
    asyncio.run(main()) # Run the main function
```

### How to get battlelog info

```py
from novabrawlstars.client import NovaBrawlStars
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_bs = os.getenv("api_bs") # Your Brawl Stars API token
    tag_p1 = os.getenv("tag_p1") # Brawl Stars Player tag (es. #12345678 or 12345678)
    nb = NovaBrawlStars(api_bs) # Initialize the Brawl Stars API client
    
    async with nb as client:
        player_battlelog = await client.get_battlelog(tag_p1)  # Get a BattleLogListType object from the API

    await nb.close() # Close the HTTP client session

if __name__ == "__main__":
    asyncio.run(main()) # Run the main function
```

### How to get club info

```py
from novabrawlstars.client import NovaBrawlStars
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_bs = os.getenv("api_bs") # Your Brawl Stars API token
    tag_p1 = os.getenv("tag_p1") # Brawl Stars Player tag (es. #12345678 or 12345678)
    nb = NovaBrawlStars(api_bs) # Initialize the Brawl Stars API client
    
    async with nb as client:
        player = await client.get_player(tag_p1)  # Get a BattleLogListType object from the API
        club = await client.get_player_club(player.club.tag) # Get a Club object passing the player 

    await nb.close() # Close the HTTP client session

if __name__ == "__main__":
    asyncio.run(main()) # Run the main function
```

### How to get club members info using pagination

```py
from novabrawlstars.client import NovaBrawlStars
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_bs = os.getenv("api_bs") # Your Brawl Stars API token
    tag_p1 = os.getenv("tag_p1") # Brawl Stars Player tag (es. #12345678 or 12345678)

    nb = NovaBrawlStars(api_bs) # Initialize the Brawl Stars API client

    async with nb as client:
        player = await client.get_player(tag_p1) # Get a Player object from the API
        club_members = await client.get_club_members(player.club.tag, limit=5) # Get Club Members with pagination
        after = club_members.paging.cursors.after # Get the 'after' cursor for pagination
        refetched_after_member = await client.get_club_members(player.club.tag, after=after, limit=5) # Refetch Club Members using the 'after' cursor
        refetched_before_member = await client.get_club_members(player.club.tag, before=club_members.paging.cursors.before, limit=5) # Refetch Club Members using the 'before' cursor
    
    await nb.close() # Close the HTTP client session

if __name__ == "__main__":
    asyncio.run(main()) # Run the main function
```

## Notes

- Make sure to replace the player tags and API token.
- Supports both numeric and #-prefixed tags.

## Donate Me 💖

If you like this project and want to support its development, you can donate:

- **PayPal:** [@NovaFenice](https://www.paypal.com/paypalme/novafenice)

Every contribution helps me maintain and improve the library! Thank you for your support! 🙏