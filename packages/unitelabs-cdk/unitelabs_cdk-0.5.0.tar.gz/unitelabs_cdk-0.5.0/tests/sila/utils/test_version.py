import itertools

import pytest

from unitelabs.cdk.sila.utils.version import parse_version

versions = [
    # Final releases
    pytest.param("0.0.0", "0.0", id="final"),
    pytest.param("1.0.0", "1.0", id="final"),
    pytest.param("1.2.3", "1.2.3", id="final"),
    pytest.param("1.2.03", "1.2.3", id="final"),
    pytest.param("v1.2.3", "1.2.3", id="final"),
    pytest.param("2012.10", "2012.10", id="date-based"),
    # Pre-releases
    *[
        pytest.param("".join(v), "1.2.3_a4", id="alpha")
        for v in itertools.product(("1.2.3",), ("", ".", "-", "_"), ("a", "alpha"), ("", ".", "-", "_"), ("4",))
    ],
    *[
        pytest.param("".join(v), "1.2.3_b4", id="beta")
        for v in itertools.product(("1.2.3",), ("", ".", "-", "_"), ("b", "beta"), ("", ".", "-", "_"), ("4",))
    ],
    *[
        pytest.param("".join(v), "1.2.3_rc4", id="rc")
        for v in itertools.product(
            ("1.2.3",), ("", ".", "-", "_"), ("c", "rc", "pre", "preview"), ("", ".", "-", "_"), ("4",)
        )
    ],
    # Post-releases
    *[
        pytest.param("".join(v), "1.2.3_post4", id="post")
        for v in itertools.product(("1.2.3",), ("", ".", "-", "_"), ("post", "rev", "r"), ("", ".", "-", "_"), ("4",))
    ],
    # Developmental releases
    *[
        pytest.param("".join(v), "1.2.3_dev4", id="dev")
        for v in itertools.product(("1.2.3",), ("", ".", "-", "_"), ("dev",), ("", ".", "-", "_"), ("4",))
    ],
]


class TestParseVersion:
    @pytest.mark.parametrize("python_version,sila_version", versions)
    def test_should_parse_version(self, python_version, sila_version):
        assert parse_version(python_version) == sila_version

    def test_should_raise_on_invalid_version(self):
        with pytest.raises(ValueError, match=r"Invalid version format: 'test'."):
            parse_version("test")
