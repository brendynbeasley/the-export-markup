"""Do export-oriented US industries carry higher markups? And do two inputs agree on the answer?

Replication: De Loecker and Warzynski's (2012) Table 3 regresses a producer's log markup on export
status with labor and capital controls and industry-by-year dummies. Firm-level US export data are
confidential, so the unit here is the industry: about 230 BEA detail manufacturing industries in
2007, 2012 and 2017, with export shares from the BEA input-output Use tables and markups built from
the NBER-CES data by src/markups.py. The paper's Table 4 (markups rise on export entry) becomes a
within-industry version with industry fixed effects.

Extension: Raval (2023) argues that if the production approach is right, any flexible input should
give the same markup. The script runs every test twice, once with materials and once with payroll as
the flexible input, and measures how far the two markups agree.

Run src/markups.py first; this reads results/markups_industry_year.csv and results/theta_cost_share.csv.

Outputs (all in results/):
  industry_panel.csv           BEA industry x benchmark year: export share, input shares, markups
  premium_cross_section.csv    Table 3 analog, every specification
  premium_within.csv           Table 4 analog (industry fixed effects)
  input_agreement.csv          how closely materials and payroll markups agree
  input_premium_gap.csv        test that both inputs give the same export premium
  named_industries.csv         the most and least export-oriented industries in 2017
  export_vs_markup.png         export share against sector-demeaned log markup, both inputs
  input_agreement.png          materials markup against payroll markup, sector-demeaned

Usage (from the repository root):
    python src/exporters.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

IO_FILE = RAW / "IOUse_Before_Redefinitions_PRO_2017_Detail.xlsx"   # BEA detail Use table, 2007/2012/2017 sheets
YEARS = [2007, 2012, 2017]
EXPORTS_COL = "F04000"        # BEA final-use code for exports of goods and services
COMP_ROW, INTERMEDIATE_ROW, OUTPUT_ROW = "V00100", "T005", "T008"   # compensation, total intermediate, industry output
# NAICS 2012 codes that the 2017 BEA concordance no longer lists (2017 NAICS merged them):
MANUAL_BEA = {"333911": "333914", "333913": "333914",
              "335221": "335220", "335222": "335220", "335224": "335220", "335228": "335220"}
DLW_PERCENT_PREMIUM = 0.078   # De Loecker & Warzynski, NBER WP 15198 (rev. Oct 2010), Sec. 5.2.1: "around 0.078"
DLW_ENTRY_EFFECT = 0.0467     # same paper, Table 4, specification I, percentage effect of export entry
NAMED_TOP, NAMED_SHARE, NAMED_BOTTOM = 8, 4, 6   # rows in the table of named industries
NAMED_MIN_OUTPUT = 10_000     # $ million; the share-ranked rows use only industries this large


def bea_concordance():
    """Map each NBER-CES (NAICS 2012) code to a BEA detail industry by longest NAICS prefix."""
    n = pd.read_excel(IO_FILE, sheet_name="NAICS Codes", header=None, engine="openpyxl")
    m = n[[3, 4, 6]].dropna(subset=[3]).astype(str)
    m.columns = ["bea", "bea_name", "naics"]
    m = m[m.bea.str.match(r"^3[1-3]")]
    prefixes = {}
    for _, r in m.iterrows():
        for tok in r.naics.split(","):
            tok = tok.strip()
            if "-" in tok:                    # "32192-9" means 32192 through 32199
                a, b = tok.split("-")
                for d in range(int(a[-1]), int(b) + 1):
                    prefixes[a[:-1] + str(d)] = r.bea
            else:
                prefixes[tok] = r.bea
    return prefixes, m.set_index("bea").bea_name


def to_bea(code, prefixes):
    if code in MANUAL_BEA:
        return MANUAL_BEA[code]
    for length in range(6, 2, -1):
        if code[:length] in prefixes:
            return prefixes[code[:length]]
    return None


def load_io():
    """Exports, commodity output, and BEA's own compensation and intermediate shares by industry."""
    frames = []
    for yr in YEARS:
        d = pd.read_excel(IO_FILE, sheet_name=str(yr), header=None, engine="openpyxl")
        codes = [str(c) for c in d.iloc[5].tolist()]
        rows = d.iloc[:, 0].astype(str).tolist()
        body = d.iloc[6:].copy()
        body.index = [str(c) for c in body.iloc[:, 0]]
        body.columns = codes
        comm = body[body.index.str.match(r"^3[1-3]")]
        exports = pd.to_numeric(comm[EXPORTS_COL], errors="coerce").fillna(0)
        output = pd.to_numeric(comm.iloc[:, -1], errors="coerce")        # total commodity output
        ind_cols = [c for c in codes if c[:2] in ("31", "32", "33")]
        ind = body.loc[[COMP_ROW, INTERMEDIATE_ROW, OUTPUT_ROW], ind_cols].apply(pd.to_numeric, errors="coerce").T
        ind.columns = ["bea_comp", "bea_intermediate", "bea_output"]
        f = pd.DataFrame({"exports": exports, "commodity_output": output}).join(ind, how="left")
        f["year"] = yr
        frames.append(f.rename_axis("bea").reset_index())
        assert COMP_ROW in rows and OUTPUT_ROW in rows
    io = pd.concat(frames, ignore_index=True)
    io["export_share"] = io.exports / io.commodity_output
    print(f"Loaded {IO_FILE.name}: {io.bea.nunique()} manufacturing commodities x {len(YEARS)} years")
    return io


def build_panel():
    mk = pd.read_csv(OUT / "markups_industry_year.csv", dtype={"naics": str, "sector": str})
    th = pd.read_csv(OUT / "theta_cost_share.csv", dtype={"sector": str})
    mk = mk[mk.year.isin(YEARS)].copy()
    prefixes, names = bea_concordance()
    mk["bea"] = [to_bea(c, prefixes) for c in mk.naics]
    unmatched = mk[mk.bea.isna()].naics.unique()
    print(f"  NBER-CES industries matched to a BEA industry: {mk.naics.nunique() - len(unmatched)} of "
          f"{mk.naics.nunique()} (unmatched: {list(unmatched)})")
    n_out = int(mk.outlier.sum())
    mk = mk[~mk.outlier & mk.bea.notna()]
    print(f"  dropped {n_out} NBER-CES industry-years flagged as input-share outliers by markups.py")

    agg = mk.groupby(["bea", "year"]).agg(
        sector=("sector", "first"), n_naics=("naics", "size"), vship=("vship", "sum"),
        matcost=("matcost", "sum"), pay=("pay", "sum"), emp=("emp", "sum"), cap=("cap", "sum")).reset_index()
    agg = agg.merge(th, on=["sector", "year"], how="left")
    agg["s_m"] = agg.matcost / agg.vship
    agg["s_l"] = agg.pay / agg.vship
    agg["mu_m"] = agg.theta_m / agg.s_m
    agg["mu_l"] = agg.theta_l / agg.s_l
    agg["ln_mu_m"] = np.log(agg.mu_m)
    agg["ln_mu_l"] = np.log(agg.mu_l)

    io = load_io()
    panel = agg.merge(io, on=["bea", "year"], how="inner")
    lost = set(agg.bea) - set(io.bea)
    print(f"  merged panel: {len(panel)} industry-years, {panel.bea.nunique()} BEA industries "
          f"({len(lost)} NBER-CES grouping(s) had no BEA commodity row: {sorted(lost)})")
    panel["bea_name"] = panel.bea.map(names)
    panel["high_export"] = (panel.export_share > panel.groupby("year").export_share.transform("median")).astype(int)
    panel["top_tercile"] = (panel.export_share > panel.groupby("year").export_share.transform(
        lambda s: s.quantile(2 / 3))).astype(int)
    panel["export_share_10"] = panel.export_share * 10    # coefficient = effect of 10 percentage points
    # BEA's own input shares, an independent check on the Census-based ones (compensation includes benefits)
    panel["bea_s_m"] = panel.bea_intermediate / panel.bea_output
    panel["bea_s_l"] = panel.bea_comp / panel.bea_output
    panel["ln_mu_m_bea"] = np.log(panel.theta_m / panel.bea_s_m)
    panel["ln_mu_l_bea"] = np.log(panel.theta_l / panel.bea_s_l)
    panel["sector_year"] = panel.sector + "_" + panel.year.astype(str)
    return panel


def fit(formula, data, weights=None):
    groups = pd.factorize(data.bea)[0]
    model = smf.wls(formula, data, weights=weights) if weights is not None else smf.ols(formula, data)
    return model.fit(cov_type="cluster", cov_kwds={"groups": groups})


def cross_section(panel):
    rows = []
    specs = [("materials", "ln_mu_m", "Census"), ("payroll", "ln_mu_l", "Census"),
             ("materials", "ln_mu_m_bea", "BEA"), ("payroll", "ln_mu_l_bea", "BEA")]
    variants = [("high_export", "all", None, panel), ("export_share_10", "all", None, panel),
                ("high_export", "weighted", "vship", panel), ("top_tercile", "all", None, panel),
                ("high_export", "2017 only", None, panel[panel.year == 2017])]
    for inp, dep, src in specs:
        for xvar, label, w, data in variants:
            if src == "BEA" and label != "all":
                continue
            data = data.dropna(subset=[dep])
            r = fit(f"{dep} ~ {xvar} + np.log(emp) + np.log(cap) + C(sector_year)", data,
                    weights=data[w] if w else None)
            b, se = r.params[xvar], r.bse[xvar]
            lo, hi = r.conf_int().loc[xvar]
            # level effect only for Census shares, where theta and the share measure the same costs
            base = np.exp(data.loc[data.high_export == 0, dep]).mean() if src == "Census" else np.nan
            rows.append({"input": inp, "share_source": src, "regressor": xvar, "sample": label,
                         "coef": b, "se": se, "ci_low": lo, "ci_high": hi, "p": r.pvalues[xvar],
                         "level_effect": (np.exp(b) - 1) * base, "low_export_mean_markup": base,
                         "n": int(r.nobs), "industries": data.bea.nunique(),
                         "dlw_0078_inside_ci": lo <= DLW_PERCENT_PREMIUM <= hi})
    out = pd.DataFrame(rows)
    out.round(6).to_csv(OUT / "premium_cross_section.csv", index=False)
    return out


def within(panel):
    rows = []
    for inp, dep in [("materials", "ln_mu_m"), ("payroll", "ln_mu_l"),
                     ("materials", "ln_mu_m_bea"), ("payroll", "ln_mu_l_bea")]:
        for xvar in ["export_share_10", "high_export"]:
            data = panel.dropna(subset=[dep])
            r = fit(f"{dep} ~ {xvar} + np.log(emp) + np.log(cap) + C(bea) + C(year)", data)
            lo, hi = r.conf_int().loc[xvar]
            rows.append({"input": inp, "share_source": "BEA" if dep.endswith("bea") else "Census",
                         "regressor": xvar, "coef": r.params[xvar], "se": r.bse[xvar],
                         "ci_low": lo, "ci_high": hi, "p": r.pvalues[xvar], "n": int(r.nobs),
                         "industries": data.bea.nunique(),
                         "switchers": int(data.groupby("bea").high_export.nunique().gt(1).sum())})
    out = pd.DataFrame(rows)
    out.round(6).to_csv(OUT / "premium_within.csv", index=False)
    return out


def agreement(panel):
    """Raval's test: under the paper's assumptions both inputs must give the same markup."""
    p = panel.copy()
    for v in ["ln_mu_m", "ln_mu_l"]:
        p[v + "_dm"] = p[v] - p.groupby("sector_year")[v].transform("mean")
    rows = []
    for yr, d in [("pooled", p)] + [(str(y), p[p.year == y]) for y in YEARS]:
        pear = stats.pearsonr(d.ln_mu_m_dm, d.ln_mu_l_dm)
        spear = stats.spearmanr(d.ln_mu_m_dm, d.ln_mu_l_dm)
        above_m = d.ln_mu_m_dm > 0
        above_l = d.ln_mu_l_dm > 0
        rows.append({"year": yr, "n": len(d), "pearson_within_sector": pear.statistic,
                     "pearson_p": pear.pvalue, "spearman_within_sector": spear.statistic,
                     "share_disagree_above_below_sector_mean": float((above_m != above_l).mean()),
                     "median_abs_gap_log_points": float((d.ln_mu_m - d.ln_mu_l).abs().median()),
                     "sd_ln_mu_m_within": d.ln_mu_m_dm.std(), "sd_ln_mu_l_within": d.ln_mu_l_dm.std()})
    # do the two inputs give the same export premium? stack them and test the difference
    long = pd.concat([p.assign(ln_mu=p.ln_mu_m, labor=0), p.assign(ln_mu=p.ln_mu_l, labor=1)])
    long["sy_input"] = long.sector_year + "_" + long.labor.astype(str)
    r = fit("ln_mu ~ high_export + high_export:labor + np.log(emp):C(labor) + np.log(cap):C(labor) "
            "+ C(sy_input)", long)
    out = pd.DataFrame(rows)
    out.round(6).to_csv(OUT / "input_agreement.csv", index=False)
    gap = pd.DataFrame([{"test": "high-export premium, payroll minus materials",
                         "coef": r.params["high_export:labor"], "se": r.bse["high_export:labor"],
                         "p": r.pvalues["high_export:labor"], "n": int(r.nobs)}])
    gap.round(6).to_csv(OUT / "input_premium_gap.csv", index=False)
    return out, gap


def named(panel):
    d = panel[panel.year == 2017].copy()
    d["rank_m_in_sector"] = d.groupby("sector").mu_m.rank(pct=True)
    d["rank_l_in_sector"] = d.groupby("sector").mu_l.rank(pct=True)
    big = d[d.commodity_output >= NAMED_MIN_OUTPUT]
    top = d.nlargest(NAMED_TOP, "exports").assign(group="largest exporters")
    share = big.nlargest(NAMED_SHARE, "export_share").assign(group="highest export share")
    share = share[~share.bea.isin(top.bea)]
    bottom = big.nsmallest(NAMED_BOTTOM, "export_share").assign(group="lowest export share")
    top = pd.concat([top, share])
    cols = ["group", "bea", "bea_name", "sector", "export_share", "exports", "commodity_output",
            "s_m", "s_l", "mu_m", "mu_l", "rank_m_in_sector", "rank_l_in_sector"]
    out = pd.concat([top, bottom])[cols]
    out.round(3).to_csv(OUT / "named_industries.csv", index=False)
    return out


def figure(panel):
    p = panel.copy()
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.3), sharex=True)
    for ax, (v, title, col) in zip(axes, [("ln_mu_m", "Materials markup", "#1f5f8b"),
                                          ("ln_mu_l", "Payroll markup", "#c0504d")]):
        y = p[v] - p.groupby("sector_year")[v].transform("mean")
        x = p.export_share * 100
        ax.scatter(x, y, s=10, alpha=0.45, color=col, edgecolor="none")
        b = np.polyfit(x, y, 1)
        xs = np.linspace(0, x.max(), 50)
        ax.plot(xs, np.polyval(b, xs), color="0.15", lw=1.4)
        ax.axhline(0, color="0.7", lw=0.7)
        ax.set_title(title, loc="left", fontsize=11)
        ax.set_xlabel("Exports as % of the industry's output")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Log markup minus its sector-year mean")
    fig.text(0.01, 0.01, "Each dot is a BEA manufacturing industry in 2007, 2012 or 2017. Sources: BEA Use "
             "tables; NBER-CES.", fontsize=8, color="0.35")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUT / "export_vs_markup.png", dpi=160)


def agreement_figure(panel):
    p = panel.copy()
    x = p.ln_mu_m - p.groupby("sector_year").ln_mu_m.transform("mean")
    y = p.ln_mu_l - p.groupby("sector_year").ln_mu_l.transform("mean")
    fig, ax = plt.subplots(figsize=(6.2, 5))
    ax.scatter(x, y, s=11, alpha=0.5, color="#5b6f7f", edgecolor="none")
    lim = 1.3
    ax.plot([-lim, lim], [-lim, lim], color="#c0504d", lw=1.2, ls="--", label="Where the two must agree")
    b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 50)
    ax.plot(xs, np.polyval(b, xs), color="0.15", lw=1.4, label="Fitted line through the data")
    ax.axhline(0, color="0.8", lw=0.7)
    ax.axvline(0, color="0.8", lw=0.7)
    ax.set_xlim(-0.7, 0.9)
    ax.set_ylim(-1.0, 1.3)
    ax.set_xlabel("Materials markup, log, relative to its sector-year mean")
    ax.set_ylabel("Payroll markup, log, relative to its sector-year mean")
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, f"{len(p)} BEA manufacturing industry-years, 2007, 2012, 2017. Sources: NBER-CES; BEA.",
             fontsize=8, color="0.35")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "input_agreement.png", dpi=160)


def main():
    panel = build_panel()
    keep = ["bea", "bea_name", "sector", "year", "n_naics", "vship", "matcost", "pay", "emp", "cap",
            "exports", "commodity_output", "export_share", "high_export", "theta_m", "theta_l",
            "s_m", "s_l", "mu_m", "mu_l", "bea_s_m", "bea_s_l"]
    panel[keep].round(5).to_csv(OUT / "industry_panel.csv", index=False)
    by_year = panel.groupby("year").export_share.describe()[["count", "mean", "50%", "max"]]
    print("Export share of output by year:\n" + by_year.round(3).to_string())

    cs = cross_section(panel)
    print("\nTable 3 analog (log markup on export status, sector-by-year dummies, clustered by industry):")
    print(cs[["input", "share_source", "regressor", "sample", "coef", "se", "p", "ci_low", "ci_high", "n"]]
          .round(3).to_string(index=False))
    wi = within(panel)
    print("\nTable 4 analog (industry and year fixed effects):")
    print(wi[["input", "share_source", "regressor", "coef", "se", "p", "n", "switchers"]].round(3).to_string(index=False))
    ag, gap = agreement(panel)
    print("\nDo materials and payroll agree?")
    print(ag.round(3).to_string(index=False))
    print(gap.round(3).to_string(index=False))
    nm = named(panel)
    print("\nNamed industries, 2017:")
    print(nm[["group", "bea_name", "exports", "export_share", "mu_m", "mu_l"]].round(2).to_string(index=False))
    figure(panel)
    agreement_figure(panel)
    print(f"\nWrote results to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
