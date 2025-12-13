# cupy_fft_match
A fast fuzzy matching algorithm based on FFT.

## Installation
```bash
pip install cupy_fft_match
```

## What is Fuzzy Matching
Consider $A$ and $B$; they are arrays, and $P$ is an array of the same length as $B$.

For any $0\leq k < \text{len}(A)$, we want to efficiently calculate:

$$
\text{Match}(A, B, P)_k = \sum_{i=0}^{\text{len}(B)-1} (A_{k + i} - B_{i})^2\cdot P_i
$$

in which $\text{Match}(A, B, P)$ is a generated array with length $\text{len}(A)-\text{len}(B)+1$.

To put it in a pragmatic way, let $A$ be a string or an 2D image, $B$ and $P$ is a template string/image that you want to match in $A$. Then, (the low value position of) $\text{Match}(A, B, P)$ gives the position in $A$ which suits $B$ well. 

If you don't need any wildcard, just let $P_i=1$ for any $i$. The position $i$ that satisfies $P_i=0$ is a wildcard. 

The interfaces provided in this project support arbitrary high-dimensional arrays. Therefore, you can use high-dimensional arrays for $A$, $B$, and $P$, the algorithm will work correctly as long as they have the same number of dimensions and the length of $A$ in each dimension is not less than that of $B$.

Since CuPy's ndarray is inherently different from NumPy's ndarray, please ensure that the data has been converted to the `cupy.ndarray` type before invoking the algorithms in this project.

## Usage
```python
import cupy as cp
import cupy_fft_match as cm

vec_a = cp.array([ ... ]) # vec_a is the text string
vec_b = cp.array([ ... ]) # vec_b is the template string, vec_b is usually "smaller" then vec_a
vec_p = cp.array([ ... ]) # vec_p is the weight string, which has the same size as vec_b
match_ans = cm.match_arr(vec_a, vec_b, vec_p)
```
