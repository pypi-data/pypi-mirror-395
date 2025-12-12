# NMFProfiler

## Name
NMFProfiler: A multi-omics integration method for samples stratified in groups

## Description

![NMFProfiler method scheme](images/nmfprofiler.png)

## Installation

NMFProfiler can be installed from PiPy:

```
pip install nmfprofiler
```

In addition, various docker images are provided in the [container registry](https://forge.inrae.fr/omics-integration/nmfprofiler/container_registry).

## Usage
Below is a short illustration of the method on a toy dataset.

```python
from nmfprofiler.nmfprofiler import NMFProfiler
from nmfprofiler.toyexample import ToyExample

# Fix a seed (not mandatory)
seed = 240820

# Run NMFProfiler
model = NMFProfiler(
    omics=[ToyExample().omic1, ToyExample().omic2],
    y=ToyExample().y,
    seed=seed,
    as_sklearn=False,
    backtrack=True)
res = model.fit()

# Get a quick overview of the dataset and model used
print(res)

# Visualize analyzed datasets (samples x features)
ToyExample().y  # 2 groups
res.heatmap(obj_to_viz="omic", width=15, height=6, path="", omic_number=1)
res.heatmap(obj_to_viz="omic", width=15, height=6, path="", omic_number=2)
```

![](images/omic1_Heatmap.png)
![](images/omic2_Heatmap.png)

*Note: NMFProfiler produces* **as many signatures as groups,** *i.e. levels in* $\mathbf{y}$ *vector. Hence in this case we will obtain 2 signatures.*

```python
# Visualize contribution matrix W obtained (samples x 2)
res.heatmap(obj_to_viz="W", width=10, height=10, path="")
```

![](images/W_Heatmap.png)

```python
# Visualize signature matrices H1 and H2 obtained (2 x features)
res.heatmap(obj_to_viz="H", width=15, height=6, path="", omic_number=1)
res.heatmap(obj_to_viz="H", width=15, height=6, path="", omic_number=2)
```

![](images/H1_Heatmap.png)
![](images/H2_Heatmap.png)

```python
# Monitor the size of each error term of the loss
res.barplot_error(width=15, height=6, path="")
```

![](images/BarplotErrors.png)

## Support
For questions or additional feature requests, use [gitlab issues](https://forge.inrae.fr/groups/omics-integration/-/issues) if possible. Authors can also be contacted by email (check authors' webpages for email information).

## Citation
If you are using `NMFProfiler`, please cite:

Mercadié, A., Gravier, É., Josse, G., Fournier, I., Viodé, C., Vialaneix, N., & Brouard, C. (2025). NMFProfiler: A multi-omics integration method for samples stratified in groups. *Bioinformatics*, **41**(2), btaf066.

## Authors and acknowledgment
This work was supported by the ANRT (CIFRE no. 2022/0051).

## License
GPL-3

## Project status
Active

See [Changelog](https://forge.inrae.fr/omics-integration/nmfprofiler/-/blob/main/CHANGELOG.md)
