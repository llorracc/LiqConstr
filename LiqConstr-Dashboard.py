# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     formats: ipynb,py:light
#     notebook_metadata_filter: all
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.6.9
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: true
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: false
#     toc_position: {}
#     toc_section_display: true
#     toc_window_display: false
#   varInspector:
#     cols:
#       lenName: 16
#       lenType: 16
#       lenVar: 40
#     kernels_config:
#       python:
#         delete_cmd_postfix: ''
#         delete_cmd_prefix: 'del '
#         library: var_list.py
#         varRefreshCmd: print(var_dic_list())
#       r:
#         delete_cmd_postfix: ') '
#         delete_cmd_prefix: rm(
#         library: var_list.r
#         varRefreshCmd: 'cat(var_dic_list()) '
#     types_to_exclude:
#     - module
#     - function
#     - builtin_function_or_method
#     - instance
#     - _Feature
#     window_display: false
# ---

# # Liquidity Constraints and Precautionary Saving
#
# This notebook generates the figures for the paper
# [Liquidity Constraints and Precautionary Saving](https://econ.jhu.edu/people/ccarroll/papers/LiqConstr)
# by Carroll, Holm, and Kimball.

# + {"code_folding": []}
# Some setup stuff
import Dashboard.dashboard_widget as liqConstr
# The warnings package allows us to ignore some harmless but alarming warning messages
from ipywidgets import interactive
import warnings
warnings.filterwarnings("ignore")
# -
# ## Counterclockwise Concavification
#
# The Figure illustrates two examples of counterclockwise concavifications: the introduction of a constraint and the
# introduction of a risk. In both cases, we start from the situation with no risk or constraints (solid line).
# The introduction of a constraint is a counterclockwise concavification around a kink point $w^{\#}$.
# Below $w^{\#}$, consumption is lower and the MPC is greater.
# The introduction of a risk also generates a counterclockwise concavification of the original consumption function,
# but this time around $\infty$. For all $w < \infty$, consumption is lower, the MPC is higher,
# and the consumption function is strictly more concave.

# + {"code_folding": []}
interactive(liqConstr.make_concavification_figure,
           in_BoroCnstArt=liqConstr.BoroCnstArt_widget[0],
           in_UnempProb=liqConstr.UnempProb_widget)


# -

# **Notes:** The solid line shows the linear consumption function in the case with no constraints and no risks.
# The two dashed line show the consumption function when we introduce a constraint and a risk, respectively.
# The introduction of a constraint is a counterclockwise concavification of the solid consumption function around
# $w^{\#}$, while the introduction of a risk is a counterclockwise concavification around $\infty$.

# ## How a current constraint can hide a future kink
#
# The original $\mathcal{T}$ contains only a single constraint, at the end of period $t+1$, inducing a kink point at
# $\omega_{t,1}$ in the consumption rule $c_{t,1}$. The expanded set of constraints, $\hat{\mathcal{T}}$, adds one
# constraint at period $t+2$. $\hat{\mathcal{T}}$ induces two kink points in the updated consumption rule $\hat{c}_{t,2}$,
# at $\hat{\omega}_{t,1}$ and $\hat{\omega}_{t,2}$.  It is true that imposition of the new constraint causes consumption to
# be lower than before at every level of wealth below $\hat{\omega}_{t,1}$.  However, this does not imply higher prudence
# of the value function at every $w <\hat{\omega}_{t,1}$.  In particular, note that the original consumption function is
# strictly concave at $w = \omega_{t,1}$, while the new consumption function is linear at $\omega_{t,1}$, so prudence can
# be greater before than after imposition of the new constraint at this particular level of wealth.
#
# The intuition is simple: At levels of initial wealth below $\hat{\omega}_{t,1}$, the consumer had been planning to end
# period $t+2$ with negative wealth. With the new constraint, the old plan of ending up with negative wealth is no longer
# feasible and the consumer will save more for any given level of current wealth below $\hat{\omega}_{t,1}$, including
# $\omega_{t,1}$. But the reason $\omega_{t,1}$ was a kink point in the initial situation was that it was the level of
# wealth where consumption would have been equal to wealth in period $t+1$. Now, because of the extra savings induced by
# the constraint in $t+2$, the larger savings induced by wealth $\omega_{t,1}$ implies that the period $t+1$ constraint
# will no longer bind for a consumer who begins period $t$ with wealth $\omega_{t,1}$. In other words, at wealth
# $\omega_{t,1}$ the extra savings induced by the new constraint moves the original constraint and prevents it from being
# relevant any more at the original $\omega_{t,1}$.
#
# Notice, however, that all constraints that existed in $\mathcal{T}$ will remain relevant at *some* level of
# wealth under $\hat{\mathcal{T}}$ even after the new constraint is imposed - they just induce kink points at different
# levels of wealth than before, e.g. the first constraint causes a kink at $\hat{\omega}_{t,2}$ rather than at $\omega_{t,1}$.

# + {"code_folding": []}
interactive(liqConstr.make_future_kink,
           in_BoroCnstArt=liqConstr.BoroCnstArt_widget[1])
# -

# **Notes:** $c_{t,1}$ is the original consumption function with one constraint that induces a kink point at $\omega_{t,1}$.
# $\hat{c}_{t,2}$ is the modified consumption function in where we have introduced one new constraint.
# The two constraints affect $\hat{c}_{t,2}$ through two kink points: $\hat{\omega}_{t,1}$ and $\hat{\omega}_{t,2}$.
# Since we introduced the new constraint at a later point in time than the current existing constraint,
# the future constraint affects the position of the kink induced by the current constraint and the modified consumption
# function $\hat{c}_{t,2}$ is not a counterclockwise concavification of ${c}_{t,1}$.

#
# ## Consumption function with and without a constraint and a risk
#
# To illustrate the result of Theorem 2 in the paper, The figure shows an
# example of optimal consumption rules in period $t$ under different combinations of an immediate risk (realized at the
# beginning of period $t+1$) and a future constraint (applying at the end of period $t+1$).
# The thinner loci reflect behavior of consumers who face the future constraint, and the dashed loci reflect behavior of
# consumers who face the immediate risk. For levels of wealth above $\omega_{t,1}$ where the future constraint stops
# impinging on current behavior for perfect foresight consumers, behavior of the constrained and unconstrained perfect
# foresight consumers is the same. Similarly, $\tilde{c}_{t,1}(w_{t}) = \tilde{c}_{t,0}(w_{t})$ for levels of wealth above
# ${\bar{\omega}}_{t,1}$ beyond which the probability of the future constraint binding is zero. For both constrained and
# unconstrained consumers, the introduction of the risk reduces the level of consumption (the dashed loci are below their
# solid counterparts). The significance of Theorem 2 in the paper in this context is that for levels of
# wealth below ${\bar{\omega}}_{t,1}$, the vertical distance between the solid and the dashed loci is greater for the
# constrained (thin line) than for the unconstrained (thick line) consumers, because of the interaction between the
# liquidity constraint and the precautionary motive.

# + {"code_folding": []}
interactive(liqConstr.make_cons_func,
           in_BoroCnstArt=liqConstr.BoroCnstArt_widget[2],
            in_TranShkStd=liqConstr.TranShkStd_widget)

# -

# **Notes:** $c_{t,0}$ is the consumption function with no constraint and no risk, $\tilde{c}_{t,0}$ is the consumption
# function with no constraint and a risk that is realized at the beginning of period $t+1$, $c_{t,1}$ is the consumption
# function with one constraint in period $t+1$ and no risk, and $\tilde{c}_{t,1}$ is the consumption function with one
# constraint in period $t+1$ and a risk that is realized at the beginning of period $t+1$. The figure illustrates that
# the vertical distance between $c_{t,1}$ and $\tilde{c}_{t,1}$ is always greater than the vertical distance between
# $c_{t,0}$ and $\tilde{c}_{t,0}$ for $w < \bar{\omega}_{t,1}$.
