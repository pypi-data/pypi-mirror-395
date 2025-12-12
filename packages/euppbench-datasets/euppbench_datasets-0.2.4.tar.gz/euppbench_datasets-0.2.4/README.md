# The EUMETNET postprocessing benchmark dataset Intake catalogue

[![PyPI version](https://badge.fury.io/py/euppbench-datasets.svg)](https://badge.fury.io/py/euppbench-datasets)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/euppbench-datasets.svg)](https://pypi.org/project/euppbench-datasets/)
[<img src="https://img.shields.io/badge/docs-online-green.svg">](https://eupp-benchmark.github.io/EUPPBench-doc)

A Python module using [Intake](https://github.com/intake/intake) catalogues to retrieve the Eumetnet postprocessing benchmark datasets.

Ease the download of the dataset time-aligned forecasts, reforecasts (hindcasts) and observations.

> * **Climetlab plugin version**: 0.3.3
> * **Intake catalogues version**: 0.2.4
> * **Base dataset version**: 1.0
> * **EUPPBench dataset version**: 1.0
> * **EUPreciPBench dataset version**: 0.5
> * **Dataset status**: [Datasets status](https://eupp-benchmark.github.io/EUPPBench-doc/files/datasets_status.html#datasets-status)

A [climetlab plugin](https://github.com/EUPP-benchmark/climetlab-eumetnet-postprocessing-benchmark) is also available, as an alternative way to get the datasets.

## Installation

The catalogue can be installed using [pip](https://pypi.org/).
Type in a terminal

    pip install euppbench-datasets 

and you are set!


## Documentation of the datasets

There are currently three sub-datasets available:

* [The base dataset over Europe's domain](https://eupp-benchmark.github.io/EUPPBench-doc/files/base_datasets.html) (available uniquely through the [climetlab plugin](https://github.com/EUPP-benchmark/climetlab-eumetnet-postprocessing-benchmark))
* [The EUPPBench dataset](https://eupp-benchmark.github.io/EUPPBench-doc/files/EUPPBench_datasets.html)
* [The EUPreciPBench dataset](https://eupp-benchmark.github.io/EUPPBench-doc/files/EUPreciPBench_datasets.html)

They are documented [here](https://eupp-benchmark.github.io/EUPPBench-doc/index.html).

## Using the Intake catalogues to access the data

Access through the catalogue can be done with the Python command line interface in a few lines:

```python
# Uncomment the line below if the catalogue is not yet installed
#!pip install euppbench-datasets
import euppbench_datasets
cat = euppbench_datasets.open_catalog()
ds = cat.euppbench.training_data.gridded.EUPPBench_highres_forecasts_surface.to_dask() 
```

which download the [original EUPPBench deterministic (high-resolution) forecasts](https://eupp-benchmark.github.io/EUPPBench-doc/files/EUPPBench_datasets.html#surface-variable-forecasts) 
in the [xarray](http://xarray.pydata.org/en/stable/index.html) format.

## Support and contributing

Please open a [issue on GitHub](https://github.com/EUPP-benchmark/intake-eumetnet-postprocessing-benchmark/issues).

## LICENSE

See the [LICENSE](https://github.com/EUPP-benchmark/intake-eumetnet-postprocessing-benchmark/blob/main/LICENSE) file for the code, and the [DATA_LICENSE](https://github.com/Climdyn/climetlab-eumetnet-postprocessing-benchmark/blob/main/DATA_LICENSE) for the data.

## Authors

See the [CONTRIBUTORS.md](https://github.com/EUPP-benchmark/intake-eumetnet-postprocessing-benchmark/blob/main/CONTRIBUTORS.md) file.

## Acknowledgments

This package was inspired by the [mlcast-datasets](https://github.com/mlcast-community/mlcast-datasets) written by Leif Denby.