from utils import setup_anlaysis_df
import pandas as pd

if __name__ == '__main__':
  # SECTION 1: Read distance data
  merged_df = setup_anlaysis_df()

  # SECTION 2: Read covariate data
  cov_df = pd.read_csv('../scripts/block-group-covariates/block_level_covariates.csv')

  # cleanup
  cov_df.drop(columns='Unnamed: 0', inplace=True)
  cov_df.rename(columns={'GEO_ID': 'geo_id'}, inplace=True)

  # remove perfectly collinear columns
  cov_df.drop(columns=['pct_two_more_races', 'pct_at_above_pov', 'pct_grad_deg', 'pct_empl', 'pct_3rd_p'], inplace=True)

  #   remove blocks with missing data
  cov_df = cov_df[~cov_df.isna().any(axis=1)]

  # SECTION 3: Merge covariate and distance data
  # merge in the covariates
  merged_df = pd.merge(merged_df, cov_df, on='geo_id', how='left')

  ## SECTION 3.1 Save results as csv
  # save one dataframe with only complete rows
  no_nan_df = merged_df[~merged_df.isna().any(axis=1)]
  print(no_nan_df.shape)
  no_nan_df.to_csv('./merged_covs_nonan.csv', index=False)

  # impute columns with mean
  for col in merged_df.columns:
    if col == 'geo_id':
      continue
    merged_df[col] = merged_df[col].fillna(merged_df[col].median())
  # save another dataframe with imputed data as well
  imputed_df = merged_df[~merged_df.isna().any(axis=1)]
  print(imputed_df.shape)
  imputed_df.to_csv('./merged_covs_impute.csv', index=False)