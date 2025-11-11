# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "pandas==2.2.3",
#     "pandapower==3.2.1",
#     "numba==0.62.1"
# ]
# ///

import marimo

__generated_with = "0.17.7"
app = marimo.App()

with app.setup:
    # Initialization code that runs before all other cells
    import marimo as mo
    import copy

    import pandas as pd

    # Ignore pandas downcasting warnings
    pd.set_option("future.no_silent_downcasting", True)
    # Ignore pandas future warnings about copy-on-write
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#evaluation-order-matters
    import warnings

    warnings.filterwarnings(action="ignore", category=FutureWarning)


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""# Minimal Example pandapower - Redefining variables"""),
            mo.callout(
                r"""
                This notebook uses unique global variables to signify different
                stages of the pandapower network. This ensures all necessary
                cells for each stage are always run in the same order.
                """,
                kind="warn",
            ),
            mo.md(r"""

                ## Creating a Power System

                We consider the following simple 3-bus example network as a minimal example:
        """),
            mo.image(src="./pics/3bus-system.png", width="50%"),
            mo.md(r"""
                The above network can be created in pandapower as follows:
            """),
        ]
    )
    return


@app.cell
def _():
    import pandapower as pp

    # create empty net
    net = pp.create_empty_network()

    # create buses
    bus1 = pp.create_bus(net, vn_kv=20.0, name="Bus 1")
    bus2 = pp.create_bus(net, vn_kv=0.4, name="Bus 2")
    bus3 = pp.create_bus(net, vn_kv=0.4, name="Bus 3")

    # create bus elements
    pp.create_ext_grid(net, bus=bus1, vm_pu=1.02, name="Grid Connection")
    pp.create_load(net, bus=bus3, p_mw=0.100, q_mvar=0.05, name="Load")

    # create branch elements
    trafo = pp.create_transformer(net, hv_bus=bus1, lv_bus=bus2, std_type="0.4 MVA 20/0.4 kV", name="Trafo")
    line = pp.create_line(net, from_bus=bus2, to_bus=bus3, length_km=0.1, std_type="NAYY 4x50 SE", name="Line")

    finished_init = True
    return bus3, finished_init, line, net, pp, trafo


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Data Structure

    Each dataframe in a pandapower net object contains the information about one pandapower element, such as line, load transformer etc.
    """)
    return


@app.cell
def _(net):
    net.bus
    return


@app.cell
def _(net):
    net.line
    return


@app.cell
def _(net):
    net.trafo
    return


@app.cell
def _(net):
    net.load  # When rerunning this cell manually the results can CHANGE
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Note that line and transformer are created with standard types, so thath the electric parameters of are automatically filled in from the standard type library.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Power Flow

    We now run a power flow:
    """)
    return


@app.cell
def _(finished_init, net, pp):
    finished_init  # only run after init-cell
    pp.runpp(net)  # WARNING - mutating net
    finished_powerflow = True  # signal that powerflow has been run
    return (finished_powerflow,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And check out at the results for buses, lines an transformers:
    """)
    return


@app.cell
def _(finished_powerflow, net):
    finished_powerflow  # only run when powerflow has been finished
    finished_powerflow_2 = True  # signal that this second order cell for powerflow have been run, otherwise other cells might be faster and different results are shown.
    net.res_bus  # use the same variable name like in production scripts
    return (finished_powerflow_2,)


@app.cell
def _(finished_powerflow, net):
    finished_powerflow  # only run when powerflow has been finished
    finished_powerflow_3 = True
    net.res_line
    return (finished_powerflow_3,)


@app.cell
def _(finished_powerflow, net):
    finished_powerflow  # only run when powerflow has been finished
    finished_powerflow_4 = True
    net.res_trafo
    return (finished_powerflow_4,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Tap Changers

    We now lower the tap changer position, from position 0 to -1 and run another power flow:
    """)
    return


@app.cell
def _(
    finished_powerflow,
    finished_powerflow_2,
    finished_powerflow_3,
    finished_powerflow_4,
    net,
    pp,
    trafo,
):
    # only run when ALL powerflow cells are done
    finished_powerflow, finished_powerflow_2, finished_powerflow_3, finished_powerflow_4
    finished_tap_changers = True
    net.trafo.tap_pos.at[trafo] = -1  # WARNING - mutating net
    pp.runpp(net)  # WARNING - mutating net
    return (finished_tap_changers,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Looking at the results shows that bus voltages at the low voltage side of the transformer have increased:
    """)
    return


@app.cell
def _(finished_tap_changers, net):
    finished_tap_changers
    finished_tap_changers_2 = True
    net.res_bus  # always showing the correct results for this calculation
    return (finished_tap_changers_2,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Switches

    We now create an open switch at the load bus:
    """)
    return


@app.cell
def _(bus3, finished_tap_changers, finished_tap_changers_2, line, net, pp):
    finished_tap_changers, finished_tap_changers_2
    finished_switches = True
    pp.create_switch(net, bus=bus3, element=line, et="l", closed=False)  # WARNING - mutating net
    # show intermediate results of this step:
    return (finished_switches,)


@app.cell(hide_code=True)
def _():
    mo.vstack(
        [
            mo.md(r"""
        The open switch cuts the load bus from power supply:
        """),
            mo.image(src="./pics/3bus-system_switch.png", width="8%"),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    This can be verified by running a power flow and inspecting the results. The voltage at bus 2 is given as NaN:
    """)
    return


@app.cell
def _(finished_switches, net, pp):
    finished_switches
    finished_switches_2 = True
    pp.runpp(net)  # WARNING - mutating net
    net.res_bus
    return (finished_switches_2,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The load does not feed in:
    """)
    return


@app.cell
def _(finished_switches, finished_switches_2, net):
    finished_switches, finished_switches_2
    finished_switches_3 = True
    net.res_load
    return (finished_switches_3,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And the line is in open loop operation:
    """)
    return


@app.cell
def _(finished_switches, finished_switches_2, net):
    finished_switches, finished_switches_2
    finished_switches_4 = True
    net.res_line
    return (finished_switches_4,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Topological Analysis

    The structure of the network can also be directly analyzed with the topology package. It uses an interface to the NetworkX library for graph searches. There are some predefined search algorithms, such as searching for unsupplied buses:
    """)
    return


@app.cell
def _(
    finished_switches,
    finished_switches_2,
    finished_switches_3,
    finished_switches_4,
    net,
):
    finished_switches, finished_switches_2, finished_switches_3, finished_switches_4
    import pandapower.topology as top

    top.unsupplied_buses(net)
    return (top,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The package correctly determines that bus 2 is cut from power supply. When we close the switch, there are no unsupplied buses anymore:
    """)
    return


@app.cell
def _(net, top):
    # only run when top is defined
    net.switch.closed.at[0] = True  # WARNING - mutating net
    finished_top_2 = True
    top.unsupplied_buses(net)
    return (finished_top_2,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Apart from predefined search functions, it is also possible to translate the pandapower network into a NetworkX graph and run searches directly on that graph.

    Suppose we want to find all buses that are on the same voltage level as the load bus. We then translate the grid into a graph but excluding the transformer:
    """)
    return


@app.cell
def _(finished_top_2, net, top):
    finished_top_2
    finished_networkx = True
    mg = top.create_nxgraph(net, include_trafos=False)
    return finished_networkx, mg


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And search for all buses that are connected to the load bus in that graph:
    """)
    return


@app.cell
def _(mg, top):
    list(top.connected_component(mg, 2))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The graph search finds all buses that are on the same voltage level. Searches like these can be used for feeder identification and many more applications.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Short Circuit Analysis

    pandapower includes a short circuit module that complies with IEC 60909. To run a short circuit analysis, we need to define short circuit parameters for the external grid:
    """)
    return


@app.cell
def _(finished_networkx, net):
    finished_networkx
    finished_sc = True
    net.ext_grid["s_sc_max_mva"] = 100  # WARNING - mutating net
    net.ext_grid["rx_max"] = 0.1  # WARNING - mutating net
    return (finished_sc,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Now we can calculate short circuits. Here, we calculate a three phase short circuit current with a fault impedance of 2 Ohms:
    """)
    return


@app.cell
def _(finished_sc, net):
    finished_sc
    import pandapower.shortcircuit as sc
    finished_sc_calculation = True

    sc.calc_sc(net, case="max", ip=True, r_fault_ohm=2.0)  # WARNING - mutating net
    return (finished_sc_calculation,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Initial and peak short circuit currents are given for faults at all buses:
    """)
    return


@app.cell
def _(finished_sc_calculation, net):
    finished_sc_calculation
    net.res_bus_sc
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    This concludes a short walkthrough of some pandapower features. More in-depth tutorials can be found in the pandapower documentation:
    https://www.pandapower.org/start/#interactive-tutorials-
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.callout(
        r"""
        The order in which the cells are run are manually enforced. As long as you don't forget to add cell dependecies the results are correct.
    """,
        kind="success",
    )
    return


if __name__ == "__main__":
    app.run()
