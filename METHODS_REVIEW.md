# Methods review: De Loecker and Warzynski (2012)

- **Paper:** De Loecker, J. & Warzynski, F. (2012). "Markups and Firm-Level Export Status." *American Economic
  Review* 102(6), 2437–2471. Circulated as NBER Working Paper 15198, July 2009, revised October 2010.
- **Statistical focus:** the exporter markup premium (Table 3, about 7.8% in logs, 0.163 in levels in
  specification I) and the export-entry effect (Table 4, 4.7%), together with the firm-level markups they rest on
  (Table 2).
- **Review standard:** current AEA Data and Code Availability Policy and standard reporting of estimates,
  uncertainty and sample construction; internal consistency of the identifying assumptions for the production
  approach.
- **What was read:** the full text of NBER Working Paper 15198, revision dated October 2010, including Appendices
  A to D, downloaded from nber.org and read from a text conversion of the PDF; the NBER abstract page for w15198; the RePEc abstract pages for Bond, Hashemi,
  Kaplan and Zoch (2021) and Raval (2023). The published *AER* article was not read. Table numbers and estimates
  below refer to the working paper and may differ from the published version.

## Methods summary

### Research design

Observational panel study. Step one estimates a production function separately for each industry (Appendix A
lists the two-digit NACE industries)
with a control-function (proxy) method, following Ackerberg, Caves and Frazer, using materials to proxy for
productivity. Step two computes each firm's markup as the estimated output elasticity of a variable input
(labor in specifications I to V, materials in VI) divided by that input's share of sales. Step three regresses
log markups on export status (cross section, equation 17) and on export entry and exit indicators (equation 19).
The authors state that the export coefficient is not interpreted causally.

### Sampling strategy

Census of Slovenian manufacturing firms from the Slovenian Central Statistical Office, full company accounts,
1994–2000. No sampling in the statistical sense; the population is all active manufacturing establishments.

### Sample size

7,915 firms in the unbalanced panel (Section 4 and Appendix A). Restricting to firms that report employment leaves
6,391 firms and 29,804 firm-years (Appendix A). Table 1 reports 3,820 to 4,906 firms per year for 1995–2000. The
regression tables do not report the number of observations used.

### Inclusion and exclusion criteria

Firms must report employment (Appendix A). For the entry regressions, the small fraction of firms that enter or
exit exporting more than once is dropped (footnote 38). No trimming rule for extreme markups or input shares is
described.

### Independent and dependent variables

Dependent variable: log firm markup, computed from estimated elasticities and observed input shares. Main
regressor: an export dummy (equation 17); entry and exit indicators interacted with post-period dummies
(equation 19); export share of sales in an extension. Controls: log labor and log capital, full year-by-industry
dummies. Output is deflated sales, materials are deflated with two-digit industry deflators, capital is book value
of fixed assets, labor is full-time-equivalent employment, and the wage bill is total employee cost (Appendix A).

### Statistical methods

GMM estimation of production-function parameters by industry (Cobb-Douglas and translog, value added and gross
output, with and without an endogenous productivity process). OLS of log markups on export status. Standard errors
for specifications I to V are described as coming from a nonlinear combination of parameter estimates; the
treatment of first-stage estimation error and of within-firm correlation is not described further.

### Reported effect sizes, confidence intervals and p-values

Effect sizes are reported as level differences with standard errors, and the percentage coefficient is given in
the text. No confidence intervals or p-values are printed; significance is marked against a 10% threshold in the
Table 3 notes.

### Missing data treatment

Not described beyond the employment-reporting restriction. Export destination data are noted as unavailable in
some years (footnote 40), so the destination analysis returns to a cross-sectional comparison.

### Stated limitations

The authors state that the export coefficient is a correlation, not a causal effect; that deflated sales stand in
for physical output (Section 6.1, citing Klette and Griliches), which they argue biases levels but not the
percentage premium under Cobb-Douglas; that markups for exporters average domestic and foreign markets
(Section 6.2); and that the data cannot distinguish quality, demand elasticity and income explanations for the
premium.

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Median markup, Hall method | 1.03 (s.e. 0.004), ratio | Table 2 | Common markup from a first-differenced Hall regression | A firm-level markup or one controlling for productivity |
| Median markup, Klette method | 1.12 (s.e. 0.020), ratio | Table 2 | Common markup by Klette's GMM procedure | Heterogeneity across firms |
| Median markups, specifications I to VI | 1.17, 1.10, 1.23, 1.28, 1.23, 1.26, ratio | Table 2 | Median firm markup under six production-function specifications | Precision (no standard errors shown for I to VI); the authors note the cross-firm s.d. is about 0.5 |
| Common markup, specification VII | 1.16 (s.e. 0.006), ratio | Table 2 | Hall-style markup estimated in levels with a productivity proxy | Firm-level variation |
| Exporter premium, Hall | 0.0155 (s.e. 0.010), markup level | Table 3 | Exporter difference in the common-markup framework | Any significant premium (not significant at 10%) |
| Exporter premium, Klette | 0.0500 (s.e. 0.090), markup level | Table 3 | Same, Klette framework | Any significant premium |
| Exporter premium, specification I | 0.1633 (s.e. 0.017), markup level | Table 3 | Average markup gap between exporters and domestic firms in the same industry-year, given labor and capital | Causality; whether the gap is price or cost |
| Exporter premium, specifications II, IV, V, VIII | 0.1608, 0.1304, 0.1829, 0.1263 (s.e. 0.013 to 0.017), level | Table 3 | Robustness of the gap to technology and estimation choices | Robustness to the choice of flexible input within each specification |
| Exporter premium, percent | about 0.078, log points | Section 5.2.1 text | The percentage markup gap | A separate standard error is not printed, although the text calls it very precise |
| Exporter premium controlling for productivity | 0.076 falling to 0.021, log points | Section 5.2.1 text | How much of the gap is associated with measured productivity | Whether the residual reflects quality, demand or prices |
| Export entry effect, specification I | 0.0467 (s.e. 0.0127), log points; 0.0939 (s.e. 0.0260), level | Table 4 and Table D.1 | Within-firm markup change after export entry | That entry causes the change; the counterfactual path |
| Export exit effect | −0.0166 (s.e. 0.0138), log points | Table D.1 | Within-firm markup change after exit | A significant decline (the estimate is about 1.2 standard errors) |
| Entry effect with export intensity | 0.097, coefficient on export share | Section 5.2.2 text | Larger markup gains for firms exporting more | A standard error is not printed in the text read |
| Western Europe destination premium | 0.045, markup level | Section 6.2.1 text | Higher markups for exporters to Western Europe | Precision (described as less precise) |
| Annual productivity growth | between 3 and 1.5 percent | Section 5.3 text | Productivity growth after correcting for markups | Uncertainty around either figure |

## Interpretation notes

- Under Cobb-Douglas the output elasticity is common within an industry, so the percentage premium in Table 3 is
  identified entirely by differences in the labor share of sales between exporters and domestic firms, net of the
  controls. The authors make this point themselves in Section 6.1. The production-function estimates matter for
  levels and for the translog specification, not for the Cobb-Douglas percentage premium.
- The specifications I to V that carry Table 3 use labor as the flexible input. Labor may be costlier to adjust
  than materials, a trade-off the authors acknowledge in footnote 28. The materials-based median (specification
  VI, 1.26) is close to the labor-based ones in Table 2, but no Table 3 premium is shown for specification VI.
- Bond, Hashemi, Kaplan and Zoch (2021) show that when output is deflated revenue, the estimated elasticity is a
  revenue elasticity, and the markup formula then returns a value near 1 under profit maximization. This bears on
  the levels in Table 2. It bears less directly on the Cobb-Douglas percentage premium, which does not depend on
  the elasticity, but it does bear on interpreting share differences as markup differences.
- Raval (2023) shows in manufacturing data from several countries that labor- and materials-based markups are
  negatively correlated and trend differently. If the same holds in Slovenia, the premium could depend on which
  input is used, and the paper reports the premium for one input only.
- The exporter share differs between Table 1 (2,335 of 4,906 firms exporting in 2000) and Appendix A (2,459 of
  6,250 firms in 2000). The difference likely reflects different sample definitions, but the paper does not
  reconcile them. This is a reporting issue, not a documented error.

## Unanswered questions

- How many firm-years enter each regression in Tables 3 and 4, and how many firms switch export status?
- Are standard errors clustered by firm, and do they account for the first-stage estimation of elasticities?
- What is the exporter premium when materials, rather than labor, is the flexible input?
- How sensitive are the results to trimming extreme markups or input shares?
- How do the published *AER* estimates compare with the working-paper figures used here?

## Items requiring expert verification

- Whether the published version's Tables 2 to 4 match the October 2010 working paper numbers extracted above.
- Whether the "nonlinear combination" standard errors in Table 3 correctly propagate first-stage uncertainty.
- Whether a proxy-method gross-output elasticity for materials is identified in these data, given the
  non-identification result of Gandhi, Navarro and Rivers (2020) for flexible inputs.
- Whether the replication files for the published article (if deposited with the AEA) reproduce the tables; they
  were not examined here and the Slovenian data are confidential.

## Relation to this repository

This repository does not reproduce the paper's results; the Slovenian firm data are confidential. It applies the
same formula and the same regression form to public US industry data. There, export-oriented industries show no
markup premium with either materials or payroll as the flexible input, and the two inputs give negatively
correlated markups across industries, in line with Raval's critique.
