"""
Tests for xls and xlsx files processing
"""
from pathlib import Path

from xls_api_demo import excel_parser


def test_process_file_basic_x_after_444() -> None:
    assert (
        excel_parser.find_x_in_file(
            Path("tests/excel_files/test_basic_x_after_444.xls")
        )
        == "added: 444"
    )
    assert (
        excel_parser.find_x_in_file(
            Path("tests/excel_files/test_basic_x_after_444.xlsx")
        )
        == "added: 444"
    )


def test_process_file_basic_x_before_444() -> None:
    assert (
        excel_parser.find_x_in_file(
            Path("tests/excel_files/test_basic_x_before_444.xls")
        )
        == "removed: 444"
    )
    assert (
        excel_parser.find_x_in_file(
            Path("tests/excel_files/test_basic_x_before_444.xlsx")
        )
        == "removed: 444"
    )
