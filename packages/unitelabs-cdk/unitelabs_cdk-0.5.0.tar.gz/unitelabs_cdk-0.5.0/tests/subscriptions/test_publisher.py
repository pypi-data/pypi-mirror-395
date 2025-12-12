import asyncio
import functools
import unittest.mock
import weakref

import pytest

from unitelabs.cdk.subscriptions import Publisher, Subject

ONE_OP_TIME = 0.01


def first_pipe(x: str) -> str:
    return x.upper()


def second_pipe(x: str) -> dict[str, str]:
    return {"value": x}


class TestSource:
    async def test_should_allow_coroutine_as_source(self):
        msg = "value"

        async def source() -> str:
            return msg

        pub = Publisher[str](source=source, interval=ONE_OP_TIME)
        sub = pub.subscribe()
        assert await sub.get() == msg

        pub.unsubscribe(sub)

    async def test_should_allow_callable_as_source(self):
        msg = "value"

        def source() -> str:
            return msg

        pub = Publisher[str](source=source, interval=ONE_OP_TIME)
        sub = pub.subscribe()
        assert await sub.get() == msg

        pub.unsubscribe(sub)

    async def test_should_allow_partial_coroutine_as_source(self):
        msg = "value"

        async def source(msg: str) -> str:
            return msg

        pub = Publisher[str](source=functools.partial(source, msg), interval=ONE_OP_TIME)
        sub = pub.subscribe()
        assert await sub.get() == msg

        pub.unsubscribe(sub)

    async def test_should_allow_partial_callable_as_source(self):
        msg = "value"

        def source(msg: str) -> str:
            return msg

        pub = Publisher[str](source=functools.partial(source, msg), interval=ONE_OP_TIME)
        sub = pub.subscribe()
        assert await sub.get() == msg

        pub.unsubscribe(sub)

    async def test_should_type_check_source(self):
        # Requires visual check
        def source() -> str:
            return "value"

        pub = Publisher[int](source=source, interval=ONE_OP_TIME)
        sub = pub.subscribe()
        assert await sub.get() == "value"

        pub.unsubscribe(sub)


class TestInit:
    async def test_should_allow_pipe_function(self):
        def pipe_func(x: str) -> str:
            return x.upper()

        pub = Publisher[str](source=lambda: "value", interval=ONE_OP_TIME, pipe=pipe_func)
        sub = pub.subscribe()

        assert await sub.get() == "VALUE"

        pub.unsubscribe(sub)


class TestSubscribe:
    async def test_should_start_polling_after_add(self):
        mock = unittest.mock.Mock(side_effect=[f"value {i}" for i in range(10)])
        pub = Publisher[str](maxsize=10, source=mock, interval=ONE_OP_TIME)
        pub._set = unittest.mock.Mock(wraps=pub._set)

        assert not pub._update_task
        mock.assert_not_called()

        sub = pub.subscribe()
        pub._set.assert_called_once()
        await asyncio.sleep(ONE_OP_TIME)

        assert sub.size >= 1
        mock.assert_called()
        assert pub._update_task

        pub.unsubscribe(sub)

    async def test_should_not_start_polling_again_if_other_subscribers(self):
        pub = Publisher[str](maxsize=10, source=lambda: "value", interval=ONE_OP_TIME)
        pub._set = unittest.mock.Mock(wraps=pub._set)
        assert not pub._update_task

        sub = pub.subscribe()
        assert pub._update_task
        pub._set.assert_called_once()
        pub._set.reset_mock()

        sub2 = pub.subscribe()
        pub._set.assert_not_called()

        for s in [sub, sub2]:
            pub.unsubscribe(s)

    async def test_should_add_current_value_to_new_subscription(self):
        mock = unittest.mock.Mock(side_effect=[f"value {i}" for i in range(10)])
        pub = Publisher[str](maxsize=10, source=mock, interval=ONE_OP_TIME)

        value = "value"
        pub.update(value)

        sub1 = pub.subscribe()
        assert await sub1.get() == value
        mock.assert_not_called()

        sub2 = pub.subscribe()
        assert await sub2.get() == value
        mock.assert_not_called()

        pub.unsubscribe(sub1)
        pub.unsubscribe(sub2)


class TestUnsubscribe:
    async def test_should_cancel_update_task_if_no_subscribers(self):
        # create a data generator for the publisher
        x = 0

        async def get_next_value() -> str:
            nonlocal x
            x += 1
            return f"update {x}"

        pub = Publisher[str](maxsize=10, source=get_next_value, interval=ONE_OP_TIME)
        assert not pub._update_task

        # create subscription and let it run for a while
        sub = pub.subscribe()
        iterations = 5
        await asyncio.sleep(ONE_OP_TIME * iterations)

        # check that internals are set and queue is being populated
        assert sub.size >= iterations
        assert pub._update_task

        # save a reference to the task and remove the subscription
        task = pub._update_task
        pub.unsubscribe(sub)

        # check that internals from source are cleared
        assert not pub._update_task

        # give the task some to time to be gracefully cancelled
        await asyncio.sleep(0.01)
        assert task.cancelled()

    async def test_should_not_cancel_update_task_if_other_subscribers(self):
        # create a data generator for the publisher
        x = 0

        async def get_next_value() -> str:
            nonlocal x
            x += 1
            return f"update {x}"

        pub = Publisher[str](maxsize=10, source=get_next_value, interval=ONE_OP_TIME)
        assert not pub._update_task

        # create two subscriptions and let them run for a while
        sub1 = pub.subscribe()
        sub2 = pub.subscribe()
        iterations = 5
        await asyncio.sleep(ONE_OP_TIME * iterations)

        # check that internals are set and queue is being populated
        assert sub1.size >= iterations
        assert sub2.size >= iterations
        assert pub._update_task

        # save a reference to the task and remove one subscription
        task = pub._update_task
        pub.unsubscribe(sub1)

        # check that internals from source are not cleared
        size_before = sub2.size
        await asyncio.sleep(ONE_OP_TIME)
        assert sub2.size >= size_before
        assert pub._update_task == task

        pub.unsubscribe(sub2)
        assert not pub._update_task


class TestPipe:
    async def test_should_type_check_pipes(self):
        # Requires visual check
        def invalid_pipe(x: int) -> str:
            return "value"

        pub = Publisher[str](source=lambda: "value", interval=ONE_OP_TIME)
        pub.pipe(invalid_pipe)

    async def test_should_create_new_publisher(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](source=mock, interval=ONE_OP_TIME, maxsize=10)

        piped = pub.pipe(first_pipe).pipe(second_pipe)
        assert piped._pipe == second_pipe

        assert piped != pub
        assert isinstance(piped, Subject)

    async def test_should_add_subscription_to_new_publisher_only(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](source=mock, interval=ONE_OP_TIME, maxsize=10)

        piped = pub.pipe(first_pipe).pipe(second_pipe)
        assert piped._pipe == second_pipe
        sub = piped.subscribe()

        assert sub in piped.subscribers
        assert sub not in pub.subscribers
        assert piped._parent._parent == weakref.proxy(pub)

        # cleanup
        piped.unsubscribe(sub)

    async def test_should_update_piped_subscription(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](source=mock, interval=ONE_OP_TIME, maxsize=10)

        piped = pub.pipe(first_pipe).pipe(second_pipe)
        piped.update = unittest.mock.Mock(wraps=piped.update)
        sub = piped.subscribe()

        for i in range(10):
            value = await sub.get()
            piped.update.assert_called_with(f"UPDATE {i}")
            assert value == {"value": f"UPDATE {i}"}
            assert mock.call_count == i + 1

        # cleanup
        piped.unsubscribe(sub)
        assert not pub._update_task

    async def test_should_not_remove_update_task_if_parent_publisher_has_subscription(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](source=mock, interval=ONE_OP_TIME, maxsize=10)
        main_sub = pub.subscribe()

        # create piped subjects
        first_piped = pub.pipe(first_pipe)
        second_piped = first_piped.pipe(second_pipe)

        sub1 = first_piped.subscribe()
        sub2 = second_piped.subscribe()

        # use piped subjects to get values
        for i in range(10):
            if i == 5:
                pub.unsubscribe(sub1)
            if i < 5:
                # sub1 is still subscribed
                assert await sub1.get() == f"UPDATE {i}"
            assert await sub2.get() == {"value": f"UPDATE {i}"}

            assert pub._update_task
            assert mock.call_count == i + 1

        # ensure that publisher's update task is still active after unsubscribing from all piped subjects
        pub.unsubscribe(sub2)
        assert pub._update_task

        pub.unsubscribe(main_sub)
        assert not pub._update_task


class TestFilter:
    async def test_should_filter_values(self):
        mock = unittest.mock.Mock(side_effect=list(range(10)))
        pub = Publisher[int](source=mock, interval=ONE_OP_TIME, maxsize=10)

        filtered_pub = pub.filter(lambda x: x > 2)
        filtered_pub.update = unittest.mock.Mock(wraps=filtered_pub.update)

        sub = pub.subscribe()
        filtered_sub = filtered_pub.subscribe()
        await asyncio.sleep(ONE_OP_TIME * 5)
        assert await sub.get() == 0
        assert await filtered_sub.get() == 3

        for s in [sub, filtered_sub]:
            pub.unsubscribe(s)


class TestSubscription_Get:
    async def test_should_get_new_value(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](source=mock, interval=ONE_OP_TIME, maxsize=10)

        sub = pub.subscribe()

        for i in range(10):
            value = await sub.get()
            assert value == f"update {i}"
            assert pub.current == f"update {i}"
            assert mock.call_count == i + 1

        # cleanup
        pub.unsubscribe(sub)

    async def test_should_timeout_if_nothing_matches_predicate(self):
        mock = unittest.mock.Mock(side_effect=[f"update {i}" for i in range(10)])
        pub = Publisher[str](source=mock, interval=ONE_OP_TIME, maxsize=10)

        sub = pub.subscribe()
        with pytest.raises(TimeoutError):
            value = await sub.get(lambda x: "value" in x, timeout=0.05)

        # cleanup
        pub.unsubscribe(sub)
