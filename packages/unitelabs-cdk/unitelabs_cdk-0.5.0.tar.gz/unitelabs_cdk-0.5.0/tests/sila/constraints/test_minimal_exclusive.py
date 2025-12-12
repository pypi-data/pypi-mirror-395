import datetime
import unittest.mock
import zoneinfo

import pytest

from unitelabs.cdk import sila
from unitelabs.cdk.sila.constraints import MinimalExclusive


class TestValidate:
    @pytest.mark.parametrize(
        "value,validation,error",
        [
            pytest.param(10, sila.data_types.Integer(11), False, id="valid-int"),
            pytest.param(10, sila.data_types.Integer(10), True, id="invalid-int"),
            pytest.param(10.5, sila.data_types.Real(10.6), False, id="valid-float"),
            pytest.param(10.5, sila.data_types.Real(10.5), True, id="invalid-float"),
            pytest.param(datetime.date(2023, 1, 1), sila.data_types.Date(2023, 1, 2), False, id="valid-date"),
            pytest.param(datetime.date(2023, 1, 1), sila.data_types.Date(2023, 1, 1), True, id="invalid-date"),
            pytest.param(
                datetime.time(12, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("US/Eastern")),
                sila.data_types.Time(12, 0, 0, 1),
                False,
                id="valid-time",
            ),
            pytest.param(
                datetime.time(12, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("US/Eastern")),
                sila.data_types.Time(12, 0, 0, 0),
                True,
                id="invalid-time",
            ),
            pytest.param(
                datetime.datetime(2023, 1, 1, 12, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("US/Eastern")),
                sila.data_types.Timestamp(2023, 1, 1, 12, 0, 0, 1),
                False,
                id="valid-timestamp",
            ),
            pytest.param(
                datetime.datetime(2023, 1, 1, 12, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("US/Eastern")),
                sila.data_types.Timestamp(2023, 1, 1, 12, 0, 0, 0),
                True,
                id="invalid-timestamp",
            ),
        ],
    )
    async def test_validation(self, value, validation, error):
        constraint = MinimalExclusive(value)
        if not error:
            assert await constraint.validate(validation)
        else:
            with pytest.raises(ValueError):
                await constraint.validate(validation)

    async def test_should_raise_type_error_unsupported_type(self):
        with pytest.raises(TypeError):
            MinimalExclusive(unittest.mock.Mock())
