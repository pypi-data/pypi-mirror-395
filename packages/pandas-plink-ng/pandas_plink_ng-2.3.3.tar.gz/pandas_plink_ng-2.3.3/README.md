# pandas-plink-ng

> [!IMPORTANT]
> This repository is a **maintained fork** of [pandas-plink](https://github.com/limix/pandas-plink) by [Danilo Horta](https://github.com/horta) and contributors.  
> All credit for the original implementation belongs to the upstream authors.  
> This fork is maintained by [Kynon J M Benjamin](https://github.com/KrotosBenjamin) for compatibility with modern Python and GPU-based genomics workflows.

**Upstream project:** https://github.com/limix/pandas-plink  
**Current fork:** https://github.com/KrotosBenjamin/pandas-plink-ng  

### What’s different?
- Relaxed **NumPy dependency** → now supports **NumPy ≥ 2.0**.  
- No other functional changes to core code or API behavior.

---

## Overview

`pandas-plink-ng` provides Pythonic access to **PLINK** binary genotype files (`.bed/.bim/.fam`)  
and related matrices (e.g., GCTA `.rel` files).  
It uses **lazy loading** to minimize memory usage, reading genotypes only when accessed.

Notable historical changes prior to this fork are tracked in the  
[upstream CHANGELOG](https://raw.githubusercontent.com/limix/pandas-plink/master/CHANGELOG.md).

---

## Installation

Install from [PyPI](https://pypi.org/project/pandas-plink-ng/):

```bash
pip install pandas-plink-ng
````

This fork ensures compatibility with the latest
[RAPIDS](https://rapids.ai), [CuPy](https://cupy.dev), and [localQTL](https://github.com/heart-gen/localQTL)
GPU environments using NumPy 2.x.

If you prefer the original, CPU-focused package:

```bash
pip install pandas-plink
```

---

## Usage

Usage remains identical to the upstream API:

```python
from pandas_plink import read_plink1_bin

G = read_plink1_bin("chr11.bed", "chr11.bim", "chr11.fam", verbose=False)
print(G)
```

Output (example):

```
<xarray.DataArray 'genotype' (sample: 14, variant: 779)>
dask.array<shape=(14, 779), dtype=float64, chunksize=(14, 779)>
Coordinates:
  * sample   (sample) object 'B001' 'B002' ... 'B014'
  * variant  (variant) object '11_316849996' ... '11_345698259'
    a0       (variant) <U1 ...
    a1       (variant) <U1 ...
```

You can also read realized relationship matrices:

```python
from pandas_plink import read_rel

K = read_rel("plink2.rel.bin")
print(K)
```

For full API details, refer to the
[original pandas-plink documentation](https://pandas-plink.readthedocs.io/).

---

## Attribution

**Original Author:** [Danilo Horta](https://github.com/horta)
**Upstream License:** [MIT](https://raw.githubusercontent.com/limix/pandas-plink/master/LICENSE.md)
**Maintainer of this fork:** [Kynon J M Benjamin](https://github.com/KrotosBenjamin)

---

## License

This project remains under the [MIT License](https://raw.githubusercontent.com/limix/pandas-plink/master/LICENSE.md).
All original copyright notices are retained.
