import pandas as pd
from typing import Dict
import os

EXPECTED_STATES = ['Not recorded', 'Recorded', 'Cleaned']


def concat_tables(dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    dataframes = {os.path.splitext(key)[0]: value for key, value in dataframes.items()}

    dataframes = [df.assign(table=table_name) for table_name, df in dataframes.items()]

    all_data = pd.concat(dataframes, ignore_index=True)

    all_data['name'] = all_data['name'].apply(lambda x: 'EXTRA' if 'EXTRA' in x else x)

    return all_data


def grouping_by_stat(all_data: pd.DataFrame) -> pd.DataFrame:
    grouped_data = all_data.groupby(['name', 'table', 'state']).size().unstack(fill_value=0).reset_index()

    for state in EXPECTED_STATES:
        if state not in grouped_data:
            grouped_data[state] = 0

    return grouped_data


def constrain_dashboard(grouped_data: pd.DataFrame) -> pd.DataFrame:
    grouped_data['Total'] = grouped_data[EXPECTED_STATES].sum(axis=1)

    grouped_data['Table Value'] = grouped_data['Recorded'].astype(str) + '/' + grouped_data['Cleaned'].astype(str) + '/' + grouped_data['Total'].astype(str)

    final_table = grouped_data.pivot(index='name', columns='table', values='Table Value')

    final_table.reset_index(inplace=True)

    return final_table


def calc_total(final_table: pd.DataFrame) -> pd.DataFrame:

    total_column = final_table.apply(
        lambda row: sum(int(x.split('/')[2]) for x in row.drop('name') if isinstance(x, str)),
        axis=1
    )
    final_table['Total'] = total_column

    return final_table


def calc_summary(final_table: pd.DataFrame) -> pd.DataFrame:

    final_table.fillna('0/0/0', inplace=True)

    totals = final_table.drop("Total", axis=1).drop("name", axis=1)\
        .apply(lambda col: col.str.rsplit('/', expand=True).astype(int).sum()).\
        apply(lambda row: f"{row[0]}/{row[1]}/{row[2]}")
    total_summary = pd.Series(
        totals.tolist() + [final_table['Total'].sum()],
        index=totals.index.tolist() + ['Total']
    )
    total_summary['name'] = 'Sum'
    final_table.loc['Sum'] = total_summary

    return final_table


def parse(dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    all_data = concat_tables(dataframes)
    grouped_data = grouping_by_stat(all_data)
    final_table = constrain_dashboard(grouped_data)
    final_table = calc_total(final_table)
    final_table = calc_summary(final_table)
    return final_table
