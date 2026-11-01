# De Loecker and Warzynski (2012) on US industry data: findings

## In plain English

De Loecker and Warzynski found that Slovenian exporters charged markups about 7.8% higher than firms selling only
at home, and that markups rose by about 4.7% when a firm started exporting. This repository asks the industry-level
version of the question for US manufacturing in 2007, 2012 and 2017.

- **Export-oriented industries do not carry higher markups.** Aircraft (Boeing), aircraft engines (GE Aviation,
  Pratt & Whitney) and semiconductor machinery (Applied Materials, Lam Research) sell 38% to 80% of their output
  abroad, yet as a group the export-oriented half of manufacturing has the same markup as the domestic half in its
  sector. With materials as the input, a premium as large as the paper's is outside the confidence interval.
- **Selling more abroad did not raise markups.** Within an industry, a rising export share went with flat or
  slightly lower markups between 2007 and 2017, the opposite sign from the paper's export-entry effect.
- **The method's two inputs disagree.** Materials and payroll markups are negatively correlated across industries
  in the same sector. Light truck plants (Ford, GM) look barely above cost by materials and at almost 4.5 times
  cost by payroll. Only on the export premium, which both put near zero, do they agree.
- **Both inputs say manufacturing markups rose from 1958 to 2018**, from about 1.30 to 1.53 by materials and from
  1.34 to 1.76 by payroll, with the gap driven by payroll's falling share of sales.

A friendlier tour is in the [README](../README.md). The rest of this page is the technical detail.

**Key to the labels below.** *materials* and *payroll* name the flexible input $`X`$ in
$`\mu = \theta^X / \alpha^X`$. *Census* shares are NBER-CES materials or payroll over shipments; *BEA* shares are
intermediate inputs or compensation over industry output from the Use table. *high_export* = export share above the
year's median; *top_tercile* = above the 67th percentile; *export_share_10* = export share in units of 10
percentage points. *weighted* = weighted by shipments. *coef* is in log points (0.01 is about 1%). *level_effect*
converts the coefficient into markup units using the mean markup of the low-export group. *dlw_0078_inside_ci*
says whether the paper's 0.078 premium falls inside the 95% interval. Standard errors are clustered by BEA
industry. *switchers* = industries whose high_export status changes across the three years. *s_m*, *s_l* = input
shares of sales; *mu_m*, *mu_l* = markups; *rank_m_in_sector* and *rank_l_in_sector* = percentile rank within the three-digit sector.

## Table 3 analog: export status and markups across industries

`results/premium_cross_section.csv`. Regression of the log markup on export status, log employment, log capital
and sector-by-year dummies, 2007, 2012 and 2017 pooled.

| input | share_source | regressor | sample | coef | se | ci_low | ci_high | p | level_effect | low_export_mean_markup | n | industries | dlw_0078_inside_ci |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| materials | Census | high_export | all | 0.006 | 0.028 | −0.048 | 0.060 | 0.838 | 0.008 | 1.495 | 671 | 225 | False |
| materials | Census | export_share_10 | all | 0.010 | 0.009 | −0.007 | 0.027 | 0.232 | 0.016 | 1.495 | 671 | 225 | False |
| materials | Census | high_export | weighted | 0.011 | 0.038 | −0.064 | 0.086 | 0.770 | 0.017 | 1.495 | 671 | 225 | True |
| materials | Census | top_tercile | all | 0.023 | 0.027 | −0.029 | 0.076 | 0.381 | 0.035 | 1.495 | 671 | 225 | False |
| materials | Census | high_export | 2017 only | 0.033 | 0.030 | −0.026 | 0.091 | 0.271 | 0.049 | 1.486 | 224 | 224 | True |
| payroll | Census | high_export | all | 0.014 | 0.047 | −0.079 | 0.106 | 0.772 | 0.022 | 1.599 | 671 | 225 | True |
| payroll | Census | export_share_10 | all | −0.026 | 0.015 | −0.056 | 0.005 | 0.096 | −0.041 | 1.599 | 671 | 225 | False |
| payroll | Census | high_export | weighted | 0.054 | 0.059 | −0.062 | 0.171 | 0.357 | 0.090 | 1.599 | 671 | 225 | True |
| payroll | Census | top_tercile | all | −0.026 | 0.051 | −0.125 | 0.074 | 0.612 | −0.040 | 1.599 | 671 | 225 | False |
| payroll | Census | high_export | 2017 only | −0.004 | 0.051 | −0.103 | 0.096 | 0.943 | −0.006 | 1.579 | 224 | 224 | True |
| materials | BEA | high_export | all | 0.030 | 0.023 | −0.015 | 0.076 | 0.193 |  |  | 671 | 225 | False |
| materials | BEA | export_share_10 | all | 0.014 | 0.008 | −0.001 | 0.029 | 0.063 |  |  | 671 | 225 | False |
| materials | BEA | top_tercile | all | 0.038 | 0.024 | −0.009 | 0.086 | 0.114 |  |  | 671 | 225 | True |
| payroll | BEA | high_export | all | 0.042 | 0.057 | −0.070 | 0.154 | 0.461 |  |  | 671 | 225 | True |
| payroll | BEA | export_share_10 | all | −0.016 | 0.019 | −0.052 | 0.021 | 0.401 |  |  | 671 | 225 | False |
| payroll | BEA | top_tercile | all | −0.018 | 0.059 | −0.134 | 0.099 | 0.768 |  |  | 671 | 225 | True |

## Table 4 analog: export share and markups within industries

`results/premium_within.csv`. Same regression with industry and year fixed effects.

| input | share_source | regressor | coef | se | ci_low | ci_high | p | n | industries | switchers |
|---|---|---|---|---|---|---|---|---|---|---|
| materials | Census | export_share_10 | −0.015 | 0.017 | −0.049 | 0.018 | 0.368 | 671 | 225 | 24 |
| materials | Census | high_export | −0.053 | 0.029 | −0.110 | 0.005 | 0.073 | 671 | 225 | 24 |
| payroll | Census | export_share_10 | −0.067 | 0.031 | −0.128 | −0.005 | 0.034 | 671 | 225 | 24 |
| payroll | Census | high_export | −0.059 | 0.034 | −0.126 | 0.009 | 0.089 | 671 | 225 | 24 |
| materials | BEA | export_share_10 | 0.015 | 0.024 | −0.032 | 0.061 | 0.541 | 671 | 225 | 24 |
| materials | BEA | high_export | −0.029 | 0.027 | −0.081 | 0.024 | 0.283 | 671 | 225 | 24 |
| payroll | BEA | export_share_10 | −0.031 | 0.026 | −0.082 | 0.020 | 0.230 | 671 | 225 | 24 |
| payroll | BEA | high_export | −0.034 | 0.055 | −0.142 | 0.074 | 0.534 | 671 | 225 | 24 |

## Do materials and payroll agree?

`results/input_agreement.csv`. Correlations of the two log markups after removing sector-year means. Perfect
agreement would give a correlation of 1 and a disagreement share of 0.

| year | n | pearson_within_sector | pearson_p | spearman_within_sector | share_disagree_above_below_sector_mean | median_abs_gap_log_points | sd_ln_mu_m_within | sd_ln_mu_l_within |
|---|---|---|---|---|---|---|---|---|
| pooled | 671 | −0.499 | 0.000 | −0.472 | 0.657 | 0.247 | 0.183 | 0.330 |
| 2007 | 222 | −0.547 | 0.000 | −0.512 | 0.671 | 0.253 | 0.185 | 0.337 |
| 2012 | 225 | −0.532 | 0.000 | −0.502 | 0.667 | 0.250 | 0.188 | 0.347 |
| 2017 | 224 | −0.404 | 0.000 | −0.401 | 0.634 | 0.224 | 0.175 | 0.306 |

`results/input_premium_gap.csv`. Stacked regression testing whether the two inputs give the same high-export
premium.

| test | coef | se | p | n |
|---|---|---|---|---|
| high-export premium, payroll minus materials | 0.008 | 0.069 | 0.907 | 1342 |

## Named industries, 2017

`results/named_industries.csv`. The eight largest exporters by dollars, the next three by export share among
industries with at least $10 billion of output, and the six least export-oriented industries of that size. Exports
and output are in $ million.

| group | bea | bea_name | sector | export_share | exports | commodity_output | s_m | s_l | mu_m | mu_l | rank_m_in_sector | rank_l_in_sector |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| largest exporters | 336411 | Aircraft manufacturing | 336 | 0.375 | 50592 | 134840 | 0.386 | 0.111 | 2.102 | 1.518 | 1 | 0.750 |
| largest exporters | 336412 | Aircraft engine and engine parts manufacturing | 336 | 0.796 | 34535 | 43359 | 0.506 | 0.133 | 1.602 | 1.274 | 0.792 | 0.458 |
| largest exporters | 336112 | Light truck and utility vehicle manufacturing | 336 | 0.141 | 30441 | 215421 | 0.746 | 0.038 | 1.088 | 4.459 | 0.042 | 1 |
| largest exporters | 325190 | Other basic organic chemical manufacturing | 325 | 0.237 | 27845 | 117608 | 0.631 | 0.062 | 1.257 | 2.351 | 0.111 | 0.944 |
| largest exporters | 325211 | Plastics material and resin manufacturing | 325 | 0.296 | 26239 | 88537 | 0.651 | 0.070 | 1.219 | 2.087 | 0.056 | 0.889 |
| largest exporters | 334413 | Semiconductor and related device manufacturing | 334 | 0.457 | 23058 | 50455 | 0.421 | 0.219 | 1.465 | 1.462 | 0.500 | 0.500 |
| largest exporters | 336390 | Other motor vehicle parts manufacturing | 336 | 0.373 | 22810 | 61210 | 0.668 | 0.114 | 1.213 | 1.481 | 0.417 | 0.667 |
| largest exporters | 325412 | Pharmaceutical preparation manufacturing | 325 | 0.145 | 22123 | 152158 | 0.288 | 0.079 | 2.752 | 1.833 | 1 | 0.778 |
| highest export share | 333242 | Semiconductor machinery manufacturing | 333 | 0.791 | 11326 | 14325 | 0.521 | 0.290 | 1.307 | 0.975 | 0.357 | 0.107 |
| highest export share | 336413 | Other aircraft parts and auxiliary equipment manufacturing | 336 | 0.522 | 21257 | 40746 | 0.488 | 0.215 | 1.661 | 0.788 | 0.833 | 0.167 |
| highest export share | 325414 | Biological product (except diagnostic) manufacturing | 325 | 0.505 | 15804 | 31287 | 0.336 | 0.137 | 2.363 | 1.059 | 0.889 | 0.222 |
| lowest export share | 326150 | Urethane and other foam product (except polystyrene) manufacturing | 326 | 0.001 | 6 | 10600 | 0.557 | 0.134 | 1.352 | 1.532 | 0.200 | 0.600 |
| lowest export share | 33211A | All other forging, stamping, and sintering | 332 | 0.002 | 24 | 13042 | 0.559 | 0.159 | 1.183 | 1.844 | 0.100 | 0.850 |
| lowest export share | 327320 | Ready-mix concrete manufacturing | 327 | 0.003 | 91 | 30655 | 0.531 | 0.141 | 1.228 | 1.890 | 0.083 | 0.667 |
| lowest export share | 331520 | Nonferrous metal foundries | 331 | 0.006 | 77 | 12324 | 0.433 | 0.217 | 1.831 | 0.743 | 1 | 0.111 |
| lowest export share | 332800 | Coating, engraving, heat treating and allied activities | 332 | 0.007 | 179 | 26122 | 0.377 | 0.227 | 1.754 | 1.289 | 0.900 | 0.350 |
| lowest export share | 325411 | Medicinal and botanical manufacturing | 325 | 0.007 | 78 | 11136 | 0.428 | 0.170 | 1.854 | 0.855 | 0.611 | 0.111 |

## Median markups (paper's Table 2 form)

`results/median_markups.csv`. Median across NBER-CES six-digit industries, excluding input-share outliers.

| year | industries | median_markup_materials | median_markup_labor | sd_markup_materials | sd_markup_labor |
|---|---|---|---|---|---|
| 1958 | 347 | 1.270 | 1.273 | 0.265 | 0.419 |
| 1987 | 349 | 1.327 | 1.338 | 0.305 | 0.465 |
| 1997 | 352 | 1.396 | 1.425 | 0.332 | 0.573 |
| 2007 | 350 | 1.426 | 1.443 | 0.342 | 0.618 |
| 2012 | 352 | 1.423 | 1.444 | 0.351 | 0.637 |
| 2017 | 353 | 1.427 | 1.446 | 0.317 | 0.591 |

## The paper's estimator on industry data

`results/acf_estimates.csv`. OLS and Ackerberg-Caves-Frazer estimates of a Cobb-Douglas gross-output production
function (labor, capital, materials) for each three-digit sector, 1958-2016, with the median cost shares used
instead. *acf_outside_0_1* flags sectors with any elasticity below 0 or above 1.

| sector | industries | obs | ols_l | ols_k | ols_m | acf_l | acf_k | acf_m | acf_criterion | median_cost_share_m | median_cost_share_l | acf_outside_0_1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 311 | 43 | 2455 | 0.266 | 0.187 | 0.557 | 0.155 | 0.234 | 0.603 | 0.000 | 0.820 | 0.137 | False |
| 312 | 7 | 406 | 0.439 | −0.110 | 0.805 | −2.705 | 2.026 | 0.740 | 0.000 | 0.759 | 0.160 | True |
| 313 | 7 | 406 | 0.034 | 0.296 | 0.589 | 2.324 | 0.981 | −2.397 | 0.000 | 0.714 | 0.220 | True |
| 314 | 5 | 290 | 0.124 | −0.240 | 0.903 | 0.050 | −0.406 | 1.143 | 0.000 | 0.756 | 0.224 | True |
| 315 | 7 | 406 | 0.060 | −0.035 | 0.920 | 0.922 | 0.250 | 0.124 | 0.000 | 0.665 | 0.300 | False |
| 316 | 4 | 232 | 0.113 | 0.242 | 0.614 | 0.694 | 0.041 | 1.206 | 0.000 | 0.655 | 0.306 | True |
| 321 | 14 | 812 | 0.286 | −0.176 | 0.940 | 0.232 | −0.031 | 0.720 | 0.000 | 0.731 | 0.229 | True |
| 322 | 11 | 638 | 0.367 | 0.101 | 0.558 | 0.333 | 0.134 | 0.547 | 0.000 | 0.706 | 0.196 | False |
| 323 | 4 | 232 | 0.372 | 0.275 | 0.385 | 0.270 | 0.468 | 0.299 | 0.000 | 0.560 | 0.388 | False |
| 324 | 5 | 290 | −0.127 | −0.075 | 1.111 | −0.134 | −0.013 | 1.023 | 0.000 | 0.827 | 0.130 | True |
| 325 | 29 | 1682 | 0.349 | 0.128 | 0.628 | 0.077 | 0.511 | −0.007 | 0.000 | 0.769 | 0.168 | True |
| 326 | 16 | 889 | 0.165 | −0.089 | 0.978 | 0.116 | 0.056 | 0.820 | 0.000 | 0.691 | 0.261 | False |
| 327 | 18 | 1044 | 0.168 | 0.010 | 0.766 | 0.513 | 0.058 | 0.282 | 0.000 | 0.622 | 0.287 | False |
| 331 | 18 | 1044 | 0.331 | 0.012 | 0.673 | 0.273 | −0.029 | 0.786 | 0.000 | 0.749 | 0.181 | True |
| 332 | 36 | 2088 | 0.362 | 0.072 | 0.537 | 0.426 | 0.128 | 0.340 | 0.000 | 0.618 | 0.325 | False |
| 333 | 40 | 2320 | 0.270 | 0.084 | 0.647 | 0.315 | 0.129 | 0.558 | 0.000 | 0.623 | 0.331 | False |
| 334 | 24 | 1392 | 0.654 | −0.830 | 1.058 | 0.738 | −0.089 | 0.104 | 0.000 | 0.581 | 0.371 | True |
| 335 | 21 | 1218 | 0.694 | 0.100 | 0.285 | 0.661 | 0.085 | 0.336 | 0.000 | 0.690 | 0.261 | False |
| 336 | 27 | 1566 | 0.389 | 0.077 | 0.576 | 0.157 | 0.103 | 0.715 | 0.000 | 0.717 | 0.242 | False |
| 337 | 12 | 696 | 0.375 | 0.200 | 0.425 | 0.142 | 0.083 | 0.863 | 0.000 | 0.622 | 0.334 | False |
| 339 | 16 | 889 | 0.166 | 0.166 | 0.650 | 0.294 | −0.008 | 0.751 | 0.000 | 0.610 | 0.338 | True |

## Manufacturing markups by year

`results/markup_trend.csv`. Sales-weighted markups and aggregate input shares. *theta_m_mean* and *theta_l_mean*
are sales-weighted cost-share elasticities.

| year | industries | markup_materials | markup_labor | materials_share_of_sales | payroll_share_of_sales | theta_m_mean | theta_l_mean |
|---|---|---|---|---|---|---|---|
| 1958 | 347 | 1.302 | 1.344 | 0.538 | 0.240 | 0.675 | 0.293 |
| 1959 | 348 | 1.279 | 1.343 | 0.549 | 0.227 | 0.679 | 0.277 |
| 1960 | 347 | 1.280 | 1.364 | 0.541 | 0.236 | 0.671 | 0.292 |
| 1961 | 347 | 1.281 | 1.348 | 0.537 | 0.239 | 0.668 | 0.291 |
| 1962 | 347 | 1.285 | 1.386 | 0.536 | 0.236 | 0.668 | 0.293 |
| 1963 | 348 | 1.304 | 1.416 | 0.531 | 0.231 | 0.670 | 0.290 |
| 1964 | 348 | 1.315 | 1.404 | 0.530 | 0.229 | 0.674 | 0.288 |
| 1965 | 348 | 1.317 | 1.424 | 0.532 | 0.225 | 0.678 | 0.286 |
| 1966 | 348 | 1.321 | 1.419 | 0.533 | 0.226 | 0.681 | 0.287 |
| 1967 | 348 | 1.347 | 1.394 | 0.521 | 0.230 | 0.679 | 0.289 |
| 1968 | 349 | 1.347 | 1.430 | 0.519 | 0.228 | 0.674 | 0.295 |
| 1969 | 348 | 1.336 | 1.422 | 0.521 | 0.228 | 0.675 | 0.295 |
| 1970 | 349 | 1.334 | 1.413 | 0.518 | 0.232 | 0.668 | 0.299 |
| 1971 | 348 | 1.333 | 1.437 | 0.518 | 0.223 | 0.668 | 0.293 |
| 1972 | 348 | 1.305 | 1.494 | 0.524 | 0.221 | 0.657 | 0.293 |
| 1973 | 348 | 1.333 | 1.538 | 0.530 | 0.213 | 0.679 | 0.290 |
| 1974 | 348 | 1.348 | 1.546 | 0.550 | 0.199 | 0.719 | 0.273 |
| 1975 | 348 | 1.333 | 1.508 | 0.552 | 0.196 | 0.710 | 0.266 |
| 1976 | 349 | 1.304 | 1.511 | 0.560 | 0.189 | 0.702 | 0.256 |
| 1977 | 350 | 1.318 | 1.536 | 0.554 | 0.190 | 0.703 | 0.260 |
| 1978 | 349 | 1.314 | 1.523 | 0.555 | 0.190 | 0.704 | 0.258 |
| 1979 | 349 | 1.356 | 1.521 | 0.550 | 0.189 | 0.719 | 0.260 |
| 1980 | 350 | 1.361 | 1.499 | 0.552 | 0.190 | 0.722 | 0.258 |
| 1981 | 350 | 1.307 | 1.437 | 0.553 | 0.188 | 0.692 | 0.245 |
| 1982 | 351 | 1.306 | 1.426 | 0.537 | 0.193 | 0.667 | 0.250 |
| 1983 | 349 | 1.279 | 1.462 | 0.539 | 0.188 | 0.659 | 0.248 |
| 1984 | 349 | 1.287 | 1.481 | 0.544 | 0.185 | 0.668 | 0.246 |
| 1985 | 349 | 1.304 | 1.490 | 0.536 | 0.187 | 0.666 | 0.251 |
| 1986 | 350 | 1.337 | 1.515 | 0.526 | 0.187 | 0.669 | 0.254 |
| 1987 | 349 | 1.365 | 1.551 | 0.519 | 0.183 | 0.675 | 0.251 |
| 1988 | 349 | 1.401 | 1.596 | 0.522 | 0.176 | 0.693 | 0.245 |
| 1989 | 350 | 1.371 | 1.584 | 0.530 | 0.176 | 0.695 | 0.242 |
| 1990 | 350 | 1.383 | 1.593 | 0.530 | 0.176 | 0.700 | 0.247 |
| 1991 | 349 | 1.418 | 1.557 | 0.519 | 0.175 | 0.698 | 0.243 |
| 1992 | 350 | 1.425 | 1.605 | 0.512 | 0.173 | 0.688 | 0.246 |
| 1993 | 349 | 1.459 | 1.632 | 0.515 | 0.167 | 0.704 | 0.240 |
| 1994 | 348 | 1.428 | 1.687 | 0.520 | 0.161 | 0.698 | 0.235 |
| 1995 | 348 | 1.407 | 1.662 | 0.529 | 0.158 | 0.707 | 0.229 |
| 1996 | 349 | 1.429 | 1.683 | 0.526 | 0.157 | 0.710 | 0.230 |
| 1997 | 352 | 1.445 | 1.802 | 0.516 | 0.156 | 0.705 | 0.238 |
| 1998 | 352 | 1.444 | 1.802 | 0.515 | 0.156 | 0.707 | 0.240 |
| 1999 | 352 | 1.440 | 1.843 | 0.514 | 0.156 | 0.703 | 0.242 |
| 2000 | 353 | 1.453 | 1.775 | 0.516 | 0.157 | 0.706 | 0.241 |
| 2001 | 352 | 1.462 | 1.796 | 0.516 | 0.160 | 0.708 | 0.246 |
| 2002 | 351 | 1.512 | 1.784 | 0.495 | 0.157 | 0.701 | 0.242 |
| 2003 | 351 | 1.533 | 1.829 | 0.500 | 0.152 | 0.710 | 0.237 |
| 2004 | 351 | 1.545 | 1.854 | 0.504 | 0.145 | 0.720 | 0.228 |
| 2005 | 349 | 1.526 | 1.840 | 0.517 | 0.138 | 0.735 | 0.216 |
| 2006 | 349 | 1.529 | 1.850 | 0.521 | 0.134 | 0.738 | 0.210 |
| 2007 | 350 | 1.529 | 1.795 | 0.520 | 0.133 | 0.738 | 0.203 |
| 2008 | 350 | 1.500 | 1.818 | 0.540 | 0.131 | 0.751 | 0.204 |
| 2009 | 350 | 1.520 | 1.747 | 0.515 | 0.137 | 0.729 | 0.208 |
| 2010 | 351 | 1.505 | 1.797 | 0.529 | 0.130 | 0.749 | 0.198 |
| 2011 | 351 | 1.494 | 1.837 | 0.548 | 0.124 | 0.765 | 0.192 |
| 2012 | 352 | 1.491 | 1.774 | 0.548 | 0.125 | 0.767 | 0.189 |
| 2013 | 352 | 1.483 | 1.769 | 0.545 | 0.125 | 0.761 | 0.187 |
| 2014 | 351 | 1.477 | 1.769 | 0.547 | 0.123 | 0.764 | 0.185 |
| 2015 | 350 | 1.490 | 1.730 | 0.529 | 0.131 | 0.747 | 0.193 |
| 2016 | 352 | 1.530 | 1.799 | 0.523 | 0.132 | 0.751 | 0.203 |
| 2017 | 353 | 1.514 | 1.746 | 0.528 | 0.135 | 0.752 | 0.203 |
| 2018 | 351 | 1.535 | 1.762 | 0.529 | 0.132 | 0.754 | 0.203 |

## User cost of capital

`results/user_cost.csv`. Ten-year Treasury yield minus CPI inflation plus implied depreciation, used to charge
capital in the cost shares.

| year | treasury_10y | cpi_inflation | depreciation | user_cost |
|---|---|---|---|---|
| 1958 | 0.033 | 0.027 | 0.049 | 0.055 |
| 1959 | 0.043 | 0.009 | 0.049 | 0.083 |
| 1960 | 0.041 | 0.015 | 0.038 | 0.064 |
| 1961 | 0.039 | 0.011 | 0.043 | 0.071 |
| 1962 | 0.040 | 0.012 | 0.043 | 0.070 |
| 1963 | 0.040 | 0.013 | 0.044 | 0.071 |
| 1964 | 0.042 | 0.013 | 0.044 | 0.073 |
| 1965 | 0.043 | 0.016 | 0.041 | 0.068 |
| 1966 | 0.049 | 0.030 | 0.041 | 0.060 |
| 1967 | 0.051 | 0.028 | 0.037 | 0.059 |
| 1968 | 0.057 | 0.042 | 0.040 | 0.054 |
| 1969 | 0.067 | 0.054 | 0.042 | 0.055 |
| 1970 | 0.073 | 0.059 | 0.041 | 0.055 |
| 1971 | 0.062 | 0.042 | 0.044 | 0.063 |
| 1972 | 0.062 | 0.033 | 0.048 | 0.077 |
| 1973 | 0.068 | 0.063 | 0.043 | 0.049 |
| 1974 | 0.076 | 0.110 | 0.048 | 0.013 |
| 1975 | 0.080 | 0.091 | 0.047 | 0.035 |
| 1976 | 0.076 | 0.058 | 0.049 | 0.067 |
| 1977 | 0.074 | 0.065 | 0.048 | 0.057 |
| 1978 | 0.084 | 0.076 | 0.052 | 0.059 |
| 1979 | 0.094 | 0.113 | 0.051 | 0.032 |
| 1980 | 0.115 | 0.135 | 0.052 | 0.032 |
| 1981 | 0.139 | 0.104 | 0.056 | 0.091 |
| 1982 | 0.130 | 0.062 | 0.052 | 0.121 |
| 1983 | 0.111 | 0.032 | 0.056 | 0.135 |
| 1984 | 0.124 | 0.044 | 0.059 | 0.140 |
| 1985 | 0.106 | 0.035 | 0.059 | 0.131 |
| 1986 | 0.077 | 0.019 | 0.059 | 0.116 |
| 1987 | 0.084 | 0.036 | 0.062 | 0.110 |
| 1988 | 0.088 | 0.041 | 0.052 | 0.099 |
| 1989 | 0.085 | 0.048 | 0.066 | 0.103 |
| 1990 | 0.086 | 0.054 | 0.055 | 0.086 |
| 1991 | 0.079 | 0.042 | 0.051 | 0.087 |
| 1992 | 0.070 | 0.030 | 0.058 | 0.098 |
| 1993 | 0.059 | 0.030 | 0.056 | 0.085 |
| 1994 | 0.071 | 0.026 | 0.062 | 0.107 |
| 1995 | 0.066 | 0.028 | 0.066 | 0.103 |
| 1996 | 0.064 | 0.029 | 0.063 | 0.098 |
| 1997 | 0.064 | 0.023 | 0.059 | 0.099 |
| 1998 | 0.053 | 0.015 | 0.053 | 0.090 |
| 1999 | 0.056 | 0.022 | 0.052 | 0.087 |
| 2000 | 0.060 | 0.034 | 0.057 | 0.084 |
| 2001 | 0.050 | 0.028 | 0.051 | 0.073 |
| 2002 | 0.046 | 0.016 | 0.048 | 0.078 |
| 2003 | 0.040 | 0.023 | 0.053 | 0.071 |
| 2004 | 0.043 | 0.027 | 0.059 | 0.075 |
| 2005 | 0.043 | 0.034 | 0.067 | 0.076 |
| 2006 | 0.048 | 0.032 | 0.065 | 0.081 |
| 2007 | 0.046 | 0.029 | 0.078 | 0.096 |
| 2008 | 0.037 | 0.038 | 0.074 | 0.072 |
| 2009 | 0.033 | −0.003 | 0.050 | 0.086 |
| 2010 | 0.032 | 0.016 | 0.066 | 0.082 |
| 2011 | 0.028 | 0.031 | 0.075 | 0.072 |
| 2012 | 0.018 | 0.021 | 0.075 | 0.072 |
| 2013 | 0.024 | 0.015 | 0.074 | 0.083 |
| 2014 | 0.025 | 0.016 | 0.068 | 0.077 |
| 2015 | 0.021 | 0.001 | 0.071 | 0.091 |
| 2016 | 0.018 | 0.013 | 0.065 | 0.071 |
| 2017 | 0.023 | 0.021 | 0.065 | 0.067 |
| 2018 | 0.029 | 0.024 | 0.065 | 0.070 |

## Data files in results/

`markups_industry_year.csv` has one row per NBER-CES industry-year (22,087 rows) with shares, elasticities, both
markups and the outlier flag. `industry_panel.csv` has the 671 BEA industry-years used in the regressions.
`theta_cost_share.csv` has the cost-share elasticities for each sector and year. Figures are
`export_vs_markup.png`, `input_agreement.png` and `markup_trend.png`.
