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
            mo.md(r"""
        # Minimal Example pandapower

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
    return bus3, line, net, pp, trafo


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
    net.load
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
def _(net, pp):
    pp.runpp(net)  # FORBIDDEN: mutating net
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And check out at the results for buses, lines an transformers:
    """)
    return


@app.cell
def _(net):
    net.res_bus
    return


@app.cell
def _(net):
    net.res_line
    return


@app.cell
def _(net):
    net.res_trafo
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Tap Changers

    We now lower the tap changer position, from position 0 to -1 and run another power flow:
    """)
    return


@app.cell
def _(net, pp, trafo):
    net.trafo.tap_pos.at[trafo] = -1  # FORBIDDEN: mutating net
    pp.runpp(net)  # FORBIDDEN: mutating net
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Looking at the results shows that bus voltages at the low voltage side of the transformer have increased:
    """)
    return


@app.cell
def _(net):
    net.res_bus
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Switches

    We now create an open switch at the load bus:
    """)
    return


@app.cell
def _(bus3, line, net, pp):
    pp.create_switch(net, bus=bus3, element=line, et="l", closed=False)  # FORBIDDEN: mutating net
    return


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
def _(net, pp):
    pp.runpp(net)  # FORBIDDEN: mutating net
    net.res_bus
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The load does not feed in:
    """)
    return


@app.cell
def _(net):
    net.res_load
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And the line is in open loop operation:
    """)
    return


@app.cell
def _(net):
    net.res_line
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Topological Analysis

    The structure of the network can also be directly analyzed with the topology package. It uses an interface to the NetworkX library for graph searches. There are some predefined search algorithms, such as searching for unsupplied buses:
    """)
    return


@app.cell
def _(net):
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
    net.switch.closed.at[0] = True  # FORBIDDEN: mutating net
    top.unsupplied_buses(net)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Apart from predefined search functions, it is also possible to translate the pandapower network into a NetworkX graph and run searches directly on that graph.

    Suppose we want to find all buses that are on the same voltage level as the load bus. We then translate the grid into a graph but excluding the transformer:
    """)
    return


@app.cell
def _(net, top):
    mg = top.create_nxgraph(net, include_trafos=False)
    return (mg,)


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
def _(net):
    net.ext_grid["s_sc_max_mva"] = 100  # FORBIDDEN: mutating net
    net.ext_grid["rx_max"] = 0.1  # FORBIDDEN: mutating net
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Now we can calculate short circuits. Here, we calculate a three phase short circuit current with a fault impedance of 2 Ohms:
    """)
    return


@app.cell
def _(net):
    import pandapower.shortcircuit as sc

    sc.calc_sc(net, case="max", ip=True, r_fault_ohm=2.0)  # FORBIDDEN: mutating net
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Initial and peak short circuit currents are given for faults at all buses:
    """)
    return


@app.cell
def _(net):
    net.res_bus_sc
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    This concludes a short walkthrough of some pandapower features. More in-depth tutorials can be found in the pandapower documentation:
    https://www.pandapower.org/start/#interactive-tutorials-
    """)
    return


if __name__ == "__main__":
    app.run()
