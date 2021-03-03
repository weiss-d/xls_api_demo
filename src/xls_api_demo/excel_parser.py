"""
Module for processing XLS and XLSX files and finding difference
between 'before' and 'after' columns.
"""
from pathlib import Path

import pyexcel


def find_x_in_file(excel_file: Path) -> str:
    """Finds a number that is present only in one column and returns it in
    formatted string according to the requirements.

    Parameters
    ----------
    excel_file : Path
        Path to Excel file.
        File existence should be checked on the calling side.

    Returns
    -------
    str
        Formatted string with resulting number.

    """
    book = pyexcel.get_book(file_name=excel_file.absolute().as_posix())
    # Filtering out empty sheets
    for sheet in (sh for sh in book if sh):

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

            # Validity checkup
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
