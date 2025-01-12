import argparse
import warnings
from pathlib import Path
<<<<<<< HEAD

import numpy as np
=======
from shutil import copyfile

import numpy as np
import pandas as pd
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
from src import utils as cutil
from src.models import epi

PLOT_DIR = cutil.RESULTS / "figures" / "appendix" / "sims"


def make_coeff_factorplot(
    ds,
    pop,
    LHS_var,
    title="",
    xlabel="",
    n_bins=40,
    xlim=None,
    hist_kwargs={"edgecolor": "none"},
    fig_label=None,
    **facet_kwargs,
):
    """Make a factorplot of histograms of regression-derived estimates vs. true values for
    simulated outbreaks.
    
    Parameters
    ----------
    ds : :class:`xarray.Dataset`
        Dataset containing regression results across samples. Must contain the dims
        `pop`, ``LHS`, and any dims specified in `facet_kwargs`
    pop : numeric
        Population to make this plot for. Must be one of the values of `pop` in `ds`.
    LHS_var : str
        Plot results of regressions using this value as the left-hand-side variable.
        Must be one of the values of `pop` in `ds`.
    title : str, optional
        Suptitle for this plot
    xlabel : str, optional
        Labels of x axes.
    n_bins : int
        Number of bins in histograms
    xlim : float, optional
        The left or right-most limit of the x axis, depending on whether the true value
        is positive (for the no-policy growth rate) or negative (for policy effects).
        The other axis limit is always 0. If None (default), use 2x the true value.
    hist_kwargs : dict, optional
        Pass to :func:`matplotlib.pyplot.hist`
    fig_label : str, optional
        Label for this figure panel if going in paper (e.g. "a" or "b")
    facet_kwargs
        Passed to :class:`xarray.plot.FacetGrid`
        
    Returns
    -------
    g : :class:`xarray.plot.FacetGrid`
        The output factorplot object
    """
    this_true_val = ds.coefficient_true.item()
    if this_true_val > 0:
        xmin = 0
        if xlim is None:
            xmax = this_true_val * 2
        else:
            xmax = xlim
        text_ha, text_x, text_y, leg_x, leg_y, leg_text = (
            "left",
            0.03,
            0.05,
            0.03,
            0.55,
            "Mean estimate",
        )
    elif this_true_val < 0:
        if xlim is None:
            xmin = this_true_val * 2
        else:
            xmin = -xlim
        xmax = 0
        text_ha, text_x, text_y, leg_x, leg_y, leg_text = (
            "right",
            0.97,
            0.55,
            0.03,
            0.5,
            "Mean\nestimate",
        )

    g = xr.plot.FacetGrid(ds.sel(LHS=LHS_var, pop=pop), sharey="row", **facet_kwargs)
    g.map(lambda x: plt.axvline(x, color="k", label="Truth"), "coefficient_true")
    for ax in g.axes.flat:
        ax.set_xlim(xmin, xmax)

    def nowarn_hist(data, *args, xmin=None, xmax=None, **kwargs):
        binmin = max(xmin, np.nanmin(data))
        binmax = min(xmax, np.nanmax(data))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return plt.hist(
                data, *args, bins=np.linspace(binmin, binmax, n_bins), **kwargs
            )

    g.map(nowarn_hist, "coefficient", xmin=xmin, xmax=xmax, **hist_kwargs)
    g.map(
        lambda x: plt.axvline(
            np.nanmean(x), color="tab:grey", linestyle="dashed", label=leg_text
        ),
        "coefficient",
    )
    g.map(
        lambda x, z: plt.text(
            text_x,
            text_y,
            f"$S_{{min}}$: {x.min().item():.2f}\nBias: {(np.nanmean(z)-this_true_val) / this_true_val:.1%}",
            horizontalalignment=text_ha,
            verticalalignment="bottom",
            transform=plt.gca().transAxes,
        ),
        "S_min",
        "coefficient",
    )
    g.axes.flat[0].legend(loc=(leg_x, leg_y))
    g.set_xlabels(xlabel, fontweight="bold")
    g.set_titles("$\{coord} = {value}$")
    [t.set_text(t.get_text().replace("inf", "\infty")) for t in g.row_labels]
    g.map(lambda: plt.yticks([]))
    if fig_label is not None:
        g.fig.text(
            0.03, 0.97, fig_label, fontsize=7, fontweight="bold", va="top", ha="left"
        )
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle(title, va="bottom", y=0.95)
    sns.despine(g.fig, left=True)
    return g


def make_all_coeff_factorplots(
<<<<<<< HEAD
    dir_in, plot_dir=None, LHS_vars=[], save_source_data=None
=======
    dir_in, plot_dir=None, LHS_vars=[], save_source_data=None, save_paper_figs=False
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51
):
    """Create factorplots of estimated coefficients derived from simulated outbreaks.
    Must have previously created the regression results, which is currently done
    by running the ``iwb-simulator.ipynb`` notebook.
    
    Parameters
    ----------
    dir_in : str
        The directory containing the regression results. Must contain subdirectories
        ``SIR`` and ``SEIR``.
    plot_dir : str, optional
        The directory where you would like to store plots. If None, do not save.
    LHS_vars : list of str
        Make plots for regressions run with these values as the left-hand-side. Using
        the variable names of an SEIR model (e.g. `I` is active infectious cases, and `IR`
        is active infectious cases + recovered cases)
    save_source_data : str or :class:`pathlib.Path`
        If not None, output the source data for these factorplots to this path. Only the
        `IR` and `I` LHS vars are output (to match what is included in the Extended 
        Data)
<<<<<<< HEAD
=======
    save_paper_figs : bool
        If True, save the subset of output figures used in the Extended Data of the 
        manuscript to ``results/figures/appendix/FigED[8,9]`` and the source data to 
        ``results/source_data/ExtendedDataFigure89.csv``.
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51
    """

    coeffs = epi.load_and_combine_reg_results(
        dir_in, cols_to_keep=["effect", "Intercept", "S_min", "rmse"]
    )
    coeffs = epi.calc_cum_effects(coeffs)

<<<<<<< HEAD
=======
    if plot_dir is not None:
        plot_dir = Path(plot_dir)
        plot_dir.mkdir(exist_ok=True)

>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51
    print("Creating factorplots...")
    ## loop over population
    facet_kwargs = dict(row="sigma", col="gamma")
    hist_kwargs = {"edgecolor": "none"}
    for px, p in enumerate(coeffs.pop.values):
        print(f"...Population {px+1}/{len(coeffs.pop.values)}")
        ## loop over LHS vars
        for LHS in ["I", "IR"]:
            LHS_dict = {"I": "Active\ Cases", "IR": "Cumulative\ Cases"}
            if p == 1e8 and LHS == "I":
                fig_label = "a"
            elif p == 1e5 and LHS == "IR":
                fig_label = "b"
            else:
                fig_label = None
            title_suffix = (
                f"(pop. size: {p:,}; dep. variable: $\Delta log({LHS_dict[LHS]})$)"
            )

            # loop over
            for var in coeffs.policy.values:
                if var == "Intercept":
                    title = (
                        "$\\bf{Infection\ growth\ rate\ without\ policy}$\n"
                        + title_suffix
                    )
                    xlabel = "Estimated daily growth rate"
                    color = cutil.COLORS["no_policy_growth_rate"]
                elif var == "cum_effect":
                    title = (
                        "$\\bf{Effect\ of\ all\ policies\ combined}$\n" + title_suffix
                    )
                    xlabel = "Estimated effect on daily growth rate"
                    color = cutil.COLORS["effect"]
                else:
                    policy_num = int(var[1:])
                    title = f"Effect of policy {policy_num}"
                    xlabel = "Estimated effect on daily growth rate"
                    color = cutil.COLORS["effect"]

                # make factorplot
                g = make_coeff_factorplot(
                    coeffs.sel(policy=var),
                    p,
                    LHS,
                    title=title,
                    figsize=(6.5, 3.25),
                    fig_label=fig_label,
                    xlabel=xlabel,
                    xlim=0.6,
                    hist_kwargs={**hist_kwargs, "facecolor": color, "alpha": 0.8},
                    **facet_kwargs,
                )

                if plot_dir is not None:
<<<<<<< HEAD
                    plot_dir = Path(plot_dir)
                    plot_dir.mkdir(exist_ok=True)
=======
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51
                    for suffix in ["pdf", "png"]:
                        g.fig.savefig(
                            plot_dir / f"{var}_pop_{p}_LHS_{LHS}.{suffix}",
                            dpi=300,
                            tight_layout=True,
                            bbox_inches="tight",
                        )
                    plt.clf()

<<<<<<< HEAD
    if save_source_data is not None:
        save_source_data = Path(save_source_data)
        coeffs.sel(LHS=["I", "IR"], policy=["Intercept", "cum_effect"])[
            ["S_min", "coefficient", "coefficient_true"]
        ].to_dataframe().to_csv(save_source_data, float_format="%.5f", index=True)
=======
    if save_paper_figs:
        source_path = Path(cutil.RESULTS / "source_data" / "ExtendedDataFigure89.csv")
        out_base = Path(cutil.RESULTS / "figures" / "appendix")

        # source data
        coeff_lim = coeffs.sel(policy=["Intercept", "cum_effect"])[
            ["S_min", "coefficient", "coefficient_true"]
        ]
        df_a = coeff_lim.sel(LHS="I", pop=1e8).to_dataframe()
        df_b = coeff_lim.sel(LHS="IR", pop=1e5).to_dataframe()
        pd.concat((df_a, df_b)).to_csv(source_path, float_format="%.5f", index=True)

        # figures
        for t in (("Intercept", "FigED8"), ("cum_effect", "FigED9")):
            out_dir = out_base / t[1]
            out_dir.mkdir(parents=True, exist_ok=True)
            copyfile(
                plot_dir / f"{t[0]}_pop_100000000_LHS_I.pdf", out_dir / f"{t[1]}_a.pdf"
            )
            copyfile(
                plot_dir / f"{t[0]}_pop_100000_LHS_IR.pdf", out_dir / f"{t[1]}_b.pdf"
            )

>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot estimated coefficients from simulations."
    )
    parser.add_argument(
        "dir_in",
        help="filepath to results of regressions from simulated outbreaks",
        type=lambda x: Path(x),
    )
    parser.add_argument(
        "dir_out",
        help="directory to store results",
        nargs="?",
        type=lambda x: Path(x),
        default=None,
    )
    parser.add_argument(
        "--LHS",
        help="Plot regressions with these left-hand-side variables",
        nargs="*",
        default=["I", "IR"],
    )
    parser.add_argument(
<<<<<<< HEAD
        "--source-data",
        help="Path to save source data",
        type=lambda x: Path(x),
        default=None,
    )
=======
        "--paper-figs",
        help=(
            "Save the relevant Extended Data Figures to results/figures/appendix/EDFigX"
            " and the source data to results/source_data/ExtendedDataFigure89.csv"
        ),
        action="store_true",
    )

>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51
    args = parser.parse_args()

    sns.set(context="paper", style="ticks", font_scale=0.65)
    mpl.rc("figure", max_open_warning=0)

    make_all_coeff_factorplots(
        args.dir_in,
        plot_dir=args.dir_out,
        LHS_vars=args.LHS,
<<<<<<< HEAD
        save_source_data=args.source_data,
=======
        save_paper_figs=args.paper_figs,
>>>>>>> 3f7be048afb0e50d926b6a53b6ea7eb551308b51
    )
