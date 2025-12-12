import re
import unittest.mock

import pytest

from unitelabs.cdk.sila.common.decorator import Decorator
from unitelabs.cdk.sila.common.feature import Feature


class TestAttach:
    def test_should_attach_decorator(self):
        # Create Feature
        mock = unittest.mock.Mock()

        class TestFeature(Feature):
            @Decorator()
            def test(self):
                mock(self)

        feature = TestFeature()

        # Attach decorator
        attached = feature.attach()

        # Assert that the method returns the correct value
        assert attached is True
        assert "Test" in feature._handlers
        assert feature._handlers["Test"]._function.func == TestFeature.test
        assert feature._handlers["Test"]._feature == feature

        feature.test()
        mock.assert_called_once_with(feature)

    def test_should_attach_multiple_decorators(self):
        # Create Feature
        mock = unittest.mock.Mock()

        class TestFeature(Feature):
            @Decorator()
            def test(self):
                mock(self)

        feature1 = TestFeature()
        feature2 = TestFeature()

        # Attach decorator
        attached1 = feature1.attach()
        attached2 = feature2.attach()

        # Assert that the method returns the correct value
        assert attached1 is True
        assert "Test" in feature1._handlers
        assert feature1._handlers["Test"]._function.func == TestFeature.test
        assert feature1._handlers["Test"]._feature == feature1

        assert attached2 is True
        assert "Test" in feature2._handlers
        assert feature2._handlers["Test"]._function.func == TestFeature.test
        assert feature2._handlers["Test"]._feature == feature2

        feature1.test()
        mock.assert_called_once_with(feature1)

        mock.reset_mock()

        feature2.test()
        mock.assert_called_once_with(feature2)

    def test_should_raise_on_duplicate_handler(self):
        # Create Feature
        mock = unittest.mock.Mock()

        class TestFeature(Feature):
            @Decorator(name="Test")
            def test1(self):
                mock(self)

            @Decorator(name="Test")
            def test2(self):
                mock(self)

        feature = TestFeature()

        # Attach decorator
        with pytest.warns(
            UserWarning,
            match=re.escape(
                "Duplicate handler identifier 'Test' detected for feature 'TestFeature'. "
                "Existing: TestFeature.test1. New: TestFeature.test2 (will override). "
                "To avoid unintended overrides, set a unique 'identifier' in your decorator "
                "or rename one of the methods."
            ),
        ):
            feature.attach()
