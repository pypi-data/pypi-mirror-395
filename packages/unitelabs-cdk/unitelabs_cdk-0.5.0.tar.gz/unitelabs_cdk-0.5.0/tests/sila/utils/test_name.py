import pytest

from unitelabs.cdk.sila.utils.name import to_display_name, to_identifier


class TestToDisplayName:
    def test_should_convert_empty_string(self):
        assert to_display_name("") == ""

    def test_should_convert_class_name(self):
        assert to_display_name("MyClassName") == "My Class Name"

    @pytest.mark.parametrize("value,name", [("MyClassUUID", "My Class UUID"), ("UUIDClass", "UUID Class")])
    def test_should_convert_class_name_with_consecutive_uppercase(self, value: str, name: str):
        assert to_display_name(value) == name

    def test_should_convert_variable_name(self):
        assert to_display_name("my_variable_name") == "My Variable Name"

    @pytest.mark.parametrize(
        "value,name", [("my_variable_UUID", "My Variable UUID"), ("UUID_variable", "UUID Variable")]
    )
    def test_should_convert_consecutive_uppercase(self, value: str, name: str):
        assert to_display_name(value) == name

    @pytest.mark.parametrize(
        "name",
        [
            ("My Class Name"),
            ("My Class UUID"),
            ("UUID Class"),
            ("My Variable Name"),
            ("My Variable UUID"),
            ("UUID Variable"),
        ],
    )
    def test_should_keep_display_name(self, name: str):
        assert to_display_name(name) == name


class TestToIdentifier:
    def test_should_convert_empty_string(self):
        assert to_identifier("") == ""

    @pytest.mark.parametrize(
        "name,identifier",
        [
            ("My Class Name", "MyClassName"),
            ("My Class UUID", "MyClassUUID"),
            ("UUID Class", "UUIDClass"),
            ("My Variable Name", "MyVariableName"),
            ("My Variable UUID", "MyVariableUUID"),
            ("UUID Variable", "UUIDVariable"),
        ],
    )
    def test_should_convert_display_name(self, name: str, identifier: str):
        assert to_identifier(name) == identifier

    @pytest.mark.parametrize(
        "name,identifier",
        [
            ("Héllo 123", "Hello123"),
            ("123 Start", "I123Start"),
            ("!Bad Chars#", "BadChars"),
        ],
    )
    def test_should_remove_special_characters(self, name: str, identifier: str):
        assert to_identifier(name) == identifier
