import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np

# In order to use LaTeX to manage all text layout in our figures, we import rc settings from matplotlib.
from matplotlib import rc

rc("text", usetex=True)
plt.rc("text", usetex=True)
plt.rc("font", family="serif")

# Now we can start making the figures.  We start by importing the relevant subclass of AgentType into our workspace.

# Load consumer type from HARK
from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType

# Define all parameters of three type of settings that we need to produce the three figures in the paper.

# Common parameters for all models (the initialized lifecycle perfect foresight type with no borrowing constraint)

# load default parameteres from the lifecycle model in the HARK toolbox
from HARK.ConsumptionSaving.ConsIndShockModel import init_lifecycle

# remove all risk and growth factors, borrowing constraints, and set the solver to always use the cubic tool
init_lifecycle["PermGroFac"] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
init_lifecycle["LivPrb"] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
init_lifecycle["DiscFac"] = 1 / 1.03
init_lifecycle["T_retire"] = 11
init_lifecycle["UnempPrb"] = 0
init_lifecycle["TranShkStd"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
init_lifecycle["PermShkStd"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
init_lifecycle["BoroCnstArt"] = [
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
]
init_lifecycle["CubicBool"] = False

# add the second type of lifecycle agent with unemployment risk
init_lifecycle_risk1 = dict(init_lifecycle)
init_lifecycle_risk1["IncUnemp"] = 0.1955

# the lifecycle type with only one-period transitory risk
init_lifecycle_risk2 = dict(init_lifecycle)

# Define a slider for the artificial borrowing constraint

# Define default values for three different borrowind constraint widgets
BoroCnstArt_mat = np.array([[-1.7, -1, 0], [-0.01, 0.02, 0.09], [-7, -6, -5]])

BoroCnstArt_widget = [
    widgets.FloatSlider(
        min=row[0],
        max=row[2],
        step=0.001,
        value=row[1],  # Default value
        continuous_update=True,
        readout_format=".3f",
        description="a̲",
    )
    for row in BoroCnstArt_mat
]

# Define a slider for the unemployment probability

UnempProb = 0.05  # Default value

UnempProb_widget = widgets.FloatSlider(
    min=0,
    max=0.2,
    step=0.001,
    value=UnempProb,  # Default value UnempProb = 0.05
    continuous_update=True,
    readout_format=".3f",
    description="℧",
)

# Define a slider for the one-period transitory risk

TranShkStd = 0.5

TranShkStd_widget = widgets.FloatSlider(
    min=0,
    max=2,
    step=0.001,
    value=TranShkStd,  # Default value TranShkStd = 0.5
    continuous_update=True,
    readout_format=".3f",
    description="σ_θ",
)


def make_concavification_figure(in_BoroCnstArt, in_UnempProb):
    """
    This figure illustrates how both risks and constraints are examples of counterclockwise concavifications.
    It plots three lines: the linear consumption function of a perfect foresight consumer, the kinked consumption
    function of a consumer who faces a constraint, and the curved consumption function of a consumer that faces risk.
    """

    # load the three agents: unconstrained perfect foresight, constrained perfect foresight, unconstrained with risk

    CCC_unconstr = IndShockConsumerType(**init_lifecycle)
    CCC_unconstr.delFromTimeInv("BoroCnstArt")
    CCC_unconstr.addToTimeVary("BoroCnstArt")
    CCC_unconstr.solve()
    CCC_unconstr.unpack("cFunc")

    CCC_constraint = IndShockConsumerType(**init_lifecycle)
    CCC_constraint.delFromTimeInv("BoroCnstArt")
    CCC_constraint.addToTimeVary("BoroCnstArt")
    CCC_constraint.BoroCnstArt = [
        None,
        in_BoroCnstArt,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    CCC_constraint.solve()
    CCC_constraint.unpack("cFunc")

    init_lifecycle_risk1["UnempPrb"] = in_UnempProb

    CCC_risk = IndShockConsumerType(**init_lifecycle_risk1)
    CCC_risk.delFromTimeInv("BoroCnstArt")
    CCC_risk.addToTimeVary("BoroCnstArt")
    CCC_risk.solve()
    CCC_risk.unpack("cFunc")

    x = np.linspace(-1, 1, 500, endpoint=True)
    y = CCC_unconstr.cFunc[0](x)
    y2 = CCC_constraint.cFunc[0](x)
    y3 = CCC_risk.cFunc[0](x)

    where_close = np.isclose(y, y2, atol=1e-05)

    # Display the figure
    # print('Figure 1: Counterclockwise Concavifications')
    f = plt.figure()
    plt.plot(x, y, color="black")
    plt.plot(x, y2, color="green", label="Constraint", linestyle="--")
    plt.plot(x, y3, color="red", label="Risk", linestyle="--")
    plt.tick_params(
        labelbottom=False,
        labelleft=False,
        left="off",
        right="off",
        bottom="off",
        top="off",
    )

    if np.any(where_close):
        x0 = x[where_close][0]
        y0 = y[where_close][0]
        plt.text(x0 - 0.02, 0.42, "$w^{\#}$", fontsize=14)
        plt.plot([x0, x0], [0.45, y0], color="black", linestyle=":", linewidth=1)

    plt.text(-1.2, 1.0, "$c$", fontsize=14)
    plt.text(1.12, 0.42, "$w$", fontsize=14)
    plt.ylim(0.465, 1.0)

    plt.legend()
    plt.show()
    return None


def make_future_kink(in_BoroCnstArt):
    """
    This figure illustrates how a the introduction of a current constraint can hide/move a kink that was induced by a future constraint.

    To construct this figure, we plot two consumption functions:
    1) perfect foresight consumer that faces one constraint in period 2
    2) perfect foresight consumer that faces the same constraint as above plus one more constraint in period 3

    Both consumption functions first loads the parameter set of the perfect foresight lifecycle households with ten periods.
    We then change the parameter "BoroCnstArt" which corresponds to big Tau in the paper, i.e. the set of future constraints ordered by time.
    """

    # Make and solve the consumer with only one borrowing constraint
    Bcons1 = IndShockConsumerType(**init_lifecycle)
    Bcons1.delFromTimeInv("BoroCnstArt")
    Bcons1.addToTimeVary("BoroCnstArt")
    Bcons1.BoroCnstArt = [None, 0, None, None, None, None, None, None, None, None]
    Bcons1.solve()
    Bcons1.unpack("cFunc")

    # Make and solve the consumer with more than one binding borrowing constraint
    BCons2 = IndShockConsumerType(**init_lifecycle)
    BCons2.delFromTimeInv("BoroCnstArt")
    BCons2.addToTimeVary("BoroCnstArt")
    BCons2.BoroCnstArt = [
        None,
        0,
        in_BoroCnstArt,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    BCons2.solve()
    BCons2.unpack("cFunc")

    x = np.linspace(1, 1.2, 500, endpoint=True)
    y_mod1 = Bcons1.cFunc[0](x)
    y_mod2 = BCons2.cFunc[0](x)

    where_close = np.isclose(y_mod1, y_mod2)
    x0 = x[where_close][0]
    y0 = y_mod1[where_close][0]

    y1dd = np.diff(y_mod1, n=2)
    ind1 = np.argmin(y1dd[:250]) + 1
    x1 = x[ind1]
    y1 = y_mod1[ind1]

    y2dd = np.diff(y_mod2, n=2)
    ind2 = np.argmin(y2dd[:250]) + 1
    x2 = x[ind2]
    y2 = y_mod2[ind2]

    # Display the figure
    # print('Figure 2: How a Current Constraint Can Hide a Future Kink')

    f = plt.figure()
    plt.plot(x, y_mod1, color="green", label="$c_{t,1}$")
    plt.plot(x, y_mod2, color="red", label="$\hat{c}_{t,2}$")
    # plt.text(1.15,1.01,"$\hat{c}_{t,2}$",fontsize=14)
    # plt.text(1.07,1.01,"$c_{t,1}$",fontsize=14)
    # plt.arrow(1.149,1.011,-0.01,0,head_width=0.001,width=0.0001,facecolor='black',length_includes_head='True')
    # plt.arrow(1.085,1.011,0.01,0,head_width=0.001,width=0.0001,facecolor='black',length_includes_head='True')

    plt.xlim(left=1.0, right=1.2)
    plt.ylim(0.98, 1.025)
    plt.tick_params(
        labelbottom=False,
        labelleft=False,
        left="off",
        right="off",
        bottom="off",
        top="off",
    )

    plt.text(0.99, 1.025, "$c$", fontsize=14)
    plt.text(1.20, 0.978, "$w$", fontsize=14)

    plt.text(0.988, y0, "$\hat{c}_{t,1}^{\#}$", fontsize=14)
    plt.text(0.988, y1 + 0.0015, "${c}_{t,1}^{\#}$", fontsize=14)
    plt.text(0.97, y2 - 0.0015, "$\hat{c}_{t,2}(w_{t,1})$", fontsize=14)

    plt.annotate(
        "kink that \n gets hidden",
        xy=(x1, y1),
        xytext=((x1 + 3) / 4, y1 + 0.005),
        arrowprops=dict(facecolor="black", headwidth=4, width=1, shrink=0.15),
    )

    plt.text(x0 - 0.005, 0.977, "$\hat{w}_{t,1}$", fontsize=14)
    plt.text(x1 - 0.005, 0.977, "$w_{t,1}$", fontsize=14)
    plt.text(x2 - 0.01, 0.975, "$\hat{w}_{t,2}$", fontsize=14)

    plt.plot([1, x0], [y0, y0], color="black", linestyle="--")
    plt.plot([1, x1], [y1, y1], color="black", linestyle="--")
    plt.plot([1, x2], [y2, y2], color="black", linestyle="--")

    plt.plot([x0, x0], [0.98, y0], color="black", linestyle="--")
    plt.plot([x1, x1], [0.98, y1], color="black", linestyle="--")
    plt.plot([x2, x2], [0.98, y2], color="black", linestyle="--")

    plt.legend()
    plt.show()
    return None


def make_cons_func(in_BoroCnstArt, in_TranShkStd):
    """
    This figure illustrates how the effect of risk is greater if there already exists a constraint.

    Initialize four types: unconstrained perfect foresight, unconstrained with risk, constrained perfect foresight, and constrained with risk.
    """

    WwCR_unconstr = IndShockConsumerType(**init_lifecycle)
    WwCR_unconstr.delFromTimeInv("BoroCnstArt")
    WwCR_unconstr.addToTimeVary("BoroCnstArt")
    WwCR_unconstr.solve()
    WwCR_unconstr.unpack("cFunc")

    init_lifecycle_risk2["TranShkStd"] = [0, in_TranShkStd, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    WwCR_risk = IndShockConsumerType(**init_lifecycle_risk2)
    WwCR_risk.delFromTimeInv("BoroCnstArt")
    WwCR_risk.addToTimeVary("BoroCnstArt")
    WwCR_risk.solve()
    WwCR_risk.unpack("cFunc")

    WwCR_constr = IndShockConsumerType(**init_lifecycle)
    WwCR_constr.cycles = 1  # Make this consumer live a sequence of periods exactly once
    WwCR_constr.delFromTimeInv("BoroCnstArt")
    WwCR_constr.addToTimeVary("BoroCnstArt")
    WwCR_constr.BoroCnstArt = [
        None,
        None,
        in_BoroCnstArt,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    WwCR_constr.solve()
    WwCR_constr.unpack("cFunc")

    WwCR_constr_risk = IndShockConsumerType(**init_lifecycle_risk2)
    WwCR_constr_risk.delFromTimeInv("BoroCnstArt")
    WwCR_constr_risk.addToTimeVary("BoroCnstArt")
    WwCR_constr_risk.BoroCnstArt = [
        None,
        None,
        in_BoroCnstArt,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    WwCR_constr_risk.solve()
    WwCR_constr_risk.unpack("cFunc")

    x = np.linspace(-8, -4, 1000, endpoint=True)
    y = WwCR_unconstr.cFunc[1](x)
    y2 = WwCR_risk.cFunc[1](x)
    y3 = WwCR_constr.cFunc[1](x)
    y4 = WwCR_constr_risk.cFunc[1](x)

    where_close = np.isclose(y, y3, atol=1e-05)
    where_close_risk = np.isclose(y2, y4, atol=1e-05)
    x0 = x[where_close][0]
    x1 = x[where_close_risk][0]
    y0 = y[where_close][0]
    y1 = y2[where_close_risk][0]

    # Display the figure
    # print('Figure 3: Consumption Functions With and Without a Constraint and a Risk')

    f = plt.figure()
    plt.plot(x, y, color="black", linewidth=3, label="${c}_{t,0}$")
    plt.plot(
        x, y2, color="black", linestyle="--", linewidth=3, label=r"$\tilde{c}_{t,0}$"
    )
    plt.plot(x, y3, color="red", label="${c}_{t,1}$")
    plt.plot(x, y4, color="red", linestyle="--", label=r"$\tilde{c}_{t,1}$")
    plt.xlim(left=-8, right=-4.5)
    plt.ylim(0, 0.30)
    plt.text(-8.15, 0.305, "$c$", fontsize=14)
    plt.text(-4.5, -0.02, "$w$", fontsize=14)

    # plt.plot([-6.15,-6.15],[0,0.05],color="black",linestyle=":")
    plt.plot([x0, x0], [0, y0], color="black", linestyle=":")
    plt.plot([x1, x1], [0, y1], color="black", linestyle=":")

    # plt.text(-6.2,-0.02,r"$\underline{w}_{t,1}$",fontsize=14)
    plt.text(x0, -0.02, r"${w}_{t,1}$", fontsize=14)
    plt.text(x1, -0.02, r"$\bar{w}_{t,1}$", fontsize=14)

    plt.tick_params(
        labelbottom=False,
        labelleft=False,
        left="off",
        right="off",
        bottom="off",
        top="off",
    )
    plt.legend()
    plt.show()
    return None
