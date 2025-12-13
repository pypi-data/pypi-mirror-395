# Mathematical Methodology

## Overview

This document provides the complete mathematical methodology implemented in the `boot_dw` package, based on Jeong & Chung (2001).

## 1. The Regression Model

Consider the standard linear regression model:

$$y = X\beta + u$$

where:
- $y$ is an $n \times 1$ vector of dependent variable observations
- $X$ is an $n \times k$ matrix of regressors
- $\beta$ is a $k \times 1$ vector of parameters
- $u$ is an $n \times 1$ vector of errors

## 2. AR(1) Error Process

The errors follow a first-order autoregressive process:

$$u_t = \rho u_{t-1} + e_t, \quad |\rho| < 1$$

where:
- $\rho$ is the autocorrelation coefficient
- $e_t \sim \text{i.i.d.}(0, \sigma^2)$ are white noise innovations
- Stationarity requires $|\rho| < 1$

**Null Hypothesis:** $H_0: \rho = 0$ (no autocorrelation)

**Alternative Hypotheses:**
- $H_1: \rho > 0$ (positive autocorrelation) - **most common**
- $H_1: \rho < 0$ (negative autocorrelation)
- $H_1: \rho \neq 0$ (two-sided)

## 3. Classical Durbin-Watson Test

### 3.1 The DW Statistic

The Durbin-Watson statistic is defined as:

$$d = \frac{\sum_{t=2}^T (\\hat{u}_t - \hat{u}_{t-1})^2}{\sum_{t=1}^T \hat{u}_t^2} = \frac{\hat{u}' A \hat{u}}{\hat{u}' \hat{u}}$$

where $\hat{u} = (I - X(X'X)^{-1}X')u = Mu$ are OLS residuals, and

$$A = \begin{bmatrix}
1 & -1 & 0 & \cdots & 0 \\
-1 & 2 & -1 & \cdots & 0 \\
0 & -1 & 2 & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
0 & 0 & 0 & \cdots & 1
\end{bmatrix}$$

### 3.2 Relationship to ρ

The DW statistic is approximately:

$$d \approx 2(1 - \hat{\rho})$$

where $\hat{\rho} = \frac{\sum_{t=2}^T \hat{u}_t \hat{u}_{t-1}}{\sum_{t=1}^{T-1} \hat{u}_t^2}$

**Interpretation:**
- $d \approx 2$: No autocorrelation ($\rho \approx 0$)
- $d < 2$: Positive autocorrelation ($\rho > 0$)
- $d > 2$: Negative autocorrelation ($\rho < 0$)
- Range: $0 \leq d \leq 4$

### 3.3 The Indeterminate Range Problem

The distribution of $d$ depends on $X$ and is intractable. Durbin & Watson (1951) found bounds $(d_L, d_U)$ such that:

- If $d < d_L$: Reject $H_0$ (evidence of positive autocorrelation)
- If $d > d_U$: Do not reject $H_0$
- If $d_L \leq d \leq d_U$: **Inconclusive** (indeterminate range)

This indeterminate range **reduces test power** and creates practical difficulties.

## 4. Bootstrap Tests

Bootstrap methods eliminate the indeterminate range and improve finite-sample properties by constructing empirical distributions.

### 4.1 Recursive Bootstrap Procedure

For AR(1) errors, use **recursive bootstrap** (not standard bootstrap) to preserve serial correlation structure.

**Basic Algorithm:**
1. Estimate $\hat{\beta}$ and $\hat{\rho}$ from original data
2. Compute innovations $\hat{e}_t = \hat{u}_t - \hat{\rho}\hat{u}_{t-1}$
3. Resample innovations $e^*$ with replacement
4. Recursively construct $u^*_t = \rho^* u^*_{t-1} + e^*_t$
5. Generate bootstrap data $y^* = X\hat{\beta} + u^*$
6. Repeat $B$ times to build empirical distribution

## 5. Bootstrapped Durbin-Watson (BDW) Test

**Reference:** Jeong & Chung (2001), Section 3, pp. 55-56

### 5.1 Procedure

Given data $(y, X)$:

**Step 1:** Estimate $\hat{\beta}$ by OLS:
$$\hat{\beta} = (X'X)^{-1}X'y$$

**Step 2:** Calculate residuals $\hat{u} = y - X\hat{\beta}$

**Step 3:** Estimate $\hat{\rho}$ from residuals

**Step 4:** Compute innovations (for BDW, impose $H_0$):
$$\hat{e} = \hat{u}$$
(Under $H_0: \rho = 0$, innovations equal residuals)

**Bootstrap loop** ($b = 1, \ldots, B$):

**Step 5:** Resample innovations with replacement:
$$e^*_b = \{e^*_1, \ldots, e^*_n\} \sim \text{Random sample from } \hat{e}$$

**Step 6:** Under $H_0: \rho = 0$, set:
$$u^*_b = e^*_b$$
(No recursive construction needed under null)

**Step 7:** Create bootstrap data:
$$y^*_b = X\hat{\beta} + u^*_b$$

**Step 8:** Compute bootstrap DW statistic:
$$d^*_b = \frac{\sum_{t=2}^n (\hat{u}^*_{b,t} - \hat{u}^*_{b,t-1})^2}{\sum_{t=1}^n (\hat{u}^*_{b,t})^2}$$

where $\hat{u}^*_b$ are residuals from regressing $y^*_b$ on $X$.

**End loop**

### 5.2 Testing

**Empirical distribution:** $F^*_d = \{d^*_1, \ldots, d^*_B\}$

**P-value** (for $H_1: \rho > 0$):
$$p\text{-value} = \frac{1}{B}\sum_{b=1}^B \mathbb{1}(d^*_b \leq d_{\text{obs}})$$

**Critical value** at level $\alpha$:
$$c_\alpha = \text{Percentile}_\alpha(F^*_d)$$

**Decision:** Reject $H_0$ if $d_{\text{obs}} < c_\alpha$

### 5.3 Advantages

- Eliminates indeterminate range
- Distribution-free (robust to non-normality)
- Better finite-sample properties than classical DW
- Exact p-values available

## 6. Bootstrapped ρ (B-ρ) Test

**Reference:** Jeong & Chung (2001), Section 3, pp. 56-57

### 6.1 Procedure

**Key difference from BDW:** Bootstrap distribution constructed **under alternative** (conditional on sample), not under $H_0$.

Given data $(y, X)$:

**Step 1-2:** Same as BDW (estimate $\hat{\beta}$ and $\hat{u}$)

**Step 3:** Estimate $\hat{\rho}$:
$$\hat{\rho} = \frac{\sum_{t=2}^n \hat{u}_t \hat{u}_{t-1}}{\sum_{t=1}^{n-1} \hat{u}_t^2}$$

**Step 4:** Compute innovations:
$$\hat{e}_t = \hat{u}_t - \hat{\rho}\hat{u}_{t-1}, \quad t = 2, \ldots, n$$

**Bootstrap loop** ($b = 1, \ldots, B$):

**Step 5:** Resample innovations:
$$e^*_b = \{e^*_1, \ldots, e^*_{n-1}\} \sim \text{Random sample from } \{\hat{e}_2, \ldots, \hat{e}_n\}$$

**Step 6:** Pick initial value $e^*_{1,b} \sim \{\hat{e}_2, \ldots, \hat{e}_n\}$

**Step 7:** Recursively construct AR(1) errors using $\hat{\rho}$ (NOT imposing $H_0$):
$$u^*_{1,b} = \frac{e^*_{1,b}}{\sqrt{1 - \hat{\rho}^2}}$$
(Stationary initialization)

$$u^*_{t,b} = \hat{\rho} u^*_{t-1,b} + e^*_{t-1,b}, \quad t = 2, \ldots, n$$

**Step 8:** Estimate $\rho^*_b$ from bootstrap errors:
$$\rho^*_b = \frac{\sum_{t=2}^n u^*_{t,b} u^*_{t-1,b}}{\sum_{t=1}^{n-1} (u^*_{t,b})^2}$$

**End loop**

### 6.2 Testing (Percentile Method)

**Empirical distribution:** $F^*_\rho = \{\rho^*_1, \ldots, \rho^*_B\}$

**Confidence interval** at level $1-\alpha$:
$$[\text{Percentile}_{\alpha/2}(F^*_\rho), \text{Percentile}_{1-\alpha/2}(F^*_\rho)]$$

**One-sided test** ($H_1: \rho > 0$):
$$\text{Lower bound} = \text{Percentile}_{\alpha}(F^*_\rho)$$

**Decision:** Reject $H_0: \rho = 0$ if $0 <$ Lower bound

**P-value** (approximate):
$$p\text{-value} = \frac{1}{B}\sum_{b=1}^B \mathbb{1}(\rho^*_b \leq 0)$$

### 6.3 Advantages

- More direct test of $\rho$ than DW
- Potentially higher power than BDW
- No indeterminate range

### 6.4 Disadvantages

- Percentile method can have size distortions in small samples
- Solution: Use BCa method (next section)

## 7. Bias-Corrected Accelerated ρ (BCa-ρ) Test

**Reference:** Jeong & Chung (2001), Section 3, pp. 57; Efron (1987)

### 7.1 Motivation

The percentile method (B-ρ test) assumes the bootstrap distribution is:
- Unbiased
- Symmetric
- Homoscedastic

In **small samples**, these assumptions often fail, leading to:
- Skewed distributions
- Fat tails
- Size distortions

The BCa method corrects for both **bias** ($z_0$) and **acceleration** ($a_0$).

### 7.2 BCa Confidence Interval

The BCa $(1-\alpha)$ confidence interval is:

$$[\hat{G}^{-1}(\Phi(z_{\alpha}^{*})), \hat{G}^{-1}(\Phi(z_{1-\alpha}^{*}))]$$

where:
- $\hat{G}$ is the CDF of the bootstrap distribution $F^*_\rho$
- $\Phi$ is the standard normal CDF

**Adjusted percentiles:**
$$z_i^{*} = z_0 + \frac{z_0 + z^{(i)}}{1 - a_0(z_0 + z^{(i)})}$$

for $i \in \{\alpha, 1-\alpha\}$, where $z^{(i)} = \Phi^{-1}(i)$

### 7.3 Bias Correction Constant $z_0$

$$z_0 = \Phi^{-1}(\hat{G}(\hat{\rho}))$$

This measures how far the center of the bootstrap distribution is from $\hat{\rho}$.

**Interpretation:**
- $z_0 = 0$: Unbiased (median of $F^*_\rho$ equals $\hat{\rho}$)
- $z_0 > 0$: Upward bias
- $z_0 < 0$: Downward bias

**Computation:**
$$z_0 = \Phi^{-1}\left(\frac{1}{B}\sum_{b=1}^B \mathbb{1}(\rho^*_b \leq \hat{\rho})\right)$$

### 7.4 Acceleration Constant $a_0$

The acceleration constant corrects for skewness and variance instability.

**Definition:**
$$a_0 = \frac{\sum_{i=1}^n \dot{\theta}_i^3}{6 \left(\sum_{i=1}^n \dot{\theta}_i^2\right)^{3/2}}$$

where $\dot{\theta}_i$ is the **empirical influence function**.

**Jackknife estimation:**

For each $i = 1, \ldots, n$:
1. Delete observation $i$ to get $(y_{-i}, X_{-i})$
2. Compute $\hat{\rho}_{-i}$ from this jackknife sample
3. Calculate influence:
$$\dot{\theta}_i = (n-1)(\bar{\theta}_{(\cdot)} - \hat{\rho}_{-i})$$

where $\bar{\theta}_{(\cdot)} = \frac{1}{n}\sum_{i=1}^n \hat{\rho}_{-i}$

**Then:**
$$a_0 = \frac{\sum_{i=1}^n \dot{\theta}_i^3}{6 \left(\sum_{i=1}^n \dot{\theta}_i^2\right)^{3/2}}$$

**Interpretation:**
- $a_0 = 0$: Symmetric distribution, stable variance
- $a_0 \neq 0$: Distribution is skewed and/or has varying spread

### 7.5 Complete BCa-ρ Test Procedure

1. Perform B-ρ bootstrap to get $F^*_\rho = \{\rho^*_1, \ldots, \rho^*_B\}$
2. Calculate bias constant $z_0$
3. Calculate acceleration constant $a_0$ using jackknife
4. Compute adjusted percentiles:
   $$p_{\text{lower}} = \Phi\left(z_0 + \frac{z_0 + z_\alpha}{1 - a_0(z_0 + z_\alpha)}\right)$$
   $$p_{\text{upper}} = \Phi\left(z_0 + \frac{z_0 + z_{1-\alpha}}{1 - a_0(z_0 + z_{1-\alpha})}\right)$$
5. Get BCa interval:
   $$[\text{Percentile}_{p_{\text{lower}} \times 100}(F^*_\rho), \text{Percentile}_{p_{\text{upper}} \times 100}(F^*_\rho)]$$
6. Reject $H_0: \rho = 0$ if $0$ is outside the BCa interval

### 7.6 Properties (from Monte Carlo Studies)

Jeong & Chung (2001), Table 1 and Figures 1-16, show:

**Empirical size** (should be 0.05):
- Classical DW: Highly inaccurate (0.000-0.032)
- $(a + bd_U)$: Better but still poor (0.000-0.070)
- BDW: Good (0.042-0.060)
- B-ρ: Fair (0.014-0.050)
- **BCa-ρ: Best (0.024-0.064)** ✓

**Empirical power** (at $\rho = 0.5$, $n=50$, $k=3$):
- Classical DW: Poor, depends heavily on $(n,k)$
- $(a + bd_U)$: Better than DW
- BDW: Much better
- B-ρ: Even better
- **BCa-ρ: Highest power** ✓

**Robustness across sample sizes:**
- BCa-ρ maintains excellent performance from $n=10$ to $n=200$
- Other tests deteriorate significantly at small $n$

**Overall conclusion:** BCa-ρ test is **strongly recommended** for practical applications.

## 8. Implementation Details

### 8.1 Number of Bootstrap Replications

**Minimum:**
- For $\alpha = 0.05$: $B \geq 200$ (Jeong & Chung used 200)
- For $\alpha = 0.01$: $B \geq 1000$

**Rule of thumb:**
$$B \geq \frac{20}{\alpha}$$

**Trade-off:**
- Higher $B$: More accurate, slower
- Lower $B$: Faster, less stable

### 8.2 Stationarity Initialization

For stationary AR(1), the initial value should satisfy:
$$\text{Var}(u_0) = \frac{\sigma^2}{1 - \rho^2}$$

We use:
$$u^*_0 = \frac{e^*_0}{\sqrt{1 - \hat{\rho}^2}}$$

### 8.3 Handling Edge Cases

**Perfect autocorrelation** ($|\hat{\rho}| \approx 1$):
- Stationarity initialization may fail
- Alternative: Use $u^*_0 = 0$

**Small sample size** ($n < 20$):
- BCa method still works but requires more bootstrap replications
- Jackknife becomes computationally expensive

**High-dimensional case** ($k$ large relative to $n$):
- All bootstrap tests maintain advantage over classical DW
- Consider ridge regression for $\hat{\beta}$ if $k/n > 0.5$

## 9. Comparison Summary

| Feature | Classical DW | $(a+bd_U)$ | BDW | B-ρ | BCa-ρ |
|---------|-------------|-----------|-----|-----|-------|
| Indeterminate range | Yes | No | No | No | No |
| Distribution-free | No | No | Yes | Yes | Yes |
| Size accuracy | Poor | Fair | Good | Fair | **Excellent** |
| Power | Low | Medium | Good | Better | **Best** |
| Small sample | Poor | Poor | Good | Fair | **Excellent** |
| Computation | Fast | Fast | Slow | Slow | Slower |
| **Recommended?** | No | No | Sometimes | Sometimes | **Yes** |

## 10. References

1. Jeong, J. and Chung, S. (2001). "Bootstrap tests for autocorrelation". _Computational Statistics & Data Analysis_ 38: 49-69.

2. Durbin, J. and Watson, G.S. (1950). "Testing for Serial Correlation in Least Squares Regression I". _Biometrika_ 37: 409-428.

3. Durbin, J. and Watson, G.S. (1951). "Testing for Serial Correlation in Least Squares Regression II". _Biometrika_ 38: 159-178.

4. Efron, B. (1987). "Better Bootstrap Confidence Intervals". _Journal of the American Statistical Association_ 82: 171-200.

5. Efron, B. and Tibshirani, R.J. (1993). _An Introduction to the Bootstrap_. Chapman & Hall.

6. Davidson, R. and MacKinnon, J.G. (1996). Bootstrapping Econometric Models. Queen's University working paper.
