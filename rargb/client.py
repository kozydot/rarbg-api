import asyncio
import httpx
from bs4 import BeautifulSoup
from .leakybucket import LeakyBucket
from .exceptions import APIError

class Client:
    def __init__(self, rate_limit=2, capacity=1):
        self.base_url = "https://rargb.to"
        self._bucket = LeakyBucket(rate_limit, capacity)
        self._client = httpx.AsyncClient()

    async def search(self, query, categories=None, limit=25):
        results = []
        page = 1
        while len(results) < limit:
            if not await self._bucket.acquire(1, timeout=5):
                raise APIError("Rate limit exceeded")

            url = f"{self.base_url}/search/{page}/?search={query}"
            if categories:
                for category in categories:
                    url += f"&category[]={category.value}"
            try:
                response = await self._client.get(url)
                response.raise_for_status()
            except httpx.RequestError as e:
                raise APIError(f"Request failed: {e}")

            soup = BeautifulSoup(response.text, 'html.parser')
            
            rows = soup.find_all('tr', class_='lista2')
            if not rows:
                break

            tasks = []
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 6:
                    link = cells[1].find('a')
                    if link:
                        torrent_url = self.base_url + link.get('href')
                        tasks.append(self._get_magnet_link(torrent_url))

            magnet_links = await asyncio.gather(*tasks)

            for i, row in enumerate(rows):
                cells = row.find_all('td')
                if len(cells) > 6:
                    link = cells[1].find('a')
                    if link:
                        results.append({
                            'title': link.get('title'),
                            'url': self.base_url + link.get('href'),
                            'magnet_link': magnet_links[i],
                            'category': cells[2].text,
                            'added': cells[3].text,
                            'size': cells[4].text,
                            'seeders': cells[5].text,
                            'leechers': cells[6].text
                        })
                if len(results) >= limit:
                    break
            page += 1
        return results

    async def _get_magnet_link(self, url):
        if not await self._bucket.acquire(1, timeout=5):
            raise APIError("Rate limit exceeded")
        try:
            response = await self._client.get(url)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {e}")

        soup = BeautifulSoup(response.text, 'html.parser')
        magnet_link = soup.find('a', {'href': lambda x: x and x.startswith('magnet:')})
        return magnet_link.get('href') if magnet_link else None

    async def close(self):
        await self._client.aclose()