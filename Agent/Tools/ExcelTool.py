import pandas as pd


def get_sheet_names(
        filename: str
) -> str:
    """get Excel file name"""
    excel_file = pd.ExcelFile(filename)
    sheet_names = excel_file.sheet_names
    return f"file name: '{filename}' sheet name: \n\n{sheet_names}"


def get_column_names(
        filename: str
) -> str:
    """get Excel file column name"""

    df = pd.read_excel(filename, sheet_name=0)
    column_names = '\n'.join(
        df.columns.to_list()
    )

    result = f"file name: '{filename}' col names：\n\n{column_names}"
    return result


def get_first_n_rows(
        filename: str,
        n: int = 3
) -> str:
    """get Excel first n rows"""

    result = get_sheet_names(filename) + "\n\n"

    result += get_column_names(filename) + "\n\n"

    df = pd.read_excel(filename, sheet_name=0)  
    n_lines = '\n'.join(
        df.head(n).to_string(index=False, header=True).split('\n')
    )

    result += f"file name: '{filename}' first {n} rows: \n\n{n_lines}"
    return result
