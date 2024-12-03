import pandas as pd


def read_race_data():
  race_data = pd.read_csv(
    '../../../data/bg_covariates/ACSDT5Y2019.B02001-Data.csv',
    usecols=['GEO_ID', 'B02001_001E', 'B02001_002E', 'B02001_003E', 'B02001_004E', 'B02001_005E', 'B02001_006E',
             'B02001_007E']
  )

  # drop row corresp. to header descriptions
  race_data.drop(index=0, inplace=True)
  race_data.reset_index(drop=True, inplace=True)

  race_data.rename(
    columns={
      'B02001_001E': 'total',
      'B02001_002E': 'white',
      'B02001_003E': 'black',
      'B02001_004E': 'native',
      'B02001_005E': 'asian',
      'B02001_006E': 'pac_isl',
      'B02001_007E': 'other_race'
    },
    inplace=True
  )

  race_data[['total', 'white', 'black', 'native', 'asian', 'pac_isl', 'other_race']] = race_data[
    ['total', 'white', 'black', 'native', 'asian', 'pac_isl', 'other_race']].apply(pd.to_numeric)

  race_data['two_more_races'] = race_data['total'] - (
      race_data['white'] + race_data['black'] + race_data['native'] + race_data['asian'] + race_data['pac_isl'] +
      race_data['other_race'])

  RACE_COLS = ['white', 'black', 'native', 'asian', 'pac_isl', 'other_race', 'two_more_races']

  for col in RACE_COLS:
    race_data[f'pct_{col}'] = 100 * race_data[col] / race_data['total']

  race_data.drop(columns=['total', *RACE_COLS], inplace=True)
  return race_data


def read_income_data():
  income_data = pd.read_csv(
    '../../../data/bg_covariates/ACSDT5Y2019.B19013-Data.csv',
    usecols=['GEO_ID', 'B19013_001E'],
    na_values=['-']
  )

  #   drop row corresp. to header descriptions
  income_data.drop(index=0, inplace=True)
  income_data.reset_index(drop=True, inplace=True)

  income_data.rename(
    columns={'B19013_001E': 'med_income'},
    inplace=True
  )

  income_data.replace('250,000+', '250001', inplace=True)

  income_data[['med_income']] = income_data[['med_income']].apply(pd.to_numeric)
  return income_data

def read_poverty_data():
  poverty_data = pd.read_csv(
    '../../../data/bg_covariates/ACSDT5Y2019.B29003-Data.csv',
    usecols=['GEO_ID', 'B29003_001E', 'B29003_002E', 'B29003_003E']
  )

  #   drop row corresp. to header descriptions
  poverty_data.drop(index=0, inplace=True)
  poverty_data.reset_index(drop=True, inplace=True)

  poverty_data.rename(
    columns={
      'B29003_001E': 'total',
      'B29003_002E': 'below_pov',
      'B29003_003E': 'at_above_pov'
    },
    inplace=True
  )

  poverty_data[['total', 'below_pov', 'at_above_pov']] = poverty_data[['total', 'below_pov', 'at_above_pov']].apply(
    pd.to_numeric)

  POV_STATUS_COLS = ['below_pov', 'at_above_pov']
  for col in POV_STATUS_COLS:
    poverty_data[f'pct_{col}'] = 100 * poverty_data[col] / poverty_data['total']

  poverty_data.drop(columns=['total', *POV_STATUS_COLS], inplace=True)
  return poverty_data

def read_edu_attain_data():
  edu_data = pd.read_csv(
    '../../../data/bg_covariates/ACSDT5Y2019.B29002-Data.csv',
    usecols=['GEO_ID', 'B29002_001E', 'B29002_002E', 'B29002_003E', 'B29002_004E', 'B29002_005E', 'B29002_006E',
             'B29002_007E', 'B29002_008E']
  )

  #   drop row corresp. to header descriptions
  edu_data.drop(index=0, inplace=True)
  edu_data.reset_index(drop=True, inplace=True)

  edu_data.rename(
    columns={
      'B29002_001E': 'total',
      'B29002_002E': 'less_hs',
      'B29002_003E': 'some_hs',
      'B29002_004E': 'hs_grad',
      'B29002_005E': 'some_col',
      'B29002_006E': 'assoc_deg',
      'B29002_007E': 'bach_deg',
      'B29002_008E': 'grad_deg'
    },
    inplace=True
  )

  EDU_STATUS_COLS = ['less_hs', 'some_hs', 'hs_grad', 'some_col', 'assoc_deg', 'bach_deg', 'grad_deg']

  edu_data[['total', *EDU_STATUS_COLS]] = edu_data[['total', *EDU_STATUS_COLS]].apply(pd.to_numeric)

  for col in EDU_STATUS_COLS:
    edu_data[f'pct_{col}'] = 100 * edu_data[col] / edu_data['total']

  edu_data.drop(columns=['total', *EDU_STATUS_COLS], inplace=True)
  return edu_data

def read_empl_data():
  emp_data = pd.read_csv(
    '../../../data/bg_covariates/ACSDT5Y2019.B23025-Data.csv',
    usecols=['GEO_ID', 'B23025_001E', 'B23025_007E']
  )

  #   drop row corresp. to header descriptions
  emp_data.drop(index=0, inplace=True)
  emp_data.reset_index(drop=True, inplace=True)

  emp_data.rename(
    columns={
      'B23025_001E': 'total',
      'B23025_007E': 'unempl'
    },
    inplace=True
  )

  emp_data[['total', 'unempl']] = emp_data[['total', 'unempl']].apply(pd.to_numeric)

  emp_data['pct_unempl'] = 100 * emp_data['unempl'] / emp_data['total']
  emp_data['pct_empl'] = 100. - emp_data[f'pct_unempl']

  emp_data.drop(columns=['total', 'unempl'], inplace=True)
  return emp_data

def read_vote_data():
  # Read Election Results
  vote_data = pd.read_csv(
    '../../../data/bg_covariates/votes2016_byCbg_neighbors.csv',
    usecols=['origin_cbg', 'trump_share_votes', 'clinton_share_votes']
  )

  vote_data.rename(
    columns={'origin_cbg': 'GEO_ID'},
    inplace=True
  )

  vote_data['GEO_ID'] = vote_data['GEO_ID'].astype(str)

  #   keep WA data only (WA state has FIPS code 53)
  vote_data = vote_data[vote_data['GEO_ID'].str.startswith('53')]
  #   reformat GEO ID to match Census format
  vote_data['GEO_ID'] = '1500000US' + vote_data['GEO_ID']

  vote_data[['trump_share_votes', 'clinton_share_votes']] = vote_data[
    ['trump_share_votes', 'clinton_share_votes']].apply(pd.to_numeric)

  vote_data['pct_trump'] = 100 * vote_data['trump_share_votes']
  vote_data['pct_clinton'] = 100 * vote_data['clinton_share_votes']
  vote_data['pct_3rd_p'] = 100. - vote_data['pct_trump'] - vote_data['pct_clinton']

  vote_data.drop(columns=['trump_share_votes', 'clinton_share_votes'], inplace=True)
  return vote_data

if __name__ == '__main__':
  # Read Census Data
  race_data = read_race_data()
  income_data = read_income_data()
  poverty_data = read_poverty_data()
  edu_data = read_edu_attain_data()
  emp_data = read_empl_data()
  # Read Election Result Data
  vote_data = read_vote_data()

  # Merge All Data
  merge_df = race_data.merge(income_data, on='GEO_ID', how='outer')
  merge_df = merge_df.merge(poverty_data, on='GEO_ID', how='outer')
  merge_df = merge_df.merge(edu_data, on='GEO_ID', how='outer')
  merge_df = merge_df.merge(emp_data, on='GEO_ID', how='outer')
  merge_df = merge_df.merge(vote_data, on='GEO_ID', how='outer')

  # Save Results
  merge_df.to_csv('./block_level_covariates.csv')
