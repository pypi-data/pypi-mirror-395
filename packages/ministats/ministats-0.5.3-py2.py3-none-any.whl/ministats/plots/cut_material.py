import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import warnings

from .regression import plot_partreg
from .regression import plot_pred_bands
from .regression import plot_projreg
from .regression import plot_reg



def fit_and_plot_reg(xs, ys, ax=None):
    """
    Fit a linear model `y ~ 1 + x` for the data provided in `xs` and `ys`,
    then plot the best-fitting line on top of a scatter plot `ys` vs. `xs`.
    Returns the linear regression result object and the plot axis.
    """
    xname = xs.name if hasattr(xs, "name") and xs.name is not None else "x"
    yname = ys.name if hasattr(ys, "name") and ys.name is not None else "y"
    xydf = pd.DataFrame({xname: xs, yname: ys})
    lmres = smf.ols(f"{yname} ~ 1 + {xname}", data=xydf).fit()
    ax = plot_reg(lmres, ax=ax)
    return lmres, ax



# Old linear model plotting functions (to be deprecated in next release)
################################################################################

def plot_lm_simple(xs, ys, ax=None, ci_mean=False, alpha_mean=0.1, lab_mean=True,
                   ci_obs=False, alpha_obs=0.1, lab_obs=True): 
    """
    Draw a scatter plot of the data `[xs,ys]`, a regression line,
    and optionally show confidence intervals for the model predcitions.
    If `ci_mean` is True: draw a (1-alpha_mean)-CI for the mean.
    If `ci_obs` is True: draw a (1-ci_obs)-CI for the predicted values.
    """
    warnings.warn("This function is replaced by plot_reg and plot_pred_bands", DeprecationWarning)
    ax = plt.gca() if ax is None else ax

    # Prepare the data
    xname = xs.name if hasattr(xs, "name") else "x"
    yname = ys.name if hasattr(ys, "name") else "y"
    data = pd.DataFrame({xname: xs, yname: ys})

    # Fit the linear model
    formula = f"{yname} ~ 1 + {xname}"
    lm = smf.ols(formula, data=data).fit()

    plot_reg(lm, ax=ax)
    plot_pred_bands(lm, ax=ax,
                    ci_mean=ci_mean, alpha_mean=alpha_mean, lab_mean=lab_mean,
                    ci_obs=ci_obs, alpha_obs=alpha_obs, lab_obs=lab_obs)
    return ax


def plot_lm_partial_old(lmfit, pred, others=None, ax=None):
    """
    Generate a partial regression plot from the best-fit line
    of the predictor `pred`, where the intercept is calculated
    from the average of the `other` predictors.
    """
    warnings.warn("This function is replaced by plot_projreg", DeprecationWarning)
    return plot_projreg(lmfit, pred, others=others, ax=ax)


def plot_lm_partial(lmfit, pred, others=None, ax=None):
    """
    Generate a partial regression plot from the model `lmfit`
    for the predictor `pred`, given the `other` predictors.
    We plot the residuals of `outcome ~ other` along the y-axis,
    and the residuals of the model `pred ~ other` on the x-axis.
    """
    warnings.warn("This function is replaced by plot_partreg", DeprecationWarning)
    return plot_partreg(lmfit, pred=pred, ax=ax)



# DEPRECATED SINCE `plot_partreg` subtracts all other vars
def plot_projreg_cat(lmfit, pred, others=None, color="C0", linestyle="solid", cats=None, ax=None):
    """
    Generate a partial regression plot from the best-fit line
    of the predictor `pred`, where the intercept is calculated
    from the average of the `other` predictors,
    including the value of categorical predictors `cats` in the slope.
    """
    ax = plt.gca() if ax is None else ax
    data = lmfit.model.data.orig_exog
    params = lmfit.params
    allpreds = set(data.columns) - {"Intercept"}
    allnoncatpreds = set([pred for pred in allpreds if "T." not in pred])
    assert pred in allnoncatpreds
    others = allnoncatpreds - {pred} if others is None else others
    intercept = params["Intercept"]
    for other in others:
        intercept += params[other]*data[other].mean() 
    for cat in cats:
        intercept += params[cat]
    slope = params[pred]
    print(pred, "intercept=", intercept, "slope=", slope)
    xs = np.linspace(data[pred].min(), data[pred].max())
    ys = intercept + slope*xs
    sns.lineplot(x=xs, y=ys, color=color, ax=ax, linestyle=linestyle)
    return ax
