library('dplyr')
library('tidyplots')
devtools::source_url("https://raw.githubusercontent.com/MatthieuStigler/Misconometrics/master/Gelbach_decompo/dec_covar.R")

# read in data
df = read.csv('./merged_covs_nonan.csv')

# cap proportions to 1
df = df %>% rowwise() %>% mutate(prop_voted = min(c(1, prop_voted)))

# run OLS regression with only distance variable weighted on `total_voting_age_pop`
dist_only_model = lm(
  prop_voted ~ dist_to_nearest_ballot_box_km,
  weights = df$total_voting_age_pop, data = df
)
print(summary.lm(dist_only_model))

# run full OLS regression weighted on `total_voting_age_pop`
full_model = lm(
  prop_voted ~ dist_to_nearest_ballot_box_km + med_income + pct_white + pct_black + pct_native + pct_asian + pct_pac_isl + pct_other_race + pct_below_pov + pct_less_hs + pct_some_hs + pct_hs_grad + pct_some_col + pct_assoc_deg + pct_bach_deg + pct_unempl + pct_trump + pct_clinton,
  weights = df$total_voting_age_pop, data = df
)
print(summary.lm(full_model))

dec <- dec_covar(object = full_model, var_main = "dist_to_nearest_ballot_box_km")
print(summary(dec))


dist_effects = data.frame(delta=dec$delta_dist_to_nearest_ballot_box_km, row.names = dec$covariate)
dist_effects$covariate = dec$covariate
dist_effects$base_coeff = rep(dist_only_model$coefficients['dist_to_nearest_ballot_box_km'], length(dec$covariate))
dist_effects$full_coeff = rep(full_model$coefficients['dist_to_nearest_ballot_box_km'], length(dec$covariate))
dist_effects$adj_base_coeff = dist_effects$base_coeff + dist_effects$delta

# remove values created by dec_covar command
dist_effects = dist_effects[!(row.names(dist_effects) %in% c('Total', 'Check')), ]

ggplot(dist_effects, aes(x = adj_base_coeff, y = covariate)) + 
  geom_point(colour='black', size=1) + 
  geom_vline(aes(xintercept=full_model$coefficients['dist_to_nearest_ballot_box_km'], colour='Full'), linetype='dashed') +
  geom_vline(aes(xintercept=dist_only_model$coefficients['dist_to_nearest_ballot_box_km'], colour='DistOnly')) + 
  geom_segment(aes(x=base_coeff, xend=adj_base_coeff, y=covariate, yend=covariate, colour='black')) +
  scale_color_manual(values = c('Full'='blue', 'DistOnly' = 'black')) +
  labs(x='Regr Coeff for Avg Dist', y='Covariate', colour='Model', title='Effect of Covariate Coeffs on Coeff for Avg Dist')
