import pytest
from nabu.utils import compare_dicts
from nabu.resources.utils import get_quantities_and_units


class TestUnits:
    expected_results = {
        "distance = 1 m ; pixel_size = 2.0 um": {"distance": 1.0, "pixel_size": 2e-6},
        "distance = 1 m ; pixel_size = 2.6 micrometer": {"distance": 1.0, "pixel_size": 2.6e-6},
        "distance = 10 m ; pixel_size = 2e-6 m": {"distance": 10, "pixel_size": 2e-6},
        "distance = .5 m ; pixel_size = 2.6e-4 centimeter": {"distance": 0.5, "pixel_size": 2.6e-6},
        "distance = 10 cm ; pixel_size = 2.5 micrometer ; energy = 1 ev": {
            "distance": 0.1,
            "pixel_size": 2.5e-6,
            "energy": 1.0e-3,
        },
        "distance = 10 cm ; pixel_size = 9.0e-3 millimeter ; energy = 19 kev": {
            "distance": 0.1,
            "pixel_size": 9e-6,
            "energy": 19.0,
        },
    }
    expected_failures = {
        # typo ("ke" instead of "kev")
        "distance = 10 cm ; energy = 10 ke": ValueError("Cannot convert: ke"),
        # No units
        "distance = 10 ; energy = 10 kev": ValueError("not enough values to unpack (expected 2, got 1)"),
        # Unit not separated by space
        "distance = 10m; energy = 10 kev": ValueError("not enough values to unpack (expected 2, got 1)"),
        # Invalid separator
        "distance = 10 m, energy = 10 kev": ValueError("too many values to unpack (expected 2)"),
    }

    def test_conversion(self):
        for test_str, expected_result in self.expected_results.items():
            res = get_quantities_and_units(test_str)
            err_msg = str(
                "Something wrong with quantities/units extraction from '%s': expected %s, got %s"
                % (test_str, str(expected_result), str(res))
            )
            assert compare_dicts(res, expected_result) is None, err_msg

    def test_valid_input(self):
        for test_str, expected_failure in self.expected_failures.items():
            with pytest.raises(type(expected_failure)) as e_info:
                get_quantities_and_units(test_str)
            assert e_info.value.args[0] == str(expected_failure)
