import pandas as pd
from app.parser import concat_tables, grouping_by_stat, constrain_dashboard, calc_total, calc_summary,\
    KANBAN_STATES, Strings


def test_concat_tables():
    df1 = pd.DataFrame({
        Strings.NAME: ['name1', 'name2', 'EXTRA1'],
        Strings.STATE: [Strings.RECORDED, Strings.CLEANED, Strings.RECORDED]
    })
    df2 = pd.DataFrame({
        Strings.NAME: ['name2', 'name3', 'EXTRA2'],
        Strings.STATE: [Strings.NOT_RECORDED, Strings.RECORDED, Strings.RECORDED]
    })
    dataframes = {'table1.csv': df1, 'table2.csv': df2}
    result = concat_tables(dataframes)
    assert Strings.NAME in result.columns
    assert Strings.STATE in result.columns
    assert result.shape == (6, 3)
    assert result[Strings.NAME].value_counts().get(Strings.EXTRA, 0) == 2


def test_grouping_by_stat():
    df = pd.DataFrame({
        Strings.NAME: ['name2', 'name2', 'name2', 'name3'],
        Strings.TABLE: ['table1', 'table1', 'table2', 'table2'],
        Strings.STATE: [Strings.CLEANED, Strings.CLEANED, Strings.NOT_RECORDED, Strings.NOT_RECORDED]
    })
    result = grouping_by_stat(df)
    for state in KANBAN_STATES:
        assert state in result.columns
    assert result.loc[result[Strings.NAME] == 'name2', Strings.CLEANED].iloc[0] == 2


def test_constrain_dashboard():
    grouped_data = pd.DataFrame({
        Strings.NAME: ['name2', 'name2', 'name1'],
        Strings.TABLE: ['table1', 'table2', 'table2'],
        Strings.RECORDED: [1, 2, 0],
        Strings.CLEANED: [0, 1, 3],
        Strings.NOT_RECORDED: [1, 1, 4]
    })
    result = constrain_dashboard(grouped_data)
    assert Strings.NAME in result.columns
    assert 'table1' in result.columns
    assert 'table2' in result.columns
    assert result.loc[result[Strings.NAME] == 'name2', 'table2'].iloc[0] == '2/1/4'


def test_calc_total():
    final_table = pd.DataFrame({
        Strings.NAME: ['name1', 'name2'],
        'table1': ['2/1/4', None],
        'table2': ['2/1/4', '2/1/4'],
    })
    result = calc_total(final_table)
    assert Strings.TOTAL in result.columns
    assert Strings.NAME in result.columns
    assert 'table1' in result.columns
    assert 'table2' in result.columns
    assert result.loc[result[Strings.NAME] == 'name1', Strings.TOTAL].iloc[0] == 8
    assert result.loc[result[Strings.NAME] == 'name2', Strings.TOTAL].iloc[0] == 4


def test_calc_summary():
    final_table = pd.DataFrame({
        Strings.NAME: ['name1', 'name2'],
        'table1': ['2/1/4', None],
        'table2': ['2/1/4', '2/1/4'],
        Strings.TOTAL: ['8', '4']
    })
    result = calc_summary(final_table)
    assert result.loc[result[Strings.NAME] == Strings.SUM, 'table1'].iloc[0] == '2/1/4'
    assert result.loc[result[Strings.NAME] == Strings.SUM, 'table2'].iloc[0] == '4/2/8'

