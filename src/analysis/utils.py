import pandas as pd

def setup_anlaysis_df():
  # SECTION 1: Read and Merge Data
  # read registration data about voting blocks
  block_vote_df = pd.read_csv('../scripts/block-group-assignment/aggr_votr_out.csv',
                              usecols=['geo_id', 'total_voting_age_pop', 'num_voted'])
  print('block_vote_df num blocks', block_vote_df['geo_id'].nunique())

  # read average distance of voters to dropboxes in each voting block
  dropbox_dist_df = pd.read_csv('../scripts/ballot-box-dist/find_dist_out.csv',
                                usecols=['geo_id', 'dist_to_nearest_ballot_box_km'])
  print('dropbox_dist_df num blocks', dropbox_dist_df['geo_id'].nunique())

  # merge dataframes
  merged_df = pd.merge(block_vote_df, dropbox_dist_df, on='geo_id', how='inner')
  print('merged_df num blocks', merged_df['geo_id'].nunique())

  # SECTION 2: EDA, Data Cleanup, and Data Augmentation
  # EDA
  #   there are 14 blocks with no registration info
  print(merged_df[merged_df.isna().any(axis=1)].shape)
  #   there are 21 districts with more voters than eligible voters
  print(merged_df[merged_df['total_voting_age_pop'] < merged_df['num_voted']].shape)
  #   there's one more district with 1 voter and 0 population
  print(merged_df[merged_df['total_voting_age_pop'] == 0].shape)

  # clean up
  #   remove blocks with missing data
  merged_df = merged_df[~merged_df.isna().any(axis=1)]
  #   remove blocks with no voters
  merged_df = merged_df[merged_df['num_voted'] != 0]
  #   replace 0 populations with assoc. vote counts
  merged_df['total_voting_age_pop'] = merged_df['num_voted'].where(merged_df['total_voting_age_pop'] == 0,
                                                                   merged_df['total_voting_age_pop'])
  print(merged_df.shape)

  # data augmentation
  #   calculate the proportion of each block that voted
  merged_df['prop_voted'] = merged_df['num_voted'] / merged_df['total_voting_age_pop']
  return merged_df