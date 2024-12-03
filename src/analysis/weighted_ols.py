from utils import setup_anlaysis_df

import numpy as np
import matplotlib.pyplot as plt

from scipy.sparse import spdiags
from scipy.sparse.linalg import bicgstab


# SECTION 1: Read and Merge Data
merged_df = setup_anlaysis_df()


# SECTION 2: Data Analysis
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
