"""
SOURCE: https://github.com/khuyentran1401/rich-dataframe/blob/master/rich_dataframe/rich_dataframe.py
Some minor modifications made re. color, caption, etc
"""

from upyog.imports import *


def cast_to_df(items: Union[pd.DataFrame, pd.Series, dict]):
    if   isinstance(items, pd.Series):    return pd.DataFrame(items)
    elif isinstance(items, dict):         return pd.DataFrame(items.items())
    elif isinstance(items, pd.DataFrame): return items
    else:
        raise TypeError(f"Expected `items` to be `pd.DataFrame` |  `pd.Series` | `dict`, got {type(items)} instead")

def print_df(
    df: Union[pd.DataFrame, pd.Series],
    title: Optional[str] = None,
    headers = "keys", tablefmt = "psql",
    **tabulate_kwargs,
):
    from tabulate import tabulate

    if title: print(title)
    df = cast_to_df(df)

    table = tabulate(
        df,
        headers = headers,
        tablefmt = tablefmt,
        **tabulate_kwargs
    )
    print(table)

    return table

def print_df(df: Union[pd.DataFrame, pd.Series, dict]):
    from prettytable import PrettyTable

    df = cast_to_df(df)

    table = PrettyTable(max_width=50)
    table.field_names = df.columns  # Set the column names

    # Add the rows to the table
    for row in df.itertuples(index=False):
        table.add_row(row)

    print(table)
