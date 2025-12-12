# robcointeg

## Outlier-Robust Cointegration Analysis

[![Python Version](https://img.shields.io/pypi/pyversions/robcointeg)](https://pypi.org/project/robcointeg/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python implementation of outlier-robust cointegration testing based on the methodology of Franses & Lucas (1998).

**Author:** Dr Merwan Roudane  
**Email:** merwanroudane920@gmail.com  
**GitHub:** https://github.com/merwanroudane/robcointeg

---

## Overview

Standard unit-root and cointegration tests are sensitive to atypical events such as outliers and structural breaks. This package implements the outlier-robust cointegration test proposed by Franses & Lucas (1998), which provides:

1. **Robust Cointegration Testing**: A pseudolikelihood ratio (PLR) test based on the Student-*t* distribution that is less sensitive to outliers than the standard Gaussian-based Johansen test.

2. **Outlier Detection**: Observation weights that identify which data points may be driving the cointegration results.

3. **Diagnostic Tools**: Methods for comparing robust and non-robust test results to signal when standard cointegration results might be influenced by aberrant observations.

---

## Installation

### From PyPI (when published)

```bash
pip install robcointeg
```

### From Source

```bash
git clone https://github.com/merwanroudane/robcointeg.git
cd robcointeg
pip install -e .
```

### With Plotting Support

```bash
pip install robcointeg[plotting]
```

### Full Installation (all optional dependencies)

```bash
pip install robcointeg[full]
```

---

## Quick Start

### Basic Usage

```python
import numpy as np
from robcointeg import RobustVAR, compare_tests, diagnostic_report

# Generate sample data
np.random.seed(42)
T = 100
y = np.cumsum(np.random.randn(T, 2), axis=0)

# Add an outlier
y[50, 0] += 5

# Fit robust VAR model
model = RobustVAR(p=2, nu=5)
model.fit(y)

# View results
print(model.summary())
print(f"Observation weights: {model.weights}")
```

### Cointegration Testing

```python
from robcointeg import plr_test, johansen_trace_test

# Robust test (Student-t based)
robust_result = plr_test(y, p=2, nu=5, r=0)
print(f"Robust PLR statistic: {robust_result.test_statistic:.2f}")
print(f"Reject at 5%: {robust_result.reject[0.05]}")

# Standard Johansen test for comparison
johansen_result = johansen_trace_test(y, p=2, r=0)
print(f"Johansen statistic: {johansen_result.test_statistic:.2f}")
```

### Compare Robust and Non-Robust Tests

```python
from robcointeg import compare_tests

comparison = compare_tests(y, p=2, nu=5)
print(comparison['summary'])

if comparison['conflict']:
    print("⚠ Tests give different results!")
    print(f"Gaussian rank: {comparison['gaussian_rank']}")
    print(f"Robust rank: {comparison['robust_rank']}")
```

### Full Diagnostic Report

```python
from robcointeg import diagnostic_report

report = diagnostic_report(
    y, p=2, nu=5,
    variable_names=['Y1', 'Y2'],
    significance_level=0.05
)
```

---

## Methodology

This package implements the methodology from:

> **Franses, P.H. & Lucas, A. (1998)**. "Outlier Detection in Cointegration Analysis", *Journal of Business & Economic Statistics*, 16:4, 459-468.

### Key Equations

**1. VAR/VECM Model (Equation 1):**

$$\Delta y_t = \alpha\beta' y_{t-1} + \Phi_1 \Delta y_{t-1} + \cdots + \Phi_{p-1} \Delta y_{t-p+1} + \mu + \varepsilon_t$$

**2. Student-*t* Pseudolikelihood (Equation 2):**

$$\mathcal{L}(\theta) = \prod_{t=1}^{T} \frac{\Gamma((\nu+k)/2)}{\Gamma(\nu/2)|\pi\nu V|^{1/2}} \left(1 + \frac{\varepsilon_t' V^{-1} \varepsilon_t}{\nu}\right)^{-(\nu+k)/2}$$

**3. Pseudolikelihood Ratio Test (Equation 3):**

$$\text{PLR} = 2 \ln\left(\frac{\mathcal{L}(\hat{\theta})}{\mathcal{L}(\tilde{\theta})}\right)$$

**4. Observation Weights (Equation 8):**

$$w_t = \left(\frac{\nu}{\nu + \varepsilon_t' V^{-1} \varepsilon_t}\right)^{1/2}$$

### Interpretation of Weights

- **Low weight** ($w_t < 0.67$ for $\nu=5$, $k=2$): The observation does not correspond to the general pattern of the model and deserves closer inspection.
- Consecutive low weights may indicate **additive outliers (AO)**.
- Low weights at the start and end of a period may indicate **level shifts**.
- Many consecutive low weights may indicate **variance shifts**.

---

## API Reference

### Core Classes

#### `RobustVAR`

```python
from robcointeg import RobustVAR

model = RobustVAR(p=2, nu=5, with_constant=True)
model.fit(y)

# Attributes
model.weights        # Observation weights
model.residuals      # Model residuals
model.log_likelihood # Log pseudolikelihood
model.Pi             # Long-run impact matrix
model.alpha          # Loading matrix
model.beta           # Cointegrating vectors
model.eigenvalues    # Eigenvalues
```

#### `RobustCointegrationTest`

```python
from robcointeg import sequential_plr_test

result = sequential_plr_test(y, p=2, nu=5)

# Attributes
result.test_results    # List of test results for each rank
result.selected_rank   # Determined cointegrating rank
result.weights         # Observation weights
result.outlier_indices # Detected outlier indices
result.summary         # Text summary
```

### Main Functions

| Function | Description |
|----------|-------------|
| `plr_test()` | Perform PLR test for a specific rank |
| `johansen_trace_test()` | Standard Johansen trace test |
| `compare_tests()` | Compare robust and non-robust tests |
| `compute_weights()` | Compute observation weights |
| `detect_outliers()` | Identify outlying observations |
| `diagnostic_report()` | Generate full diagnostic report |

### Critical Values

The package includes critical values from Table 1 of Franses & Lucas (1998):

```python
from robcointeg import get_critical_value, CriticalValueTable

# Get single critical value
cv = get_critical_value(k_minus_r=2, nu=5, significance_level=0.05)

# Access full table
table = CriticalValueTable(with_drift=True)
print(table.print_table())
```

---

## Examples

### Example 1: Finland/U.S. Real Exchange Rate

This replicates the empirical application from Section 3 of the paper:

```python
import numpy as np
from robcointeg import compare_tests, plot_comparison_panel

# Load Finland/U.S. exchange rate data (hypothetical)
# y should contain: log(CPI_US), log(CPI_Finland), log(Exchange_Rate)

comparison = compare_tests(y, p=2, nu=5)
print(comparison['summary'])

# Visualize (requires matplotlib)
plot_comparison_panel(
    y, comparison['weights'], comparison['outlier_indices'],
    nu=5, k=3, title='Finland/U.S. Real Exchange Rate Analysis'
)
```

### Example 2: Monte Carlo Simulation

```python
from robcointeg import monte_carlo_critical_values

# Simulate critical values
cv = monte_carlo_critical_values(
    k_minus_r=2, nu=5, n_sim=10000, T=100, with_drift=True
)
print(f"95% critical value: {cv[0.95]:.2f}")
```

---

## Citation

If you use this package in your research, please cite the original paper:

```bibtex
@article{franses1998outlier,
  title={Outlier Detection in Cointegration Analysis},
  author={Franses, Philip Hans and Lucas, Andr{\'e}},
  journal={Journal of Business \& Economic Statistics},
  volume={16},
  number={4},
  pages={459--468},
  year={1998},
  publisher={Taylor \& Francis}
}
```

And this software:

```bibtex
@software{robcointeg,
  author = {Roudane, Merwan},
  title = {robcointeg: Outlier-Robust Cointegration Analysis in Python},
  year = {2025},
  url = {https://github.com/merwanroudane/robcointeg}
}
```

---

## References

- Franses, P.H. & Lucas, A. (1998). "Outlier Detection in Cointegration Analysis", *Journal of Business & Economic Statistics*, 16:4, 459-468.
- Johansen, S. (1988). "Statistical Analysis of Cointegration Vectors", *Journal of Economic Dynamics and Control*, 12, 231-254.
- Johansen, S. (1991). "Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models", *Econometrica*, 59, 1551-1580.
- Lucas, A. (1997). "Cointegration Testing Using Pseudo Likelihood Ratio Tests", *Econometric Theory*, 13, 149-169.
- Lucas, A. (1998). "Inference on Cointegrating Ranks Using LR and LM Tests Based on Pseudo Likelihoods", *Econometric Reviews*, 17, 185-214.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Changelog

### Version 0.0.1 (2025)

- Initial release
- Implementation of Franses & Lucas (1998) methodology
- Student-t pseudolikelihood ratio (PLR) test
- Observation weight computation
- Outlier detection
- Comparison with standard Johansen test
- Visualization tools
- Critical value tables from the original paper
