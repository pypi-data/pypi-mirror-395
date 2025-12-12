# standard
# third party
# custom
from sunwaee_gen.helpers import get_nested_dict_value


class TestHelpers:

    def test_get_nested_dict_value_classic(self):
        data = {
            "a": {
                "b": {
                    "c": "d",
                },
            },
        }
        assert get_nested_dict_value(data, "a.b.c") == "d"

    def test_get_nested_dict_value_none(self):
        assert get_nested_dict_value({}, "a.b.c") is None

    def test_get_nested_dict_value_invalid_path(self):
        data = {"a": {"b": "c"}}
        assert get_nested_dict_value(data, "a.b.c.d") is None

    def test_get_nested_dict_value_array_index(self):
        data = {
            "a": [
                {
                    "b": "c",
                },
                {
                    "b": "d",
                },
            ],
        }
        assert get_nested_dict_value(data, "a.0.b") == "c"
        assert get_nested_dict_value(data, "a.1.b") == "d"

    def test_get_nested_dict_value_array_index_invalid(self):
        data = {
            "a": [
                {
                    "b": "c",
                },
            ],
        }
        assert get_nested_dict_value(data, "a.X.b") is None

    def test_get_nested_dict_value_array_filter_key(self):
        data = {
            "a": [
                {
                    "b": "c",
                },
                {
                    "b": "d",
                },
            ],
        }
        assert get_nested_dict_value(data, "a.[b].b") == ["c", "d"]

    def test_get_nested_dict_value_arrays_filter_key(self):
        data = {
            "a": [
                {
                    "b": {
                        "c": "d",
                    },
                },
                {
                    "b": {
                        "c": "e",
                    },
                },
            ],
        }
        assert get_nested_dict_value(data, "a.[b].b.[c].c") == ["d", "e"]

    def test_get_nested_dict_value_array_filter_only(self):
        data = {
            "a": [
                {
                    "b": "c",
                },
                {
                    "b": "d",
                },
            ],
        }
        assert get_nested_dict_value(data, "a.[b]") == [{"b": "c"}, {"b": "d"}]

    def test_get_nested_dict_value_array_filter_key_value(self):
        data = {
            "a": [
                {
                    "b": "c",
                },
                {
                    "b": "d",
                },
            ],
        }
        assert get_nested_dict_value(data, "a.[b=c].b") == "c"
