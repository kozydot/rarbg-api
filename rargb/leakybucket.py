import asyncio
import time

class LeakyBucket:
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.last_check = time.time()
        self.allowance = capacity
        self._lock = asyncio.Lock()

    async def acquire(self, tokens, timeout=None):
        async with self._lock:
            start_time = time.time()
            while True:
                now = time.time()
                self.allowance += (now - self.last_check) * self.rate
                self.last_check = now
                if self.allowance > self.capacity:
                    self.allowance = self.capacity
                if self.allowance >= tokens:
                    self.allowance -= tokens
                    return True
                if timeout is not None and (now - start_time) > timeout:
                    return False
                await asyncio.sleep(0.1)