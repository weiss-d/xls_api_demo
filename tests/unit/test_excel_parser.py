"""
Tests for xls and xlsx files processing
"""
from pathlib import Path

import pytest

from xls_api_demo import excel_parser


@pytest.mark.parametrize(
    "excel_file,expected_output",
    [
        ("tests/excel_files/test_basic_x_after_444.xls", "added: 444"),
        ("tests/excel_files/test_basic_x_after_444.xlsx", "added: 444"),
        ("tests/excel_files/test_basic_x_before_444.xls", "removed: 444"),
        ("tests/excel_files/test_basic_x_before_444.xlsx", "removed: 444"),
        (
            "tests/excel_files/test_basic_double_after_column_x_after_444.xls",
            "added: 444",
        ),
        (
            "tests/excel_files/test_basic_double_after_column_x_after_444.xlsx",
            "added: 444",
        ),
        (
            "tests/excel_files/test_data_after_empty_row_x_before_444.xls",
            "removed: 444",
        ),
        (
            "tests/excel_files/test_data_after_empty_row_x_before_444.xlsx",
            "removed: 444",
        ),
        ("tests/excel_files/test_data_on_2nd_sheet_x_before_444.xls", "removed: 444"),
        ("tests/excel_files/test_data_on_2nd_sheet_x_before_444.xlsx", "removed: 444"),
        (
            "tests/excel_files/test_data_on_2nd_sheet_plus_3rd_sheet_x_before_444.xls",
            "removed: 444",
        ),
        (
            "tests/excel_files/test_data_on_2nd_sheet_plus_3rd_sheet_x_before_444.xlsx",
            "removed: 444",
        ),
    ],
)
def test_find_x_in_file_basic_x_444_with_normal_edge_cases(
    excel_file: str, expected_output: str
) -> None:
    """Testing normal cases with pure input files and some deviations.

    Parameters
    ----------
    excel_file : str
        Excel file from test folder.
    expected_output : str
        Expected output.

    Returns
    -------
    None

    """
    assert excel_parser.find_x_in_file(Path(excel_file)) == expected_output


@pytest.mark.parametrize(
    "excel_file",
    [
        "tests/excel_files/test_error_empty.xls",
        "tests/excel_files/test_error_empty.xlsx",
        "tests/excel_files/test_error_only_one_column.xls",
        "tests/excel_files/test_error_only_one_column.xlsx",
        "tests/excel_files/test_fake_data_after_empty_column_x_before_444.xls",
        "tests/excel_files/test_fake_data_after_empty_column_x_before_444.xlsx",
    ],
)
def test_find_x_in_file_one_or_both_columns_absent(excel_file: str) -> None:
    with pytest.raises(ValueError) as e:
        excel_parser.find_x_in_file(Path(excel_file))
    assert str(e.value) == "No sheets with valid 'before' and 'after' colums found."


@pytest.mark.parametrize(
    "excel_file",
    [
        "tests/excel_files/test_error_equal_columns.xls",
        "tests/excel_files/test_error_equal_columns.xlsx",
    ],
)
def test_find_x_in_file_error_for_equal_columns(excel_file: str) -> None:
    with pytest.raises(ValueError) as e:
        excel_parser.find_x_in_file(Path(excel_file))
    assert (
        str(e.value) == "'before' and 'after' columns found, but have incorrect size."
    )


@pytest.mark.parametrize(
    "excel_file",
    [
        "tests/excel_files/test_error_non_integer_value_in_column.xls",
        "tests/excel_files/test_error_non_integer_value_in_column.xlsx",
    ],
)
def test_find_x_in_file_error_incorrect_row_values(excel_file: str) -> None:
    with pytest.raises(ValueError) as e:
        excel_parser.find_x_in_file(Path(excel_file))
    assert str(e.value) == "Processed columns contain non-integer values."
