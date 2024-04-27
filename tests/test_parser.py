import pandas as pd
from app.parser import concat_tables, grouping_by_stat, constrain_dashboard, calc_total, calc_summary, EXPECTED_STATES


def test_concat_tables():
    df1 = pd.DataFrame({
        'name': ['name1', 'name2', 'EXTRA1'],
        'state': ['Recorded', 'Cleaned', 'Recorded']
    })
    df2 = pd.DataFrame({
        'name': ['name2', 'name3', 'EXTRA2'],
        'state': ['Not recorded', 'Recorded', 'Recorded']
    })
    dataframes = {'table1.csv': df1, 'table2.csv': df2}
    result = concat_tables(dataframes)
    assert 'name' in result.columns
    assert 'status' in result.columns
    assert result.shape == (6, 3)
    assert result['name'].value_counts().get('EXTRA', 0) == 2


def test_grouping_by_stat():
    df = pd.DataFrame({
        'name': ['name2', 'name2', 'name2', 'name3'],
        'table': ['table1', 'table1', 'table2', 'table2'],
        'state': ['Cleaned', 'Cleaned', 'Not recorded', 'Not recorded']
    })
    result = grouping_by_stat(df)
    for state in EXPECTED_STATES:
        assert state in result.columns
    assert result.loc[result['name'] == 'name2', 'Cleaned'].iloc[0] == 2


def test_constrain_dashboard():
    grouped_data = pd.DataFrame({
        'name': ['name2', 'name2', 'name1'],
        'table': ['table1', 'table2', 'table2'],
        'Recorded': [1, 2, 0],
        'Cleaned': [0, 1, 3],
        'Not recorded': [1, 1, 4]
    })
    result = constrain_dashboard(grouped_data)
    assert 'name' in result.columns
    assert 'table1' in result.columns
    assert 'table2' in result.columns
    assert result.loc[result['name'] == 'name2', 'table2'].iloc[0] == '2/1/4'


def test_calc_total():
    final_table = pd.DataFrame({
        'name': ['name1', 'name2'],
        'table1': ['2/1/4', None],
        'table2': ['2/1/4', '2/1/4'],
    })
    result = calc_total(final_table)
    assert 'Total' in result.columns
    assert result.loc[result['name'] == 'name1', 'Total'].iloc[0] == 8
    assert result.loc[result['name'] == 'name2', 'Total'].iloc[0] == 4


def test_calc_summary():
    final_table = pd.DataFrame({
        'name': ['name1', 'name2'],
        'table1': ['2/1/4', None],
        'table2': ['2/1/4', '2/1/4'],
        'Total': ['8', '4']
    })
    result = calc_summary(final_table)
    assert result.loc[result['name'] == 'Sum', 'table1'].iloc[0] == '2/1/4'
    assert result.loc[result['name'] == 'Sum', 'table2'].iloc[0] == '4/2/8'

