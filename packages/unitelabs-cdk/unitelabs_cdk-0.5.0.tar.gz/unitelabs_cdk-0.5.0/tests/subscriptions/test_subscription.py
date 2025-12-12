import asyncio
import time
import unittest.mock

import pytest

from unitelabs.cdk.subscriptions import Subject, Subscription

ONE_OP_TIME = 0.01


class TestMaxsize:
    async def test_should_limit_queue_size(self):
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        for i in range(10):
            sub.update(f"value{i}")
        assert sub.size == 10

        with pytest.raises(asyncio.QueueFull):
            sub.update("value11")

        assert sub.size == 10


class TestSize:
    async def test_should_return_current_size(self):
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        assert sub.size == 0

        sub.update("value")
        assert sub.size == 1

        await sub.get()
        assert sub.size == 0


class TestUpdate:
    async def test_should_allow_none_value_in_subscription(self):
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        values_added = ["value", None]
        for value in values_added:
            sub.update(value)

        seen = []
        async for value in sub:
            if value is None:
                sub.cancel()

            seen.append(value)
        assert seen == values_added

    async def test_should_not_update_same_value(self):
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        sub.put_nowait = unittest.mock.Mock(wraps=sub.put_nowait)

        # update twice
        sub.update("value")
        sub.update("value")

        assert sub._value == "value"
        sub.put_nowait.assert_called_once_with("value")


class TestCancel:
    async def test_should_stop_waiting_for_queue_task_after_cancel(self):
        callback = unittest.mock.Mock()
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        sub.cancel()

        async for value in sub:
            # this is never executed because the iterator is immediately exited
            callback(value)

        await asyncio.sleep(ONE_OP_TIME * 2)
        callback.assert_not_called()

    async def test_should_stop_iterating_after_cancel_in_loop(self):
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        values = [f"value{i}" for i in range(1, 5)]
        for value in values:
            sub.update(value)

        seen = []
        async for value in sub:
            if value == values[2]:
                sub.cancel()

            seen.append(value)
        assert seen == values[:3]

    async def test_should_stop_iterating_after_cancel(self):
        start_time = time.perf_counter()
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        N_OPS = 5

        async def make_updates():
            for i in range(10):
                sub.update(f"value{i}")
                await asyncio.sleep(ONE_OP_TIME)

                if i == N_OPS - 1:
                    sub.cancel()

        update_task = asyncio.create_task(make_updates())

        seen = [value async for value in sub]
        assert seen == [f"value{i}" for i in range(N_OPS)]
        assert time.perf_counter() - start_time == pytest.approx(ONE_OP_TIME * (N_OPS + 1), rel=1e3)

        await update_task


class TestTerminate:
    async def test_should_remove_subscription(self):
        subject = Subject[str](maxsize=10)
        sub = subject.subscribe()
        assert sub in subject.subscribers
        sub.terminate()
        assert sub not in subject.subscribers


class TestAsyncIterator:
    async def test_should_clear_tasks_after_each_iteration(self):
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        for i in range(10):
            sub.update(f"value{i}")

        async for value in sub:
            assert "value" in value
            await asyncio.sleep(ONE_OP_TIME / 10)
            assert not sub._closed.is_set()
            if "9" in value:
                break

    async def test_should_raise_stop_iteration(self):
        # create a subscription and populate it with values
        sub = Subscription[str](10, parent=unittest.mock.Mock())

        task = asyncio.create_task(sub.__anext__())
        await asyncio.sleep(0)
        task.cancel()

        with pytest.raises(StopAsyncIteration):
            await task


class TestGet:
    async def test_should_get_new_value(self):
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        for i in range(10):
            msg = f"value{i}"
            sub.update(msg)
            assert await sub.get() == msg

    async def test_should_return_value_if_matches_predicate(self):
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        msgs = [f"value{i}" for i in range(9)]
        msgs.insert(5, "find me 5")
        for msg in msgs:
            sub.update(msg)

        assert await sub.get(lambda x: "find me" in x) == "find me 5"

    async def test_should_timeout_if_nothing_in_queue(self):
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        with pytest.raises(TimeoutError):
            await sub.get(timeout=0.05)

    async def test_should_timeout_if_nothing_matches_predicate(self):
        # create a subscription and populate it with values
        sub = Subscription[str](10, parent=unittest.mock.Mock())
        for value in [f"value {i}" for i in range(10)]:
            sub.update(value)

        with pytest.raises(TimeoutError):
            await sub.get(lambda x: "find me" in x, timeout=0.05)

    async def test_should_cycle_through_queued_items_until_match(self, create_task):
        sub = Subscription[str](10, parent=unittest.mock.Mock())

        # create a mock filter predicate to monitor how many times it was called
        def predicate(x: str) -> bool:
            return "5" in x

        mock_predicate = unittest.mock.Mock(wraps=predicate)

        # create background update task
        async def make_updates():
            for i in range(10):
                sub.update(f"value {i}")
                await asyncio.sleep(ONE_OP_TIME)

        update_task = next(create_task(make_updates()))

        assert await sub.get(mock_predicate) == "value 5"
        assert mock_predicate.call_count == 6

        # cleanup
        update_task.cancel()
        await asyncio.sleep(ONE_OP_TIME)
        assert update_task.done()
