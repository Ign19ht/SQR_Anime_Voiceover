import pandas as pd
from typing import Dict
import os


class Strings:
    # States
    NOT_RECORDED = "Not recorded"
    RECORDED = "Recorded"
    CLEANED = "Cleaned"
    # Sheet fields
    NAME = "name"
    STATE = "state"
    # New columns strings
    TABLE = "table"
    TOTAL = "Total"
    # New rows strings
    EXTRA = "EXTRA"
    SUM = "Sum"
    # Sup String
    CELL_VIEW = "Cell Value"


KANBAN_STATES = [Strings.NOT_RECORDED, Strings.RECORDED, Strings.CLEANED]
VIEW_STATES = [Strings.RECORDED, Strings.CLEANED, Strings.TOTAL]


# Merge all tables into one and all EXTRA characters into one
def concat_tables(dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    # Use only file name without extension
    dataframes = {os.path.splitext(key)[0]: value for key, value in dataframes.items()}

    # Save table name
    dataframes = [df.assign(table=table_name) for table_name, df in dataframes.items()]

    all_data = pd.concat(dataframes, ignore_index=True)

    # Move all EXTRA characters to one
    all_data[Strings.NAME] = all_data[Strings.NAME].apply(
        lambda x: Strings.EXTRA if Strings.EXTRA in x else x
    )

    return all_data


# Grouping for next calculations
def grouping_by_stat(all_data: pd.DataFrame) -> pd.DataFrame:
    grouped_data = (
        all_data.groupby([Strings.NAME, Strings.TABLE, Strings.STATE])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Add missing columns
    for state in KANBAN_STATES:
        if state not in grouped_data:
            grouped_data[state] = 0

    return grouped_data


# Create dashboard
def constrain_dashboard(grouped_data: pd.DataFrame) -> pd.DataFrame:
    # Calculate total for each episode
    grouped_data[Strings.TOTAL] = grouped_data[KANBAN_STATES].sum(axis=1)

    # Format cell with VIEW_STATES
    grouped_data[Strings.CELL_VIEW] = (
        grouped_data[VIEW_STATES].astype(str).apply("/".join, axis=1)
    )
    final_table = grouped_data.pivot(
        index=Strings.NAME, columns=Strings.TABLE, values=Strings.CELL_VIEW
    )

    final_table.reset_index(inplace=True)

    return final_table


# Calculate total for each character
def calc_total(final_table: pd.DataFrame) -> pd.DataFrame:
    total_column = final_table.apply(
        lambda row: sum(
            int(x.split("/")[VIEW_STATES.index(Strings.TOTAL)])
            for x in row.drop(Strings.NAME)
            if isinstance(x, str)
        ),
        axis=1,
    )
    final_table[Strings.TOTAL] = total_column

    return final_table


# Calculate total for each episode
def calc_summary(final_table: pd.DataFrame) -> pd.DataFrame:
    # Fill all NaN cells with necessary format
    final_table.fillna("/".join("0" for _ in range(len(VIEW_STATES))), inplace=True)

    # Calculate total for each episode
    totals = (
        final_table.drop(Strings.TOTAL, axis=1)
        .drop(Strings.NAME, axis=1)
        .apply(lambda col: col.str.rsplit("/", expand=True).astype(int).sum())
        .apply(lambda row: "/".join(str(val) for val in row))
    )

    # Calculate total for Total column and merge
    total_summary = pd.Series(
        totals.tolist() + [final_table[Strings.TOTAL].sum()],
        index=totals.index.tolist() + [Strings.TOTAL],
    )

    # Insert into final table
    total_summary[Strings.NAME] = Strings.SUM
    final_table.loc[Strings.SUM] = total_summary

    return final_table


# Main function for paring
def parse(dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    all_data = concat_tables(dataframes)
    grouped_data = grouping_by_stat(all_data)
    final_table = constrain_dashboard(grouped_data)
    final_table = calc_total(final_table)
    final_table = calc_summary(final_table)
    return final_table
