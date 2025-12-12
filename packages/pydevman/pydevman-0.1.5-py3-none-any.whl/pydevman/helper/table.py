from rich.table import Table


def build_table(title: str, header: list[str], rows: list):
    table = Table(show_header=True, header_style="bold magenta", title=title)
    for head in header:
        table.add_column(head)
    for row in rows:
        table.add_row(*row)
    return table
