# NiCo: Niche Covariation Analysis

Developed by Ankit Agrawal (c) Grün lab 2024

NiCo package designed to uncover covariation patterns between interacting cell types from image-based single-cell resolution spatial transcriptomics data. It enables comprehensive cell type annotations, niche interaction discoveries, and the analysis of covariation patterns between interacting cell types.


### Key Features <br>
* **Cell Type Annotation**: Perform accurate cell type annotations on single cell resolution spatial transcriptomics data. <br>
* **Niche Interaction**: Identify and analyze colocalized interactions between different cell types within their tissue niches. <br>
* **Covariation**: Discover covariates between colocalized cell types to understand the cross-talk of gene modules and the enrichment of pathways in the niche.  <br>


Ready for use! <br>
Tutorials and documentation are available!



### Installation  
Install the NiCo package using the conda environment. This ensures all dependencies are correctly managed and installed.

```shell
conda create -n nicoUser python=3.11
conda activate nicoUser
pip install nico-sc-sp
pip install jupyterlab
```

Sometimes, the ``pygraphviz`` package cannot be installed via pip, or during the cell type interaction part, it gives an error that "neato" is not found in path, so an alternative conda way of installation is recommended. Please follow the installation of ``pygraphviz`` [here](https://pygraphviz.github.io/documentation/stable/install.html)

```shell
conda create -y -n nicoUser python=3.11
conda activate nicoUser
conda install -c conda-forge pygraphviz
pip install nico-sc-sp
pip install jupyterlab
```

### Required packages built upon
By default, these packages should install automatically. However, if any version conflicts arise, you can manually install the specific versions using pip.

```shell
scanpy==1.11.2
seaborn==0.13.2
scipy==1.11.3
matplotlib==3.10.3
numpy==1.26.1
gseapy==1.1.4
xlsxwriter==3.1.9
numba==0.58.1
pydot==1.4.2
KDEpy==1.1.8
pygraphviz==1.11
networkx==3.2.1
scikit-learn==1.3.2
pandas==2.1.1
leidenalg
```


### Usage

Import the NiCo functions in your Python script or Jupyter Notebook as follows:

```
from nico import Annotations as sann
from nico import Interactions as sint
from nico import Covariations as scov
```



# Tutorials (Jupyter notebook)
Detailed tutorials are available to help you get started quickly. These tutorials will guide you through setting up and using NiCo for various applications. <br>
https://github.com/ankitbioinfo/nico_tutorial

# Documentations, tutorials (html) and API reference
Comprehensive documentation is available to guide you through the installation, usage, and features of NiCo. <br>
https://nico-sc-sp.readthedocs.io/en/latest/

# Reference
Ankit Agrawal, Stefan Thomann, Sukanya Basu, Dominic Grün. NiCo Identifies Extrinsic Drivers of Cell State Modulation by Niche Covariation Analysis. Submitted (under review), 2024


### Additional Resources:
Special thanks to the following utility packages used in the development of NiCo:

SCTransformPy <br>
https://github.com/atarashansky/SCTransformPy

pyliger <br>
https://github.com/welch-lab/pyliger

### Contact
For any questions or issues, please feel free to contact [ankitplusplus at gmail.com]. Your feedback and contributions are always welcome!
