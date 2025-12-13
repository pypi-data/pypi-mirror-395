"""Utilities for scraping HTML tables."""

from dataclasses import dataclass
from typing import cast

from bs4 import Tag as HtmlTag

from oocone import errors

DataRow = dict[str, str]


@dataclass
class Table:
    columns: list[str]
    rows: list[DataRow]


def parse_table(html_table: HtmlTag) -> Table:
    rows = cast("list[HtmlTag]", html_table.find_all("tr"))
    for row in rows:
        if not isinstance(row, HtmlTag):
            msg = f"Expected tr as Tag but found {type(row)}"
            raise errors.UnexpectedResponse(msg)

    columns = _parse_header_row(rows[0])
    data_rows = [_parse_data_row(r, columns) for r in rows[1:]]

    return Table(columns=columns, rows=data_rows)


def _parse_header_row(row: HtmlTag) -> list[str]:
    return [cell.text for cell in row.find_all("th")]


def _parse_data_row(row: HtmlTag, columns: list[str]) -> DataRow:
    row_cells = row.find_all("td")
    return {header: cell.text for header, cell in zip(columns, row_cells, strict=False)}
