# SEPARATE

**Storm Event Partitioning And Rainfall Analytics for Tipping-bucket rain gauge data Evaluation (SEPARATE)**  
*Core Python functions for partitioning storm events from tipping-bucket rain gauge data.*

---

## What This Package Includes

This PyPI version includes only the **backend Python functions** used to partition storm events and calculate rainfall metrics.  
It is intended for developers who want to contribute to backend functionality or use SEPARATE in scripted workflows.  
**It does not include the GUI or prepackaged datasets.**

However, you can manually install PySimpleGUI after installing this package using a wheel file and download the associated images from the GitHub repository if you would like to use the GUI from this installation.

---

## Installation

```bash
pip install separate
```

> **Note:** PySimpleGUI is not included in this version.**  
> This version is intended for users who want to use SEPARATE functions in scripts or notebooks, rather than GUI-based applications.

---

## Example Usage

```python
# In Python, you can import core functions like this:
from separate.functions import SEPARATE_FUNCTIONS as sf
```

An example script for using these functions to execute the SEPARATE workflow can be found in  
[`SEPARATE_standalone_script.py`](https://github.com/WatershedsWildfireResearchCollaborative/SEPARATE/blob/main/SEPARATE_standalone_script.py) on our GitHub repository.

---

## Documentation

For the full GUI version and a detailed user manual (including screenshots and example workflows), please see the GitHub repository:

[SEPARATE on GitHub](https://github.com/WatershedsWildfireResearchCollaborative/SEPARATE)

---

## Authors

- Brendan Murphy (Simon Fraser University)
- Scott David (Utah State University)

---

## License

Licensed under the MIT License. See `LICENSE` for details.

---

## How to Use This

This version is ideal if you:
- Want to import SEPARATE's logic into your own analysis pipelines
- Need to script batch processing or run headless workflows
- Are not using the GUI
