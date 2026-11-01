"""Markups for every US manufacturing industry, 1958-2018, by the production approach.

De Loecker and Warzynski (2012) recover a producer's markup as the output elasticity of a
flexible input divided by that input's share of revenue:

    markup = theta_X / (spending on X / sales)

This script applies that formula to the NBER-CES Manufacturing Industry Database (364 six-digit
NAICS industries, 1958-2018) twice, once with materials and once with total payroll as the
flexible input. The output elasticities theta come from two
estimators run separately for each three-digit NAICS sector:

  1. cost shares (each input's share of total cost, with capital charged at a user cost),
     the sector-year median, as in Foster, Haltiwanger and Syverson (2008) and the cost-share
     variant of De Loecker, Eeckhout and Unger (2020); this is the estimator used downstream;
  2. the paper's own route, a Cobb-Douglas gross-output production function estimated with the
     Ackerberg-Caves-Frazer two-step proxy method using materials as the proxy. Its estimates
     are written out and compared, not used, for the reason printed when the script runs.

Outputs (all in results/):
  markups_industry_year.csv   one row per industry-year with input shares, thetas and markups
  theta_cost_share.csv        sector-year cost-share elasticities
  acf_estimates.csv           OLS and ACF production-function estimates by sector
  markup_trend.csv            sales-weighted manufacturing markup by year, by input
  median_markups.csv          median industry markup in each benchmark year (paper's Table 2 form)
  markup_trend.png            the two markup series over time

Usage (from the repository root):
    python src/markups.py
"""

import itertools
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

CES_FILE = RAW / "nberces5818v1_n2012.csv"   # NBER-CES Manufacturing Industry Database, 2021 release, NAICS 2012
GS10_FILE = RAW / "fred_GS10.csv"             # FRED: 10-year Treasury constant maturity, monthly
CPI_FILE = RAW / "fred_CPIAUCSL.csv"          # FRED: CPI for all urban consumers, monthly

LAST_CAPITAL_YEAR = 2016     # NBER-CES capital stock and investment deflator end in 2016; carried forward to 2017-18
BENCHMARK_YEARS = [2007, 2012, 2017]   # years with detailed BEA input-output export data (used in exporters.py)
ACF_LAST_YEAR = 2016         # production functions are estimated only on years with measured capital
POLY_DEGREE = 3              # degree of the first-stage polynomial in (l, k, m), as is standard for ACF
SHARE_TRIM = (0.01, 0.99)    # input-revenue shares outside these percentiles of their year are flagged, not used


def load_ces():
    """NBER-CES panel with real output, real inputs and nominal input shares."""
    ces = pd.read_csv(CES_FILE)
    n0 = len(ces)
    print(f"Loaded {CES_FILE.name}: {n0:,} industry-years, {ces.naics.nunique()} industries, "
          f"{ces.year.min()}-{ces.year.max()}")
    ces["naics"] = ces.naics.astype(str)
    ces["sector"] = ces.naics.str[:3]

    # Capital is measured through 2016. For 2017 and 2018 I use the 2016 stock and deflator,
    # which treats capital as fixed for two years (it is a slow-moving state variable).
    last = ces[ces.year == LAST_CAPITAL_YEAR].set_index("naics")[["cap", "piinv"]]
    late = ces.year > LAST_CAPITAL_YEAR
    for col in ["cap", "piinv"]:
        ces.loc[late, col] = ces.loc[late, "naics"].map(last[col]).values

    ok = (ces[["vship", "matcost", "pay", "emp", "cap", "piship", "pimat", "piinv"]].gt(0).all(axis=1))
    dropped = ces[~ok]
    print(f"  dropped {len(dropped)} industry-years with a missing or zero input, output or deflator "
          f"({dropped.naics.nunique()} industries: {sorted(dropped.naics.unique())}, years "
          f"{dropped.year.min()}-{dropped.year.max()})")
    ces = ces[ok].copy()

    ces["s_m"] = ces.matcost / ces.vship          # materials (incl. energy) share of sales
    ces["s_l"] = ces.pay / ces.vship              # payroll share of sales
    ces["y"] = np.log(ces.vship / ces.piship)     # real gross output
    ces["m"] = np.log(ces.matcost / ces.pimat)    # real materials
    ces["l"] = np.log(ces.emp)                    # employment (thousands)
    ces["k"] = np.log(ces.cap)                    # real capital stock
    print(f"  kept {len(ces):,} industry-years")
    return ces


def user_cost(ces):
    """Rental rate of capital by year: 10-year Treasury yield - CPI inflation + depreciation.

    Depreciation is the rate implied by the NBER-CES capital accounts themselves,
    delta_t = 1 - (K_t - I_t / p^I_t) / K_{t-1}, aggregated over all manufacturing.
    """
    gs10 = pd.read_csv(GS10_FILE, parse_dates=["observation_date"])
    cpi = pd.read_csv(CPI_FILE, parse_dates=["observation_date"])
    i = gs10.groupby(gs10.observation_date.dt.year).GS10.mean() / 100
    p = cpi.groupby(cpi.observation_date.dt.year).CPIAUCSL.mean()
    infl = p.pct_change()

    c = ces[ces.year <= LAST_CAPITAL_YEAR].sort_values(["naics", "year"]).copy()
    c["k_lag"] = c.groupby("naics").cap.shift(1)
    c["real_inv"] = c.invest / c.piinv
    agg = c.dropna(subset=["k_lag"]).groupby("year")[["cap", "real_inv", "k_lag"]].sum()
    delta = 1 - (agg.cap - agg.real_inv) / agg.k_lag
    delta = delta.reindex(range(ces.year.min(), ces.year.max() + 1))
    delta = delta.bfill().ffill()   # 1958 takes 1959; 2017-18 take 2016

    r = pd.DataFrame({"treasury_10y": i, "cpi_inflation": infl}).reindex(delta.index)
    r["depreciation"] = delta
    r["user_cost"] = r.treasury_10y - r.cpi_inflation + r.depreciation
    r.index.name = "year"
    print(f"  user cost of capital: mean {r.user_cost.mean():.3f}, range {r.user_cost.min():.3f} to "
          f"{r.user_cost.max():.3f}; implied depreciation averages {r.depreciation.mean():.3f}")
    return r


def cost_share_thetas(ces, rates):
    """Sector-year median cost shares of materials and payroll (constant returns assumed)."""
    c = ces.merge(rates[["user_cost"]], left_on="year", right_index=True)
    capital_cost = c.user_cost * c.cap * c.piinv
    total = c.matcost + c.pay + capital_cost
    c["cs_m"] = c.matcost / total
    c["cs_l"] = c.pay / total
    th = c.groupby(["sector", "year"])[["cs_m", "cs_l"]].median().rename(
        columns={"cs_m": "theta_m", "cs_l": "theta_l"}).reset_index()
    return th


def poly(X, deg):
    cols = [np.ones(len(X))]
    for d in range(1, deg + 1):
        for comb in itertools.combinations_with_replacement(range(X.shape[1]), d):
            cols.append(np.prod(X[:, list(comb)], axis=1))
    return np.column_stack(cols)


def acf_sector(g):
    """Ackerberg-Caves-Frazer estimate of y = bl*l + bk*k + bm*m + omega + e for one sector.

    Stage 1: y on a cubic in (l, k, m) and year dummies gives phi = expected output.
    Stage 2: omega(beta) = phi - bl*l - bk*k - bm*m follows omega_t = g(omega_{t-1}) + xi_t with g
    cubic; beta solves E[xi_t * (k_t, l_{t-1}, m_{t-1})] = 0 (exactly identified).
    """
    g = g.sort_values(["naics", "year"]).copy()
    yd = pd.get_dummies(g.year, drop_first=True).values.astype(float)
    Z = np.column_stack([poly(g[["l", "k", "m"]].values, POLY_DEGREE), yd])
    b, *_ = np.linalg.lstsq(Z, g.y.values, rcond=None)
    year_part = yd @ b[-yd.shape[1]:]
    g["phi"] = Z @ b - year_part
    g["y_net"] = g.y - year_part
    for v in ["phi", "l", "k", "m"]:
        g[v + "_1"] = g.groupby("naics")[v].shift(1)
    h = g.dropna(subset=["phi_1"])
    X = np.column_stack([np.ones(len(h)), h[["l", "k", "m"]].values])
    ols = np.linalg.lstsq(X, h.y_net.values, rcond=None)[0][1:]

    def crit(beta):
        bl, bk, bm = beta
        w = h.phi - bl * h.l - bk * h.k - bm * h.m
        w1 = h.phi_1 - bl * h.l_1 - bk * h.k_1 - bm * h.m_1
        P = np.column_stack([np.ones(len(h)), w1, w1 ** 2, w1 ** 3])
        xi = w - P @ np.linalg.lstsq(P, w, rcond=None)[0]
        mom = np.column_stack([h.k, h.l_1, h.m_1]).T @ xi / len(h)
        return float(mom @ mom)

    best = None
    for start in [ols, [0.3, 0.1, 0.6], [0.2, 0.2, 0.5]]:
        res = minimize(crit, start, method="Nelder-Mead",
                       options={"xatol": 1e-7, "fatol": 1e-14, "maxiter": 5000})
        if best is None or res.fun < best.fun:
            best = res
    return ols, best.x, best.fun, len(h)


def run_acf(ces):
    rows = []
    sample = ces[ces.year <= ACF_LAST_YEAR]
    for sector, g in sample.groupby("sector"):
        ols, acf, fun, n = acf_sector(g)
        rows.append({"sector": sector, "industries": g.naics.nunique(), "obs": n,
                     "ols_l": ols[0], "ols_k": ols[1], "ols_m": ols[2],
                     "acf_l": acf[0], "acf_k": acf[1], "acf_m": acf[2], "acf_criterion": fun,
                     "median_cost_share_m": np.nan, "median_cost_share_l": np.nan})
    out = pd.DataFrame(rows)
    implausible = ((out[["acf_l", "acf_k", "acf_m"]] < 0) | (out[["acf_l", "acf_k", "acf_m"]] > 1)).any(axis=1)
    out["acf_outside_0_1"] = implausible
    print(f"  ACF (materials proxy, as in the paper): {implausible.sum()} of {len(out)} sectors return an "
          f"elasticity below 0 or above 1; ACF materials elasticity ranges {out.acf_m.min():.2f} to "
          f"{out.acf_m.max():.2f}")
    return out


def main():
    OUT.mkdir(exist_ok=True)
    ces = load_ces()
    rates = user_cost(ces)
    th = cost_share_thetas(ces, rates)
    ces = ces.merge(th, on=["sector", "year"], how="left")

    acf = run_acf(ces)
    med = th[th.year <= ACF_LAST_YEAR].groupby("sector")[["theta_m", "theta_l"]].median()
    acf["median_cost_share_m"] = acf.sector.map(med.theta_m)
    acf["median_cost_share_l"] = acf.sector.map(med.theta_l)
    acf.round(4).to_csv(OUT / "acf_estimates.csv", index=False)
    print("  the downstream markups use cost-share elasticities; the ACF estimates are kept in "
          "acf_estimates.csv for comparison")

    ces["mu_m"] = ces.theta_m / ces.s_m
    ces["mu_l"] = ces.theta_l / ces.s_l
    lo_m, hi_m = ces.groupby("year").s_m.transform(lambda s: s.quantile(SHARE_TRIM[0])), \
        ces.groupby("year").s_m.transform(lambda s: s.quantile(SHARE_TRIM[1]))
    lo_l, hi_l = ces.groupby("year").s_l.transform(lambda s: s.quantile(SHARE_TRIM[0])), \
        ces.groupby("year").s_l.transform(lambda s: s.quantile(SHARE_TRIM[1]))
    ces["outlier"] = ~(ces.s_m.between(lo_m, hi_m) & ces.s_l.between(lo_l, hi_l))
    print(f"  flagged {int(ces.outlier.sum())} industry-years with an input share in the top or bottom 1% "
          f"of its year; they are excluded from the trend and medians")

    keep = ["naics", "sector", "year", "vship", "matcost", "pay", "emp", "cap", "piship",
            "s_m", "s_l", "theta_m", "theta_l", "mu_m", "mu_l", "outlier"]
    ces[keep].round(5).to_csv(OUT / "markups_industry_year.csv", index=False)
    th.round(4).to_csv(OUT / "theta_cost_share.csv", index=False)
    rates.round(4).to_csv(OUT / "user_cost.csv")

    clean = ces[~ces.outlier]
    trend = clean.groupby("year").apply(lambda d: pd.Series({
        "industries": len(d),
        "markup_materials": np.average(d.mu_m, weights=d.vship),
        "markup_labor": np.average(d.mu_l, weights=d.vship),
        "materials_share_of_sales": d.matcost.sum() / d.vship.sum(),
        "payroll_share_of_sales": d.pay.sum() / d.vship.sum(),
        "theta_m_mean": np.average(d.theta_m, weights=d.vship),
        "theta_l_mean": np.average(d.theta_l, weights=d.vship),
    }), include_groups=False).reset_index()
    trend.round(4).to_csv(OUT / "markup_trend.csv", index=False)

    medians = clean[clean.year.isin(BENCHMARK_YEARS + [1958, 1987, 1997])].groupby("year").agg(
        industries=("naics", "size"), median_markup_materials=("mu_m", "median"),
        median_markup_labor=("mu_l", "median"), sd_markup_materials=("mu_m", "std"),
        sd_markup_labor=("mu_l", "std")).reset_index()
    medians.round(3).to_csv(OUT / "median_markups.csv", index=False)
    print(medians.round(3).to_string(index=False))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(trend.year, trend.markup_materials, color="#1f5f8b", lw=2.2, label="Materials as the flexible input")
    ax.plot(trend.year, trend.markup_labor, color="#c0504d", lw=2.2, label="Payroll as the flexible input")
    ax.axhline(1, color="0.6", lw=0.8)
    ax.set_ylabel("Sales-weighted markup (price / marginal cost)")
    ax.set_title("Same factories, same years, two answers", loc="left", fontsize=12)
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(0, -0.13, "Source: NBER-CES Manufacturing Industry Database, 364 industries; cost-share elasticities "
            "by sector and year.", transform=ax.transAxes, fontsize=8, color="0.35")
    fig.tight_layout()
    fig.savefig(OUT / "markup_trend.png", dpi=160)
    first, last = trend.iloc[0], trend.iloc[-1]
    print(f"  manufacturing markup {int(first.year)} -> {int(last.year)}: materials "
          f"{first.markup_materials:.3f} -> {last.markup_materials:.3f}, payroll "
          f"{first.markup_labor:.3f} -> {last.markup_labor:.3f}")
    print(f"Wrote results to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
