import unittest
from rargb.client import Client

class TestClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = Client()

    async def test_search(self):
        results = await self.client.search("test")
        self.assertIsInstance(results, list)
        if results:
            self.assertIn('title', results[0])
            self.assertIn('url', results[0])

    async def asyncTearDown(self):
        await self.client.close()

if __name__ == '__main__':
    unittest.main()