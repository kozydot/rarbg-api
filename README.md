# Unofficial RARBG API Wrapper

This project is a Python wrapper for rargb.to. Since the official API is no longer available, this wrapper scrapes the website to provide a similar interface.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a Library

```python
import asyncio
from rargb.client import Client

async def main():
    # Initialize the client
    client = Client()

    # Search for torrents with category filtering
    results = await client.search("test", categories=["movies", "tv"])

    # Print the results
    for result in results:
        print(result)
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### As a Web API

To run the FastAPI server, use the following command:

```bash
uvicorn main:app --reload
```

Then, you can access the API at `http://127.0.0.1:8000/docs`. You can filter by category by passing the `categories` query parameter, like so: `http://127.0.0.1:8000/search?query=test&categories=movies&categories=tv`

### Available Categories

- `movies`
- `xxx`
- `tv`
- `games`
- `music`
- `anime`
- `apps`
- `doc`
- `other`
- `nonxxx`

Made with ❤️ by Kozydot

*Note: I might add rotating proxy support in the future.*
