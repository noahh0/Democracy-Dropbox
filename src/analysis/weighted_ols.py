import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.sparse import spdiags
from scipy.sparse.linalg import bicgstab


# SECTION 1: Read and Merge Data
# read registration data about voting blocks
block_vote_df = pd.read_csv('../scripts/block-group-assignment/aggr_votr_out.csv', usecols=['geo_id', 'total_voting_age_pop', 'num_voted'])
print('block_vote_df num blocks', block_vote_df['geo_id'].nunique())

# read average distance of voters to dropboxes in each voting block
dropbox_dist_df = pd.read_csv('../scripts/ballot-box-dist/find_dist_out.csv', usecols=['geo_id', 'dist_to_nearest_ballot_box_km'])
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
merged_df['total_voting_age_pop'] = merged_df['num_voted'].where(merged_df['total_voting_age_pop'] == 0, merged_df['total_voting_age_pop'])
print(merged_df.shape)

# data augmentation
#   calculate the proportion of each block that voted
merged_df['prop_voted'] = merged_df['num_voted']/merged_df['total_voting_age_pop']


# SECTION 3: Data Analysis
def get_ols(X, y):
  beta_hat, code = bicgstab(X.T @ X, X.T @ y)
  assert code == 0

  y_hat = X @ beta_hat
  r_sq = 1 - np.var(y - y_hat, ddof=0) / np.var(y, ddof=0)
  return beta_hat, y_hat, r_sq

def get_weighted_ols(X, y, W):
  beta_hat, code = bicgstab(X.T @ W @ X, X.T @ W @ y)
  assert code == 0

  y_hat = X @ beta_hat
  r_sq = 1 - np.var(W @ (y - y_hat), ddof=0) / np.var(W @ y, ddof=0)
  return beta_hat, y_hat, r_sq

def plot_ols(X, y, beta_hat, r_sq, model_name = ''):
  plt.scatter(X[:, 0], y)
  max_dist = np.max(X[:, 0])
  plt.plot([0, max_dist], [beta_hat[1], beta_hat[0] * max_dist + beta_hat[1]],
           linestyle='--', c='k',
           label='$\hat{p} = $' + f'{beta_hat[0]:.4e} d + {beta_hat[1]:.4e}\n($r^2$ = {r_sq:0.4f})')
  plt.xlabel('Distance to Nearest Ballot Dropbox')
  plt.ylabel('Proportion of Voters who Turned Out')
  plt.suptitle(f'Voter Turnout vs Mean Distance to Dropbox {model_name}')
  plt.title('in WA Voting Blocks for the 2020 General Election')
  plt.legend()

# analysis 0- unweighted model, no processing
N = merged_df.shape[0]

# explanatory variables are the distance to a drop box and bias
X = np.stack((merged_df['dist_to_nearest_ballot_box_km'], np.ones((N, ))), axis=-1)
# the response variable is the proportion of voters who voted
y = merged_df['prop_voted']

beta_hat, y_hat, r_sq = get_ols(X, y)
plot_ols(X, y, beta_hat, r_sq, '(Unweighted Model)')
plt.tight_layout()
plt.show()

# analysis 1- weighted model, no processing
# weight districts by their count of eligible voters
W = spdiags(merged_df['total_voting_age_pop'], [0], N, N)

beta_hat, y_hat, r_sq = get_weighted_ols(X, y, W)
plot_ols(X, y, beta_hat, r_sq, '(Weighted Model)')
plt.tight_layout()
plt.show()

# analysis 2- unweighted model, cap proportions to 1
y_cap = merged_df['prop_voted'].where(merged_df['prop_voted'] < 1., 1.)
print('Max y cap', max(y_cap))

beta_hat, y_hat, r_sq = get_ols(X, y_cap)
plot_ols(X, y_cap, beta_hat, r_sq, '(Unweighted Model)')
plt.tight_layout()
plt.show()

# analysis 3- cap proportions to 1
# the response variable is the proportion of voters who voted, capped to 1
beta_hat, y_hat, r_sq = get_weighted_ols(X, y_cap, W)
plot_ols(X, y_cap, beta_hat, r_sq, '(Weighted Model)')
plt.tight_layout()
plt.show()
