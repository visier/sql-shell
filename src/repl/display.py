import itertools
from visier.connector import ResultTable
from .constants import SQL_TABLE_START, SQL_TABLE_END

class TableDisplay:
    "Displays the contents of a result table with aligned columns"
    def __init__(self, table: ResultTable, max_col_width: int):
        "Initializes the table display which consumes the table rows generator"
        self._header = table.header
        self._rows_width, self._rows_display = itertools.tee(table.rows())
        self._max_col_width = max_col_width
        self._col_widths = [0] * len(table.header)

    def display(self):
        "Displays the table in a simple, columnar format"
        self._determine_col_widths()
        print(SQL_TABLE_START)
        self._columnize(self._header)
        self._print_separator()
        [self._columnize(row) for row in self._rows_display]
        print(SQL_TABLE_END)

    def _columnize(self, row):
        "Prints a row of the table, respecting the column width"
        print("|".join([self._cap_field_width(str(col)).ljust(self._col_widths[i]) for i, col in enumerate(row)]))

    def _determine_col_widths(self):
        "Determines the maximum column width for each column by traversing the header and rows"
        self._determine_col_widths_by_row(self._header)
        for row in self._rows_width:
            self._determine_col_widths_by_row(row)

    def _determine_col_widths_by_row(self, row):
        "Potentially update the column widths based on actual values in a given row (which may be the header)"
        for i, col in enumerate(row):
            self._col_widths[i] = min(self._max_col_width, max(self._col_widths[i], len(str(col))))
    
    def _print_separator(self):
        print("-" * (sum(self._col_widths) + len(self._col_widths) - 1))

    def _cap_field_width(self, field):
        if (len(field) <= self._max_col_width):
            return field
        else:
            return field[:self._max_col_width - 2] + '..'