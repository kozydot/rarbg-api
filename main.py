from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from rargb.client import Client
from rargb.exceptions import APIError
from enum import Enum

class Category(str, Enum):
    all = "all"
    movies = "movies"
    xxx = "xxx"
    tv = "tv"
    games = "games"
    music = "music"
    anime = "anime"
    apps = "apps"
    doc = "doc"
    other = "other"
    nonxxx = "nonxxx"

app = FastAPI(
    title="Unofficial RARBG API",
    description="A web API for the unofficial RARBG API wrapper.",
    version="1.0.0"
)

rargb_client = Client()

@app.on_event("shutdown")
async def shutdown_event():
    await rargb_client.close()

@app.get("/search")
async def search(query: str, category: Category = Query(Category.all, description="Select a category to filter results"), limit: int = 25):
    """
    Search for torrents on RARBG.
    """
    try:
        categories = [category] if category != Category.all else None
        results = await rargb_client.search(query, categories, limit)
        return {"results": results}
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")