


I'm learned pandapower using their interactive Jupyter notebook tutorials.
I never liked Jupyter notebooks because they're not reproducible (you can run cells in an arbitary order) so I was quite glad when I found marimo.


I ran the marimo converter for the original [minimal example from pandapower](https://github.com/e2nIEE/pandapower/blob/7b6b2bf058525143ff590f57d0e8dce0fcef3f66/tutorials/minimal_example.ipynb):
```sh
marimo convert
```



The direct conversion is bad because all net operations are mutating the `net` object. In the marimo philosophy this is forbidden (see ... for more information).

Here is a short video demonstrating this hidden state, when starting the notebook it runs in one order, but by manually rerunning specific cells you can change their output, because the `net` object is changed in other cells.

<video width="600" height="630" src="https://github.com/4x4Robots/marimo/blob/e05c5b0e635f51f9d1e64698f99b87196de657c4/examples/third_party/pandapower/public/Demonstation_Hidden_State_Mutating_Net.mp4"></video>

