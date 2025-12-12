import asyncio
import re
import unittest.mock

import pytest

from sila.framework.common.stream import QueueShutDown, Stream


class TestStream:
    async def test_should_push_and_consume_item(self):
        # Create stream
        stream = Stream()

        # Push
        stream.next(unittest.mock.sentinel.item)
        stream.close()

        # Consume
        assert await stream.get() == unittest.mock.sentinel.item

    async def test_should_consume_items_in_lifo_order(self):
        # Create stream
        stream = Stream()

        # Push
        stream.next(unittest.mock.sentinel.item_0)
        stream.next(unittest.mock.sentinel.item_1)
        stream.next(unittest.mock.sentinel.item_2)
        stream.close()

        # Consume
        results = [item async for item in stream]

        assert results == [
            unittest.mock.sentinel.item_0,
            unittest.mock.sentinel.item_1,
            unittest.mock.sentinel.item_2,
        ]

    async def test_should_limit_maxsize(self):
        # Create stream
        stream = Stream(maxsize=1)

        # Push
        stream.next(unittest.mock.sentinel.item_0)
        stream.next(unittest.mock.sentinel.item_1)
        stream.next(unittest.mock.sentinel.item_2)
        stream.close()

        # Consume
        results = [item async for item in stream]

        assert results == [
            unittest.mock.sentinel.item_2,
        ]

    async def test_size(self):
        # Create stream
        stream = Stream()

        # Push
        stream.next(unittest.mock.sentinel.item_0)
        stream.next(unittest.mock.sentinel.item_1)
        stream.next(unittest.mock.sentinel.item_2)
        stream.close()

        assert stream.size == 4

    async def test_should_close_without_items(self):
        # Create stream
        stream = Stream()

        # Close
        stream.close()

        # Consume
        results = [item async for item in stream]

        assert results == []

    async def test_should_raise_after_timeout(self):
        # Create stream
        stream = Stream()

        # Next
        with pytest.raises(TimeoutError):
            await stream.get(timeout=0)

    async def test_should_raise_after_close(self):
        # Create stream
        stream = Stream()

        # Next
        task = asyncio.get_running_loop().call_soon(stream.close)
        with pytest.raises(TimeoutError):
            await stream.get(timeout=0.1)

        task.cancel()

    async def test_should_raise_on_push_after_close(self):
        # Create stream
        stream = Stream()

        # Close
        stream.close()

        # Push
        with pytest.raises(QueueShutDown, match=re.escape("Cannot push to a closed queue.")):
            stream.next(unittest.mock.sentinel.item)

    async def test_should_handle_cancel(self):
        # Create stream
        stream = Stream()

        async def iterate():
            return [item async for item in stream]

        # Close
        task = asyncio.create_task(iterate())
        await asyncio.sleep(0)
        task.cancel()

        await asyncio.sleep(0)
        task.result()
