# Technical notes

This is the technical companion to the [README](README.md). It covers the data, the method, the full set of test
statistics and how to reproduce everything. Every table is in [results/FINDINGS.md](results/FINDINGS.md).

## The original study

Jan De Loecker and Frederic Warzynski, "Markups and Firm-Level Export Status," *American Economic Review* 102(6),
2012, pp. 2437–2471; NBER Working Paper 15198 (July 2009, revised October 2010). Using all Slovenian manufacturing
firms 1994–2000 (7,915 firms), the authors recover firm markups as the output elasticity of a flexible input over
its revenue share, with elasticities from proxy-method production functions. The figures below are from the
October 2010 working paper, the version read for this repository: median markups of 1.10 to 1.28 across
specifications I–VI (Table 2); an exporter premium of about 7.8% (Section 5.2.1), 0.163 in levels with s.e. 0.017
in specification I (Table 3); and a 4.7% rise in markups on export entry, s.e. 1.3% (Table 4).

## Headline results

| Test | Materials | Payroll |
|---|---|---|
| Export-oriented premium, log points (s.e.) | 0.006 (0.028) | 0.014 (0.047) |
| 95% CI | [−0.048, 0.060] | [−0.079, 0.106] |
| Paper's 0.078 inside the CI | no | yes |
| Within-industry, per 10 pp export share | −0.015 (0.017) | −0.067 (0.031) |
| Within-industry, becoming export-oriented | −0.053 (0.029) | −0.059 (0.034) |
| Median industry markup, 2017 | 1.427 | 1.446 |
| Sales-weighted markup, 1958 → 2018 | 1.302 → 1.535 | 1.344 → 1.762 |

Materials and payroll markups, each measured relative to its sector-year mean, have a Pearson correlation of
−0.499 and a Spearman correlation of −0.472 (N = 671). The two inputs put an industry on opposite sides of its
sector mean in 65.7% of industry-years. Their export premiums do not differ (gap 0.008, s.e. 0.069, p = 0.91).

## Data

| File in `data/raw/` | Source | Used for |
|---|---|---|
| `nberces5818v1_n2012.csv` | NBER-CES Manufacturing Industry Database, 2021 release (Becker, Gray and Marvakov), NAICS 2012, data.nber.org/nberces | shipments, materials, payroll, employment, capital, deflators, 364 industries, 1958–2018 |
| `IOUse_Before_Redefinitions_PRO_2017_Detail.xlsx` | BEA, AllTablesIO.zip, detailed Use table before redefinitions in producers' prices, sheets 2007, 2012, 2017, plus the "NAICS Codes" concordance | exports (F04000), commodity output, compensation (V00100), intermediate inputs (T005), industry output (T008) |
| `fred_GS10.csv` | FRED, 10-year Treasury constant maturity | user cost of capital |
| `fred_CPIAUCSL.csv` | FRED, CPI for all urban consumers | user cost of capital |

All files were downloaded on November 1, 2026. The two FRED files were copied unchanged from same-day FRED
downloads.

## Method

Rules fixed before looking at results:

1. **Markups.** For each NBER-CES industry-year, $`\mu^X_{it} = \theta^X_{s(i)t} / \alpha^X_{it}`$ with
   $`X`$ = materials (`matcost`, which includes energy) or payroll (`pay`), and $`\alpha^X`$ the input's share of
   shipments (`vship`).
2. **Elasticities.** Cost shares, the median within each three-digit NAICS sector and year, assuming constant
   returns.

   ```math
   \theta^X_{st} = \operatorname{median}_{i \in s}\ \frac{P^X X_{it}}{P^M M_{it} + W L_{it} + r_t P^K K_{it}}
   ```

   The rental rate is $`r_t = i_t - \pi_t + \delta_t`$, with $`i_t`$ the annual mean ten-year Treasury yield,
   $`\pi_t`$ CPI inflation and $`\delta_t`$ the depreciation rate implied by the NBER-CES capital accounts,
   $`\delta_t = 1 - (K_t - I_t/p^I_t)/K_{t-1}`$, summed over manufacturing. It averages 0.078 over 1958–2018.
3. **Capital after 2016.** NBER-CES capital and the investment deflator end in 2016; 2017 and 2018 use the 2016
   values, including the 2016 depreciation rate. 1958 has no lagged stock and uses the 1959 depreciation rate.
4. **Outliers.** Industry-years with a materials or payroll share in the top or bottom 1% of their year are flagged
   and excluded from medians, trends and regressions (764 of 22,087; 37 in the benchmark years). Because the flag is
   applied before aggregation, a BEA industry that groups several NBER-CES industries loses only the flagged one;
   this changes the composition of 7 BEA industries in some benchmark years.
5. **Unit of comparison.** NBER-CES industries are mapped to BEA detail industries by longest NAICS prefix in the
   BEA concordance, plus six NAICS 2012 codes that NAICS 2017 merged (333911 and 333913 to 333914; 335221, 335222,
   335224 and 335228 to 335220). Sums of shipments, materials, payroll, employment and capital are taken within
   each BEA industry. One grouping (331314) has no BEA commodity row. The panel is 671 industry-years, 225
   industries.
6. **Export status.** Export share is BEA exports over total commodity output. "Export-oriented" means above the
   year's median export share.
7. **Cross-section test** (the paper's equation 17), with sector-year effects and standard errors clustered by BEA
   industry.

   ```math
   \ln \mu^X_{it} = \delta_0 + \delta_1\,\text{EXP}_{it} + \gamma_1 \ln L_{it} + \gamma_2 \ln K_{it} + \lambda_{s(i)t} + \varepsilon_{it}
   ```

   Under Cobb-Douglas, $`\ln \mu^X_{it} = \ln \theta^X_{s(i)t} - \ln \alpha^X_{it}`$, so $`\lambda_{s(i)t}`$
   absorbs the elasticity and $`\hat\delta_1`$ is the same for any estimator of $`\theta`$.
8. **Within test** (analog of Table 4): the same regression with industry and year effects in place of
   sector-year effects.
9. **Robustness, specified in advance:** shipment weights; 2017 only; top-tercile dummy; continuous export share;
   input shares from the BEA Use table (intermediate inputs over output, compensation over output).
10. **Extension (Raval 2023).** Correlation of sector-year-demeaned log markups from the two inputs, the share of
    industry-years on opposite sides of the sector mean, and a stacked regression testing equal export premiums.

**Why no production-function elasticity.** `src/markups.py` estimates a Cobb-Douglas gross-output production
function for each sector by Ackerberg, Caves and Frazer's two-step method with materials as the proxy, a cubic
first stage with year dummies, a cubic productivity process and moments on $`(k_t, l_{t-1}, m_{t-1})`$. Ten of the
21 sectors return an elasticity outside [0, 1], with materials elasticities from −2.40 to 1.21
(`results/acf_estimates.csv`). When the flexible input is also the proxy, the gross-output elasticity is not
separately identified (Gandhi, Navarro and Rivers 2020; Bond et al. 2021). Because sector-year effects absorb the
elasticity, the export tests do not depend on this choice; markup levels and the Raval comparison across sectors
do.

## Full test statistics

Cross-section, Census input shares, N = 671 except 2017 only (N = 224):

| Input | Regressor | Sample | Coef. | s.e. | p | 95% CI |
|---|---|---|---|---|---|---|
| Materials | above median | all | 0.006 | 0.028 | 0.84 | [−0.048, 0.060] |
| Materials | export share ×10 | all | 0.010 | 0.009 | 0.23 | [−0.007, 0.027] |
| Materials | above median | weighted | 0.011 | 0.038 | 0.77 | [−0.064, 0.086] |
| Materials | top tercile | all | 0.023 | 0.027 | 0.38 | [−0.029, 0.076] |
| Materials | above median | 2017 only | 0.033 | 0.030 | 0.27 | [−0.026, 0.091] |
| Payroll | above median | all | 0.014 | 0.047 | 0.77 | [−0.079, 0.106] |
| Payroll | export share ×10 | all | −0.026 | 0.015 | 0.10 | [−0.056, 0.005] |
| Payroll | above median | weighted | 0.054 | 0.059 | 0.36 | [−0.062, 0.171] |
| Payroll | top tercile | all | −0.026 | 0.051 | 0.61 | [−0.125, 0.074] |
| Payroll | above median | 2017 only | −0.004 | 0.051 | 0.94 | [−0.103, 0.096] |

With BEA input shares (N = 671): materials 0.030 (0.023, p = 0.19) for the dummy and 0.014 (0.008, p = 0.06) per
10 points; payroll 0.042 (0.057, p = 0.46) and −0.016 (0.019, p = 0.40). Within-industry estimates with BEA shares:
materials 0.015 (0.024) and −0.029 (0.027); payroll −0.031 (0.026) and −0.034 (0.055). Only 24 industries change
export-oriented status across the three years.

## Reproducing the results

```bash
pip install -r requirements.txt     # Python 3.12 or later
python src/markups.py               # NBER-CES markups, elasticities, trend
python src/exporters.py             # export tests and the two-input comparison
```

Everything runs offline from `data/raw/` in under a minute and rewrites `results/`.

## Repository layout

| Path | What it is |
|---|---|
| `src/markups.py` | Elasticities (cost shares and ACF), markups for 364 industries, 1958–2018 |
| `src/exporters.py` | BEA export shares, concordance, Table 3 and Table 4 analogs, Raval comparison |
| `results/*.csv`, `results/*.png` | Every number and figure in the README |

## References

- Ackerberg, D., Caves, K. & Frazer, G. (2015). Identification properties of recent production function
  estimators. *Econometrica* 83(6).
- Becker, R., Gray, W. & Marvakov, J. (2021). NBER-CES Manufacturing Industry Database (1958–2018, version 2021a).
- Bond, S., Hashemi, A., Kaplan, G. & Zoch, P. (2021). Some unpleasant markup arithmetic. *Journal of Monetary
  Economics* 121, 1–14.
- De Loecker, J., Eeckhout, J. & Unger, G. (2020). The rise of market power and the macroeconomic implications.
  *QJE* 135(2), 561–644.
- De Loecker, J. & Warzynski, F. (2012). Markups and firm-level export status. *AER* 102(6), 2437–2471.
- Foster, L., Haltiwanger, J. & Syverson, C. (2008). Reallocation, firm turnover, and efficiency. *AER* 98(1).
- Gandhi, A., Navarro, S. & Rivers, D. (2020). On the identification of gross output production functions.
  *Journal of Political Economy* 128(8).
- Hall, R. (1988). The relation between price and marginal cost in U.S. industry. *JPE* 96(5).
- Raval, D. (2023). Testing the production approach to markup estimation. *Review of Economic Studies* 90(5),
  2592–2611.
