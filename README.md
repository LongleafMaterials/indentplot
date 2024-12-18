# Tools to Parse and Plot Indentation Testing Data
I intend to develop these tools into a Python package to facilitate parsing, analysis, and visualization of indentation test data, e.g., nanoindentation, microindentation, etc. For usage and examples, see [sample_code.py](https://github.com/LongleafMaterials/indentplot/blob/main/examples/sample_code.py).

The package is currently only available from github and can be installed using one of the following commands:
```
pip install git+https://github.com/LongleafMaterials/indentplot.git --trusted-host github.com
```
or
```
pip install git+https://github.com/LongleafMaterials/indentplot.git --user
```

The first supported data format is for Bruker software (.tdm, .hld, and .txt outputs), specifically that from the [Hysitron PI 89](https://www.bruker.com/en/products-and-solutions/test-and-measurement/nanomechanical-instruments-for-sem-tem/hysitron-pi-89-sem-picoindenter.html).

![](/assets/readme_img1.png)
