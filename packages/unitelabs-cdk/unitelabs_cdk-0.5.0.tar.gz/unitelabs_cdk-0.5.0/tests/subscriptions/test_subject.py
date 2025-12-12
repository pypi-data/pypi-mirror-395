import asyncio
import re
import typing
import unittest.mock
import weakref

import pytest

from unitelabs.cdk.subscriptions import Subject, Subscription
from unitelabs.cdk.subscriptions.subject import _DEFAULT_VALUE

ONE_OP_TIME = 0.01


def first_pipe(x: str) -> str:
    return x.upper()


def second_pipe(x: str) -> dict[str, str]:
    return {"value": x}


async def redundant_update(subject: Subject[str]) -> None:
    """Update the subject 10x, once per operation time, with redundant updates after the first iteration."""
    for x in range(1, 11):
        if x > 1:
            subject.update(f"update {x - 1}")  # redundant update
        subject.update(f"update {x}")
        await asyncio.sleep(ONE_OP_TIME)


class TestDefaults:
    async def test_should_set_default_value_as_current(self):
        subject = Subject[str]()
        assert subject.current is _DEFAULT_VALUE

    async def test_should_set_default_maxsize(self):
        subject = Subject[str]()
        sub = subject.subscribe()
        assert sub.maxsize == 0

    async def test_should_allow_optional_value(self):
        subject = Subject[typing.Optional[str]](maxsize=10)
        subject.update(None)
        assert subject.current is None


class TestInit:
    async def test_should_type_check_pipe(self):
        # Requires visual check
        def invalid_pipe(x: int) -> str:
            return "value"

        Subject[str](maxsize=10, pipe=invalid_pipe)

    async def test_should_allow_pipe_function(self):
        def pipe_func(x: str) -> str:
            return x.lower()

        subject = Subject[str](maxsize=10, pipe=pipe_func)
        assert subject._pipe == pipe_func
        subject.update("TEST")
        assert subject.current == "test"


class TestUpdate:
    async def test_should_update_current_value(self):
        subject = Subject[str](maxsize=10)
        subject.update("new value")
        assert subject.current == "new value"

    async def test_should_notify_even_if_value_is_current(self):
        subject = Subject[str](maxsize=10)
        subject.update("new value")
        subject.notify = unittest.mock.Mock(wraps=subject.notify)
        assert isinstance(subject.current, str)
        subject.update(subject.current)
        subject.notify.assert_called_once()


class TestSubscribe:
    async def test_should_add_subscription(self):
        subject = Subject[str](maxsize=10)
        sub = subject.subscribe()
        assert sub in subject.subscribers

    async def test_should_not_set_current_value_on_subscription(self, create_task):
        subject = Subject[str](maxsize=10)
        FIRST_UPDATE = "first"
        subject.update(FIRST_UPDATE)
        assert subject.current == FIRST_UPDATE

        sub = subject.subscribe()
        assert subject.current == FIRST_UPDATE

        update_task = next(create_task(redundant_update(subject)))
        assert await sub.get() == "update 1"
        assert subject.current == "update 1"

        update_task.cancel()
        await asyncio.sleep(0.01)
        assert update_task.done()
        subject.unsubscribe(sub)


class TestOnSubscribe:
    async def test_should_trigger_on_subscription(self):
        subject = Subject[str](maxsize=10)
        subject.on_subscribe = unittest.mock.Mock(wraps=subject.on_subscribe)

        subject.subscribe()

        subject.on_subscribe.assert_called_once_with()

    async def test_should_trigger_on_child_subscription(self):
        subject = Subject[str](maxsize=10)
        subject.on_subscribe = unittest.mock.Mock(wraps=subject.on_subscribe)
        child_subject = subject.pipe(first_pipe).pipe(second_pipe)

        child_subject.subscribe()

        subject.on_subscribe.assert_called_once_with()

    async def test_should_trigger_only_on_first_subscription(self):
        subject = Subject[str](maxsize=10)
        subject.on_subscribe = unittest.mock.Mock(wraps=subject.on_subscribe)
        child_subject = subject.pipe(first_pipe).pipe(second_pipe)

        subject.subscribe()
        subject.on_subscribe.assert_called_once_with()
        subject.on_subscribe.reset_mock()

        subject.subscribe()
        child_subject.subscribe()
        subject.on_subscribe.assert_not_called()

    async def test_should_trigger_only_on_first_child_subscription(self):
        subject = Subject[str](maxsize=10)
        subject.on_subscribe = unittest.mock.Mock(wraps=subject.on_subscribe)
        child_subject = subject.pipe(first_pipe).pipe(second_pipe)

        child_subject.subscribe()
        subject.on_subscribe.assert_called_once_with()
        subject.on_subscribe.reset_mock()

        subject.subscribe()
        child_subject.subscribe()
        subject.on_subscribe.assert_not_called()


class TestOnUnsubscribe:
    async def test_should_trigger_on_unsubscription(self):
        subject = Subject[str](maxsize=10)
        subject.on_unsubscribe = unittest.mock.Mock(wraps=subject.on_unsubscribe)

        sub = subject.subscribe()
        subject.unsubscribe(sub)

        subject.on_unsubscribe.assert_called_once_with()

    async def test_should_trigger_on_child_unsubscription(self):
        subject = Subject[str](maxsize=10)
        subject.on_unsubscribe = unittest.mock.Mock(wraps=subject.on_unsubscribe)
        child_subject = subject.pipe(first_pipe).pipe(second_pipe)

        sub = child_subject.subscribe()
        subject.unsubscribe(sub)

        subject.on_unsubscribe.assert_called_once_with()

    async def test_should_trigger_only_on_last_unsubscription(self):
        subject = Subject[str](maxsize=10)
        subject.on_unsubscribe = unittest.mock.Mock(wraps=subject.on_unsubscribe)
        child_subject = subject.pipe(first_pipe).pipe(second_pipe)

        sub1 = subject.subscribe()
        sub2 = child_subject.subscribe()
        sub3 = subject.subscribe()

        subject.unsubscribe(sub1)
        child_subject.unsubscribe(sub2)
        subject.on_unsubscribe.assert_not_called()

        subject.unsubscribe(sub3)
        subject.on_unsubscribe.assert_called_once_with()

    async def test_should_trigger_only_on_last_child_unsubscription(self):
        subject = Subject[str](maxsize=10)
        subject.on_unsubscribe = unittest.mock.Mock(wraps=subject.on_unsubscribe)
        child_subject = subject.pipe(first_pipe).pipe(second_pipe)

        sub1 = subject.subscribe()
        sub2 = child_subject.subscribe()
        sub3 = child_subject.subscribe()

        subject.unsubscribe(sub1)
        subject.unsubscribe(sub2)
        subject.on_unsubscribe.assert_not_called()

        subject.unsubscribe(sub3)
        subject.on_unsubscribe.assert_called_once_with()


class TestUnsubscribe:
    async def test_should_remove_subscription(self):
        subject = Subject[str](maxsize=10)
        sub = subject.subscribe()
        assert sub in subject.subscribers
        subject.unsubscribe(sub)
        assert sub not in subject.subscribers

    async def test_should_raise_value_error_on_unknown_subscription(self):
        subject = Subject[str](maxsize=10)
        with pytest.raises(ValueError, match="Subscription not found in subscribers or children."):
            subject.unsubscribe(Subscription(10, parent=unittest.mock.Mock()))

    async def test_should_raise_value_error_on_twice_removed(self):
        subject = Subject[str](maxsize=10)
        sub = subject.subscribe()
        subject.unsubscribe(sub)
        with pytest.raises(ValueError, match="Subscription not found in subscribers or children."):
            subject.unsubscribe(sub)

    async def test_should_cancel_subscription(self):
        subject = Subject[str](maxsize=10)
        sub = subject.subscribe()
        sub.cancel = unittest.mock.Mock(wraps=sub.cancel)

        subject.unsubscribe(sub)

        sub.cancel.assert_called_once()
        assert sub not in subject.subscribers

        subject.update("value")
        assert not sub.size  # should not receive updates after being unsubscribed

    async def test_should_allow_unsubscribe_from_direct_parent_subject(self):
        subject = Subject[str](maxsize=10)
        child_subject = subject.pipe(first_pipe).pipe(second_pipe)

        sub = child_subject.subscribe()
        assert sub not in subject.subscribers
        assert sub in child_subject.subscribers

        subject.unsubscribe(sub)
        assert sub not in child_subject.subscribers

        with pytest.raises(TimeoutError):
            await sub.get(timeout=0.01)

    async def test_should_allow_unsubscribe_from_ancestral_parent_subject(self):
        subject = Subject[str](maxsize=10)
        child_subject = subject.pipe(first_pipe).pipe(second_pipe)

        sub = child_subject.subscribe()
        assert sub not in subject.subscribers
        assert sub in child_subject.subscribers

        subject.unsubscribe(sub)
        assert sub not in child_subject.subscribers

        with pytest.raises(TimeoutError):
            await sub.get(timeout=0.01)

    async def test_should_not_allow_unsubscribe_from_sibling_subject(self):
        subject = Subject[str](maxsize=10)
        child_subject = subject.pipe(first_pipe).pipe(second_pipe)
        other_subject = subject.pipe(second_pipe)

        sub = child_subject.subscribe()
        assert sub not in subject.subscribers
        assert sub in child_subject.subscribers

        with pytest.raises(ValueError, match="Subscription not found in subscribers or children."):
            other_subject.unsubscribe(sub)

    async def test_should_prune_temporary_child_subjects(self):
        subject = Subject[str](maxsize=10)
        child_subject = subject.pipe(first_pipe, temporary=True)
        grandchild_subject = child_subject.pipe(second_pipe, temporary=True)

        sub = grandchild_subject.subscribe()
        assert subject._children
        assert subject._children[0]._children

        subject.unsubscribe(sub)
        assert not subject._children

    async def test_should_not_prune_child_subjects_with_subscriptions(self):
        subject = Subject[str](maxsize=10)
        child_subject = subject.pipe(first_pipe)
        temp_child_subject = child_subject.pipe(second_pipe, temporary=True)

        child_subject.subscribe()
        temp_grandchild_sub = temp_child_subject.subscribe()

        assert child_subject in subject._children
        assert temp_child_subject in child_subject._children

        subject.unsubscribe(temp_grandchild_sub)
        assert child_subject in subject._children
        assert not child_subject._children

    async def test_should_not_prune_parent_subjects_with_subscriptions(self):
        subject = Subject[str](maxsize=10)
        temp_child_subject = subject.pipe(first_pipe, temporary=True)
        assert temp_child_subject in subject._children

        with pytest.raises(
            RuntimeError,
            match=(
                re.escape(
                    "Cannot create a non-temporary `Subject` from a temporary `Subject`, use pipe() with `temporary=True` "
                    "or adjust the current `Subject` to be non-temporary."
                )
            ),
        ):
            temp_child_subject.pipe(second_pipe)


class TestPipes:
    async def test_should_type_check_pipes(self):
        # Requires visual check
        def invalid_pipe(x: int) -> str:
            return "value"

        subject = Subject[str](maxsize=10)
        subject.pipe(invalid_pipe)

    async def test_should_create_new_subject(self):
        subject = Subject[str](maxsize=10)
        piped = subject.pipe(first_pipe).pipe(second_pipe)

        assert isinstance(piped, Subject)
        assert piped != subject

    async def test_should_not_set_pipes_on_current_subject(self):
        subject = Subject[str](maxsize=10)
        start_pipe = subject._pipe

        upper_subject = subject.pipe(first_pipe)
        assert subject._pipe == start_pipe
        assert upper_subject._pipe == first_pipe

        to_dict_subject = subject.pipe(second_pipe)
        assert subject._pipe == start_pipe
        assert to_dict_subject._pipe == second_pipe

        # test that pipes are applied correctly
        upper_subscription = upper_subject.subscribe()
        to_dict_subscription = to_dict_subject.subscribe()

        subject.update("value")
        assert await upper_subscription.get() == "VALUE"
        assert await to_dict_subscription.get() == {"value": "value"}

    async def test_should_track_child_subscription(self):
        subject = Subject[str](maxsize=10)
        piped = subject.pipe(first_pipe).pipe(second_pipe)

        sub = piped.subscribe()

        assert subject._children[0]._pipe == first_pipe
        assert subject._children[0]._children[0]._pipe == second_pipe

        assert sub in piped.subscribers
        assert piped._parent._parent == weakref.proxy(subject)

        # cleanup
        piped.unsubscribe(sub)

    async def test_should_update_value_in_all_child_subjects(self):
        subject = Subject[str](maxsize=10)
        sub = subject.subscribe()
        sub.update = unittest.mock.Mock(wraps=sub.update)

        piped = subject.pipe(first_pipe).pipe(second_pipe)
        piped.update = unittest.mock.Mock(wraps=piped.update)

        piped_sub = piped.subscribe()
        piped_sub.update = unittest.mock.Mock(wraps=piped_sub.update)

        subject.update("value")

        sub.update.assert_called_once_with("value")
        piped.update.assert_called_once_with("VALUE")
        piped_sub.update.assert_called_once_with({"value": "VALUE"})
        assert await sub.get() == "value"
        assert await piped_sub.get() == {"value": "VALUE"}

        # cleanup
        for s in [sub, piped_sub]:
            subject.unsubscribe(s)


class TestFilter:
    async def test_should_allow_filtering(self):
        subject = Subject[str](maxsize=10)
        subscription = subject.subscribe()
        filtered = subject.filter(lambda x: x and "filter" not in x)
        filtered.update = unittest.mock.Mock(wraps=filtered.update)
        filtered_subscription = filtered.subscribe()
        filtered_subscription.update = unittest.mock.Mock(wraps=filtered_subscription.update)

        subject.update("filter this")
        filtered.update.assert_called_once_with("filter this")
        filtered_subscription.update.assert_not_called()
        assert filtered_subscription.empty()
        assert await subscription.get() == "filter this"

    async def test_should_pass_filtering(self):
        subject = Subject[str](maxsize=10)
        subscription = subject.subscribe()
        filtered = subject.filter(lambda x: x and "filter" not in x)
        filtered.update = unittest.mock.Mock(wraps=filtered.update)
        filtered_subscription = filtered.subscribe()
        filtered_subscription.update = unittest.mock.Mock(wraps=filtered_subscription.update)

        subject.update("pass")
        filtered.update.assert_called_once_with("pass")
        filtered_subscription.update.assert_called_once_with("pass")
        assert await filtered_subscription.get() == "pass"
        assert await subscription.get() == "pass"

    async def test_should_prune_from_parent_if_temporary(self):
        subject = Subject[int](maxsize=10)
        filtered = subject.filter(lambda x: x > 5, temporary=True)
        assert filtered in subject._children

        filtered_subscription = filtered.subscribe()
        assert filtered_subscription._parent._is_temporary

        subject.unsubscribe(filtered_subscription)
        assert filtered not in subject._children


class TestContextManager:
    async def test_should_subscribe_on_enter(self):
        subject = Subject[str](maxsize=10)

        with subject as subscription:
            assert subscription in subject.subscribers

    async def test_should_unsubscribe_on_exit(self):
        subject = Subject[str](maxsize=10)

        with subject:
            pass

        assert not subject.subscribers

    async def test_should_raise_on_nested_contexts(self):
        subject = Subject[str](maxsize=10)

        with subject, pytest.raises(RuntimeError), subject:
            pass

        assert not subject.subscribers

    async def test_should_reset__context(self):
        subject = Subject[int](maxsize=10)
        with subject as subscription:
            assert subscription in subject.subscribers
        with subject as subscription:
            assert subscription in subject.subscribers

    async def test_should_allow_and_tear_down_temporary_pipe(self):
        subject = Subject[int](maxsize=10)
        with subject.pipe(lambda x: x * 2, temporary=True) as subscription:
            for i in range(10):
                subject.update(i)
                value = await subscription.get()
                assert value == i * 2

        assert not subject.subscribers
        assert not subject._children


class TestSubscription_Get:
    async def test_should_get_new_value(self):
        subject = Subject[str](maxsize=10)
        subscription: Subscription[str] = subject.subscribe()
        subscription.update = unittest.mock.Mock(wraps=subscription.update)

        for i in range(10):
            msg = f"update {i}"
            subject.update(msg)
            subscription.update.assert_called_with(msg)
            assert await subscription.get() == msg

        # cleanup
        subject.unsubscribe(subscription)

    async def test_should_timeout_if_nothing_queued(self):
        subject = Subject[str](maxsize=10)
        subscription: Subscription[str] = subject.subscribe()
        with pytest.raises(TimeoutError):
            await subscription.get(timeout=0.05)

        # cleanup
        subject.unsubscribe(subscription)

    async def test_should_timeout_if_nothing_matches_predicate(self, create_task):
        subject = Subject[str](maxsize=10)
        update_task = next(create_task(redundant_update(subject)))
        subscription: Subscription[str] = subject.subscribe()

        with pytest.raises(TimeoutError):
            await subscription.get(lambda x: "value" in x, timeout=0.05)

        # cleanup
        update_task.cancel()
        await asyncio.sleep(0.01)
        assert update_task.done()
        subject.unsubscribe(subscription)

    async def test_should_not_set_subject_current_value_on_new_subscriptions(self):
        subject = Subject[Exception](maxsize=10)
        subscription = subject.subscribe()

        exception = ValueError("Test exception")
        subject.update(exception)

        expected_exception = await subscription.get(lambda x: isinstance(x, ValueError))
        assert expected_exception == exception
        assert subject._value == exception

        new_subscription = subject.subscribe()
        with pytest.raises(TimeoutError):
            await new_subscription.get(lambda x: isinstance(x, ValueError), timeout=0.05)
        assert subject._value == exception

        # cleanup
        for s in [subscription, new_subscription]:
            subject.unsubscribe(s)
