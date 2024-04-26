import pandas as pd
from unittest.mock import mock_open, patch
from app.parser import read_data, concat_tables, grouping_by_stat, constrain_dashboard, calc_total, calc_summary, EXPECTED_STATES


def test_read_data(monkeypatch):
    CSV_DATA = """start,end,status,name,text
    0:00:15,0:00:18,Recorded,testname,"text"
    0:00:19,0:00:21,Recorded,testname,"text"
    0:00:22,0:00:26,Recorded,testname,text"""

    with patch("builtins.open", mock_open(read_data=CSV_DATA)):
        files = ["dummy.csv", "dummy2.csv"]
        result = read_data(files)
        assert len(result) == 2
        assert all(isinstance(df, pd.DataFrame) for df in result)
        assert result[0].shape == (3, 6)
        assert result[0]["table"][0] == "dummy"
        assert result[1]["table"][0] == "dummy2"


def test_concat_tables():
    df1 = pd.DataFrame({
        'name': ['name1', 'name2', 'EXTRA1'],
        'status': ['Recorded', 'Cleaned', 'Recorded'],
        'table': ['table1', 'table1', 'table1']
    })
    df2 = pd.DataFrame({
        'name': ['name2', 'name3', 'EXTRA2'],
        'status': ['Not recorded', 'Recorded', 'Recorded'],
        'table': ['table2', 'table2', 'table2']
    })
    dataframes = [df1, df2]
    result = concat_tables(dataframes)
    assert 'name' in result.columns
    assert 'status' in result.columns
    assert result.shape == (6, 3)
    assert result['name'].value_counts().get('EXTRA', 0) == 2


def test_grouping_by_stat():
    df = pd.DataFrame({
        'name': ['name2', 'name2', 'name2', 'name3'],
        'table': ['table1', 'table1', 'table2', 'table2'],
        'status': ['Cleaned', 'Cleaned', 'Not recorded', 'Not recorded']
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

