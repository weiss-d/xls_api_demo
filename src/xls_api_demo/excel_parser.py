"""
Module for processing XLS and XLSX files and finding difference
between 'before' and 'after' columns.
"""
from pathlib import Path

import pyexcel


def find_x_in_file(excel_file: Path) -> str:
    """find_x_in_file.

    Parameters
    ----------
    excel_file : Path
        excel_file

    Returns
    -------
    str

    """
    book = pyexcel.get_book(file_name=excel_file.absolute().as_posix())
    for sheet in book:

        # Trimming the columns
        sheet.name_columns_by_row(0)
        header = sheet.colnames
        if "" in header:
            header = header[0 : header.index("")]

        if "before" in header and "after" in header:

            # Trimming the rows
            before_column = sheet.column["before"]
            if "" in before_column:
                before_column = before_column[: before_column.index("")]

            after_column = sheet.column["after"]
            if "" in after_column:
                after_column = after_column[: after_column.index("")]

            # Validity checks
            if abs(len(before_column) - len(after_column)) != 1:
                raise ValueError(
                    "'before' and 'after' columns found, but have incorrect size."
                )

            if not all(
                isinstance(element, int) for element in before_column + after_column
            ):
                raise ValueError("Processed columns contain non-integer values.")

            # Comparison
            before_column = set(before_column)
            after_column = set(after_column)

            if difference := before_column.difference(after_column):
                return f"removed: {difference.pop()}"
            if difference := after_column.difference(before_column):
                return f"added: {difference.pop()}"
    raise ValueError("No sheets with valid 'before' and 'after' colums found.")
