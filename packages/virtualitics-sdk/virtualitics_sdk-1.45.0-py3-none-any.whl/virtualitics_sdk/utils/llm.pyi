def df_to_compact_markdown(df, title: str | None = None, max_rows: int | None = 10, max_cols: int | None = None):
    """
    Convert a pandas DataFrame to a compact markdown representation with statistics.

    :param df: (pd.DataFrame): The DataFrame to convert
    :param title: Title for the table
    :param max_rows: Maximum number of sample rows to include (default: 5)
    :param max_cols: Maximum number of columns to show (None = all)

    Returns:
        str: Markdown representation of the DataFrame
    """
