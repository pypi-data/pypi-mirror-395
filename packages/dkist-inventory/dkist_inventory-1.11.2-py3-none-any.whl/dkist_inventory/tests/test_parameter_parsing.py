import datetime

import pytest

from dkist_inventory.parameter_parsing import ParameterParser


@pytest.fixture
def input_data_list():
    # Fixture with two parameters, one with two values
    return [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "value1",
                    "parameterValueId": 1,
                    "parameterValueStartDate": "2023-01-01T00:00:00",
                },
                {
                    "parameterValue": "value2",
                    "parameterValueId": 2,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                },
                {
                    "parameterValue": "value3",
                    "parameterValueId": 3,
                    "parameterValueStartDate": "2023-05-01T00:00:00",
                },
            ],
        },
        {
            "parameterName": "parameter_2",
            "parameterValues": [
                {
                    "parameterValue": "value3",
                    "parameterValueId": 4,
                    "parameterValueStartDate": "2023-03-01T00:00:00",
                }
            ],
        },
    ]


@pytest.fixture
def input_json_string():
    # Fixture with two parameters, one with two values as a JSON string
    return """[
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {"parameterValue": "value1", "parameterValueId": 1, "parameterValueStartDate": "2023-01-01T00:00:00"},
                {"parameterValue": "value2", "parameterValueId": 2, "parameterValueStartDate": "2023-02-01T00:00:00"}
            ]
        },
        {
            "parameterName": "parameter_2",
            "parameterValues": [
                {"parameterValue": "value4", "parameterValueId": 3, "parameterValueStartDate": "2023-03-01T00:00:00"}
            ]
        }
    ]"""


@pytest.fixture
def input_data_multiple_values():
    # Fixture with one parameter with two values, and multiple values
    return [
        {
            "parameterName": "visp_background_continuum_index",
            "parameterValues": [
                {
                    "parameterValue": '{"values": [1, 2, 3], "wavelength": [100, 200, 300]}',
                    "parameterValueId": 1,
                    "parameterValueStartDate": "2023-01-01T00:00:00",
                },
                {
                    "parameterValue": '{"values": [4, 5, 6], "wavelength": [100, 200, 300]}',
                    "parameterValueId": 2,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                },
            ],
        }
    ]


@pytest.fixture
def dataset_date_str():
    """Fixture with a dataset start date as a string"""
    return "2023-02-15T00:00:00"


@pytest.fixture
def dataset_date_datetime():
    """Fixture with a dataset start date as a datetime object"""
    return datetime.datetime(2023, 2, 15, 0, 0, 0)


@pytest.fixture
def dataset_date_late_datetime():
    """Fixture with a dataset start date as a datetime object"""
    return datetime.datetime(2024, 2, 15, 0, 0, 0)


@pytest.fixture
def dataset_date_early_datetime():
    """Fixture with a dataset start date as a datetime object"""
    return datetime.datetime(2022, 2, 15, 0, 0, 0)


@pytest.fixture
def dataset_date_exact_datetime():
    """Fixture with a dataset start date as a datetime object"""
    return datetime.datetime(2023, 2, 1, 0, 0, 0)


# Tests
def test_filter_one_valid_with_list(input_data_list, dataset_date_str):
    """
    Test that filters with one valid and one invalid parameter value.

    :Given: Two parameters, one with multiple parameter values in a JSON object.
    :When: Earlier values for the parameter value and values later than dataset start date are filtered out.
    :Then: The JSON object contains only one valid parameter.
    """
    # Given
    expected_output = [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "value2",
                    "parameterValueId": 2,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                }
            ],
        },
    ]

    # When/Then
    # Date used 2023-02-15T00:00:00
    assert (
        ParameterParser(
            parameters=input_data_list, dataset_date=dataset_date_str
        ).filtered_parameters
        == expected_output
    )


# Tests
def test_filter_all_valid_with_list(input_data_list, dataset_date_late_datetime):
    """
    Test that filters with two parameter values, both with valid values.

    :Given: Two parameters, both with multiple parameter values in a JSON object.
    :When: Earlier values for the parameter value are filtered out.
    :Then: The JSON object contains two valid parameters.
    """
    # Given
    expected_output = [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "value3",
                    "parameterValueId": 3,
                    "parameterValueStartDate": "2023-05-01T00:00:00",
                }
            ],
        },
        {
            "parameterName": "parameter_2",
            "parameterValues": [
                {
                    "parameterValue": "value3",
                    "parameterValueId": 4,
                    "parameterValueStartDate": "2023-03-01T00:00:00",
                }
            ],
        },
    ]

    # When/Then
    # Date used 2024-02-15T00:00:00
    assert (
        ParameterParser(
            parameters=input_data_list,
            dataset_date=dataset_date_late_datetime,
        ).filtered_parameters
        == expected_output
    )


def test_filter_latest_with_datetime(input_data_list, dataset_date_datetime):
    """
    Test that ensures filtering works with a dataset date provided as a datetime object.

    :Given: Two parameters, one with multiple parameter values.
    :When: Filtering is applied with a dataset start date as a datetime object.
    :Then: The correct latest parameter value before the dataset date is returned.
    """
    # Given
    expected_output = [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "value2",
                    "parameterValueId": 2,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                }
            ],
        },
    ]

    # When/Then
    # Date used 2023-02-15T00:00:00
    assert (
        ParameterParser(
            parameters=input_data_list, dataset_date=dataset_date_datetime
        ).filtered_parameters
        == expected_output
    )


def test_filter_latest_with_empty_list(input_data_list):
    """
    Test that ensures an empty list input returns an empty list.

    :Given: An empty list as input.
    :When: The filter_latest_parameter_values method is called.
    :Then: The output should be an empty list.
    """
    assert (
        ParameterParser(parameters=[], dataset_date="2023-02-15T00:00:00").filtered_parameters == []
    )


def test_filter_latest_with_earlier_dataset_date(input_data_list, dataset_date_early_datetime):
    """
    Test that ensures filtering works correctly when the dataset date is earlier than all parameter values.

    :Given: A dataset date before all parameter start dates.
    :When: The filter_latest_parameter_values method is called.
    :Then: The output should be an empty list since no values exist before the dataset date.
    """

    # When/Then
    # Date used 2022-02-15T00:00:00
    assert (
        ParameterParser(
            parameters=input_data_list,
            dataset_date=dataset_date_early_datetime,
        ).filtered_parameters
        == []
    )


def test_filter_latest_with_exact_match(input_data_list, dataset_date_exact_datetime):
    """
    Test that ensures filtering correctly selects a parameter value that exactly matches the dataset start date.

    :Given: A dataset date matching a parameter value's start date.
    :When: The filter_latest_parameter_values method is called.
    :Then: The exact matching value should be selected.
    """
    # Given
    expected_output = [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "value2",
                    "parameterValueId": 2,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                }
            ],
        },
    ]

    # When/Then
    # Date used 2022-02-01T00:00:00
    assert (
        ParameterParser(
            parameters=input_data_list,
            dataset_date=dataset_date_exact_datetime,
        ).filtered_parameters
        == expected_output
    )


@pytest.fixture
def input_data_with_none_or_missing_dates():
    """Fixture that includes parameter values with None and missing start dates."""
    return [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {"parameterValue": "no_date1", "parameterValueId": 10},
                {
                    "parameterValue": "no_date2",
                    "parameterValueId": 11,
                    "parameterValueStartDate": None,
                },
                {
                    "parameterValue": "valid",
                    "parameterValueId": 12,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                },
            ],
        },
        {
            "parameterName": "parameter_2",
            "parameterValues": [
                {
                    "parameterValue": "later_valid",
                    "parameterValueId": 13,
                    "parameterValueStartDate": "2023-03-01T00:00:00",
                }
            ],
        },
        {
            "parameterName": "parameter_3",
            "parameterValues": [
                {"parameterValue": "no_date2", "parameterValueId": 14},
                {
                    "parameterValue": "no_date3",
                    "parameterValueId": 15,
                    "parameterValueStartDate": None,
                },
            ],
        },
    ]


@pytest.fixture
def input_data_only_missing_dates():
    """Fixture that includes only None/missing start dates."""
    return [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {"parameterValue": "no_date1", "parameterValueId": 20},
                {
                    "parameterValue": "no_date2",
                    "parameterValueId": 21,
                    "parameterValueStartDate": None,
                },
                {"parameterValue": "no_date3", "parameterValueId": 22},
            ],
        }
    ]


def test_filter_ignores_none_or_missing_dates(
    input_data_with_none_or_missing_dates, dataset_date_datetime
):
    """
    Parameters with None or missing `parameterValueStartDate` should be handled as 0001-01-01.

    :Given: Mixed valid, None, and missing start dates across multiple parameters.
    :When: Filtering with a dataset date of 2023-02-15T00:00:00.
    :Then: Values with None/missing dates are treated as 0001-01-01; only the latest value <= the dataset date is retained per parameter.
    """
    expected_output = [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "valid",
                    "parameterValueId": 12,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                }
            ],
        },
        {
            "parameterName": "parameter_3",
            "parameterValues": [
                {
                    "parameterValue": "no_date2",
                    "parameterValueId": 14,
                    "parameterValueStartDate": "0001-01-01T00:00:00",
                }
            ],
        },
    ]

    assert (
        ParameterParser(
            parameters=input_data_with_none_or_missing_dates, dataset_date=dataset_date_datetime
        ).filtered_parameters
        == expected_output
    )


def test_filter_only_missing_dates_returns_empty(
    input_data_only_missing_dates, dataset_date_datetime
):
    """
    If all parameter values have None or missing `parameterValueStartDate`, treat them as 0001-01-01
    and select the first such value. This is a case that "should" not normally occur in real data.

    :Given: A parameter with only None/missing start dates.
    :When: Filtering with any dataset date.
    :Then: The output should include one value dated 0001-01-01.
    """
    assert ParameterParser(
        parameters=input_data_only_missing_dates, dataset_date=dataset_date_datetime
    ).filtered_parameters == [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "no_date1",
                    "parameterValueId": 20,
                    "parameterValueStartDate": "0001-01-01T00:00:00",
                }
            ],
        }
    ]


@pytest.fixture
def input_data_with_missing_start_dates_and_valid():
    """Fixture: entries with missing start-date values plus a valid-dated value."""
    return [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {"parameterValue": "no_date_a", "parameterValueId": 30},
                {"parameterValue": "no_date_b", "parameterValueId": 31},
                {
                    "parameterValue": "valid",
                    "parameterValueId": 32,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                },
            ],
        },
        {
            "parameterName": "parameter_2",
            "parameterValues": [
                {
                    "parameterValue": "later_valid",
                    "parameterValueId": 33,
                    "parameterValueStartDate": "2023-03-01T00:00:00",
                }
            ],
        },
    ]


@pytest.fixture
def input_data_missing_and_valid_same_parameter():
    """Fixture: same parameter has missing/None dates and a valid-dated value."""
    return [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {"parameterValue": "no_date1", "parameterValueId": 50},
                {
                    "parameterValue": "no_date2",
                    "parameterValueId": 51,
                    "parameterValueStartDate": None,
                },
                {
                    "parameterValue": "valid",
                    "parameterValueId": 52,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                },
                {
                    "parameterValue": "future",
                    "parameterValueId": 53,
                    "parameterValueStartDate": "2024-01-01T00:00:00",
                },
            ],
        }
    ]


@pytest.fixture
def input_data_only_missing_start_dates():
    """Fixture: ONLY missing start-date values (no explicit None values)."""
    return [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {"parameterValue": "no_date1", "parameterValueId": 40},
                {"parameterValue": "no_date2", "parameterValueId": 41},
            ],
        }
    ]


def test_filter_ignores_missing_start_dates_only(
    input_data_with_missing_start_dates_and_valid, dataset_date_datetime
):
    """
    Parameters missing the `parameterValueStartDate` value are treated as 0001-01-01, valid-dated value before the dataset date is kept.

    :Given: A mix of values where some omit the start-date value entirely,
    plus a valid earlier-dated value and another parameter with a later date.
    :When: Filtering with a dataset date of 2023-02-15T00:00:00.
    :Then: Only the parameter_1 value from 2023-02-01 is retained; the later 2023-03-01 value is excluded.
    """
    expected_output = [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "valid",
                    "parameterValueId": 32,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                }
            ],
        }
    ]

    assert (
        ParameterParser(
            parameters=input_data_with_missing_start_dates_and_valid,
            dataset_date=dataset_date_datetime,
        ).filtered_parameters
        == expected_output
    )


def test_missing_and_valid_date_same_parameter(
    input_data_missing_and_valid_same_parameter, dataset_date_datetime
):
    """
    When a parameter contains both missing/None and valid start dates, treat missing/None as 0001-01-01
    and select the latest value <= dataset date. In theory, this situation should not occur in real data.

    :Given: One parameter with two missing/None values and two dated values (one before, one after dataset date).
    :When: Filtering with dataset date 2023-02-15T00:00:00.
    :Then: The 2023-02-01 value is retained (later than 0001-01-01 and <= dataset date).
    """
    expected_output = [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "valid",
                    "parameterValueId": 52,
                    "parameterValueStartDate": "2023-02-01T00:00:00",
                }
            ],
        }
    ]

    assert (
        ParameterParser(
            parameters=input_data_missing_and_valid_same_parameter,
            dataset_date=dataset_date_datetime,
        ).filtered_parameters
        == expected_output
    )


def test_filter_only_missing_start_dates_returns_empty(
    input_data_only_missing_start_dates, dataset_date_datetime
):
    """
    If all parameters are missing the `parameterValueStartDate` value, treat them as 0001-01-01
    and select the first such value.

    :Given: A parameter where all values omit the start-date value.
    :When: Filtering with any dataset date.
    :Then: The output should include one value dated 0001-01-01.
    """
    assert ParameterParser(
        parameters=input_data_only_missing_start_dates, dataset_date=dataset_date_datetime
    ).filtered_parameters == [
        {
            "parameterName": "parameter_1",
            "parameterValues": [
                {
                    "parameterValue": "no_date1",
                    "parameterValueId": 40,
                    "parameterValueStartDate": "0001-01-01T00:00:00",
                }
            ],
        }
    ]
