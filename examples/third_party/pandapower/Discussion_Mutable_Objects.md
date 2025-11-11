


I'm learned pandapower using their interactive Jupyter notebook tutorials.
I never liked Jupyter notebooks because they're not reproducible (you can run cells in an arbitary order) so I was quite glad when I found marimo.

# The problem

[Variable mutations are not tracked](https://docs.marimo.io/guides/reactivity/#variable-mutations-are-not-tracked)

[Execution Order](https://docs.marimo.io/getting_started/key_concepts/#editing-notebooks)

Maybe I'm just using marimo in the wrong way and haven't found the trick how to work with mutating dataframes.
Especially in the experimenting and exploration/learning phase. Later I can easily move the whole setup into functions
and create the required `net` instance in only one cell.

# Available solutions

## 1st Method - marimo convert
I ran the marimo converter for the original [minimal example from pandapower](https://github.com/e2nIEE/pandapower/blob/7b6b2bf058525143ff590f57d0e8dce0fcef3f66/tutorials/minimal_example.ipynb):
```sh
marimo convert
```



This direct conversion is suboptimal because all net operations are mutating the `net` object. In the marimo philosophy this is forbidden (see ... for more information).

Here is a short video demonstrating this hidden state, when starting the notebook it runs in one order, but by manually rerunning specific cells you can change their output, because the `net` object is changed in other cells.

<video src="https://github.com/user-attachments/assets/b16f9396-12d3-4e5d-b19c-d28374e196a4">Video Hidden State</video>

## 2nd Method - renaming variables

In the user guide "[Coming from Jupyter](https://docs.marimo.io/guides/coming_from/jupyter/#redefining-variables)" the first suggestion is to **redefine variables**.

So I tried creating a new `net` instance each time I want to modify something in the grid.
The graph view shows better dependencies between cells.
So this works as indented and there is no more hidden state (the cell execution is deterministic), but the convenience of using a notebook drops slightly.
Especially because you have to keep track, what was the newest variable name, so you don't work with an old grid state.
This can become quite confusing (see `net_switches_created` and `net_switches_powerflow`).
But worse, this is not the normal usage for a `net` object in pandapower, where it should be mutated.
So you would learn contra to the best practices for the pandapower package.

For this version see: `[minimap_example_redefining.py](https://github.com/4x4Robots/marimo/blob/7a818a73bc5bb96e320620ad92d5f6bda9102638/examples/third_party/pandapower/minimal_example_redefining_variables.py)`

<image src="https://github.com/4x4Robots/marimo/blob/4x4Robots/pandapower_tutorials/examples/third_party/pandapower/public/Example_Redefining_Variables.png"></image>

## 3rd Method - manual DAG

When digging deeper into the [marimo documentation] there is a mention to manually define your DAG.

[Best practices -> Minimize mutations](https://docs.marimo.io/guides/best_practices/)

[Marimo Docs -> Why I can't redefine variables](https://docs.marimo.io/guides/understanding_errors/multiple_definitions/#why-cant-i-redefine-variables)


