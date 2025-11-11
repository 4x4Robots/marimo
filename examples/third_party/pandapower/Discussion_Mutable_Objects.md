


I'm learned pandapower using their interactive Jupyter notebook tutorials.
I never liked Jupyter notebooks because they're not reproducible (you can run cells in an arbitary order) so I was quite glad when I found marimo.


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

For this version see: `minimap_example_redefining.py`

