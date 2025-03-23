# Experiment 4: High-Dimensional Spherical Intersection

## Objective
To evaluate how the process of iteratively intersecting spheres in high-dimensional space affects the accuracy of estimating a hidden point \( x \), and to observe the behavior of expected vs. observed error over multiple intersections.

## Setup
- **Dimension (D):** 784
- **Number of Spheres (N):** 128
- **Trials:** Single run with progressive logging

Each sphere is defined by:
- A random center \( \mu_i \sim 5 \cdot \mathcal{N}(0, I) \)
- A radius \( r_i = \|x - \mu_i\| \), such that the sphere passes through the true point \( x \)

At each step, the intersection of the current estimate with a new sphere is computed using geometric sphere intersection, yielding:
- A new center (\( \mu_{\text{intersect}} \))
- A new radius (\( r_{\text{intersect}} \))

The estimate of \( x \) is taken as the current center. The observed error is \( \|x - \hat{x}\| \), and the expected error is the radius.

## Results Summary
- The error rapidly drops in the first few intersections:
  - From \(~140 \rightarrow 60 \rightarrow 40 \rightarrow 30\)
- After around 50–60 spheres, the rate of reduction slows significantly
- Final expected and observed error converge to \(~29\)
- Observed error tracks expected error almost exactly

## Interpretation
This behavior reflects two main phenomena:

### 1. **Fast Early Convergence**
Early sphere intersections contribute strong geometric constraints, especially when the estimate sphere is large and intersecting spheres clip through it at different angles.

### 2. **Plateau in High Dimensions**
As the estimate sphere shrinks, newly intersected spheres (which still pass through \( x \) but are centered far away) appear nearly flat. Their constraints become less informative, and the intersection barely shrinks the estimate.

This is a direct consequence of high-dimensional geometry:
- Large spheres have low curvature near \( x \)
- Later constraints intersect almost tangentially
- Without any high-curvature (i.e., close) spheres, the estimate stabilizes at a finite radius

## Conclusion
The spherical intersection procedure performs well in high-dimensional space, with strong early improvements. However, convergence slows due to the flattening of constraints imposed by large-radius spheres. This experiment validates that expected error (radius) is a meaningful estimate of uncertainty, tightly coupled with actual error.

Future experiments may incorporate targeted, close-range constraints to improve late-stage convergence.

## Results
```
Intersecting 128 spheres across 784 dimensions
0: Expected Error: 140.60588074, Observed Error: 140.60588074
1: Expected Error: 96.55357361, Observed Error: 96.55356598
2: Expected Error: 80.81171417, Observed Error: 80.81171417
3: Expected Error: 70.19187927, Observed Error: 70.19187164
4: Expected Error: 64.37083435, Observed Error: 64.37082672
5: Expected Error: 59.61792755, Observed Error: 59.61791611
6: Expected Error: 57.60225296, Observed Error: 57.60223770
7: Expected Error: 55.25545120, Observed Error: 55.25543976
8: Expected Error: 53.12680817, Observed Error: 53.12679291
9: Expected Error: 51.66127396, Observed Error: 51.66126251
10: Expected Error: 49.79104996, Observed Error: 49.79103470
11: Expected Error: 48.57164001, Observed Error: 48.57163239
12: Expected Error: 47.32561111, Observed Error: 47.32560349
13: Expected Error: 46.10074234, Observed Error: 46.10073471
14: Expected Error: 45.16925812, Observed Error: 45.16925049
15: Expected Error: 44.53867340, Observed Error: 44.53866959
16: Expected Error: 44.36140060, Observed Error: 44.36139679
17: Expected Error: 43.10093307, Observed Error: 43.10092163
18: Expected Error: 42.56082916, Observed Error: 42.56081772
19: Expected Error: 42.00944138, Observed Error: 42.00943756
20: Expected Error: 41.39594269, Observed Error: 41.39593124
21: Expected Error: 41.37442780, Observed Error: 41.37442017
22: Expected Error: 40.52728653, Observed Error: 40.52727509
23: Expected Error: 40.21356964, Observed Error: 40.21355820
24: Expected Error: 39.61441040, Observed Error: 39.61440277
25: Expected Error: 39.10059738, Observed Error: 39.10058594
26: Expected Error: 38.91762924, Observed Error: 38.91761780
27: Expected Error: 38.65023041, Observed Error: 38.65022278
28: Expected Error: 38.44809723, Observed Error: 38.44808578
29: Expected Error: 38.32796860, Observed Error: 38.32795715
30: Expected Error: 38.14519882, Observed Error: 38.14518738
31: Expected Error: 37.71589279, Observed Error: 37.71588135
32: Expected Error: 37.56832123, Observed Error: 37.56831360
33: Expected Error: 37.37254715, Observed Error: 37.37253952
34: Expected Error: 37.30108261, Observed Error: 37.30107498
35: Expected Error: 37.07304382, Observed Error: 37.07304001
36: Expected Error: 37.03931427, Observed Error: 37.03931046
37: Expected Error: 36.87717819, Observed Error: 36.87717438
38: Expected Error: 36.76948547, Observed Error: 36.76947784
39: Expected Error: 36.68912888, Observed Error: 36.68912506
40: Expected Error: 36.56635666, Observed Error: 36.56635284
41: Expected Error: 36.12451553, Observed Error: 36.12451172
42: Expected Error: 35.90982056, Observed Error: 35.90981674
43: Expected Error: 35.70825577, Observed Error: 35.70825577
44: Expected Error: 35.51128387, Observed Error: 35.51128006
45: Expected Error: 35.31715775, Observed Error: 35.31715775
46: Expected Error: 35.23146057, Observed Error: 35.23146057
47: Expected Error: 35.04788971, Observed Error: 35.04788589
48: Expected Error: 34.96771240, Observed Error: 34.96770477
49: Expected Error: 34.72303772, Observed Error: 34.72303009
50: Expected Error: 34.69551849, Observed Error: 34.69550705
51: Expected Error: 34.52803421, Observed Error: 34.52803421
52: Expected Error: 34.32892990, Observed Error: 34.32892609
53: Expected Error: 34.15285110, Observed Error: 34.15284729
54: Expected Error: 33.86986160, Observed Error: 33.86986160
55: Expected Error: 33.67856216, Observed Error: 33.67856598
56: Expected Error: 33.45392609, Observed Error: 33.45392227
57: Expected Error: 33.26937103, Observed Error: 33.26937103
58: Expected Error: 33.13986969, Observed Error: 33.13986969
59: Expected Error: 33.01553345, Observed Error: 33.01553345
60: Expected Error: 32.97985458, Observed Error: 32.97985840
61: Expected Error: 32.86962128, Observed Error: 32.86962128
62: Expected Error: 32.73577499, Observed Error: 32.73577881
63: Expected Error: 32.54435730, Observed Error: 32.54435349
64: Expected Error: 32.49691391, Observed Error: 32.49691391
65: Expected Error: 32.21486664, Observed Error: 32.21486282
66: Expected Error: 32.14283371, Observed Error: 32.14282990
67: Expected Error: 31.99062538, Observed Error: 31.99062157
68: Expected Error: 31.98239326, Observed Error: 31.98239136
69: Expected Error: 31.96337128, Observed Error: 31.96336937
70: Expected Error: 31.89649963, Observed Error: 31.89649773
71: Expected Error: 31.87627792, Observed Error: 31.87627602
72: Expected Error: 31.81393051, Observed Error: 31.81393051
73: Expected Error: 31.80908966, Observed Error: 31.80908966
74: Expected Error: 31.76245117, Observed Error: 31.76245308
75: Expected Error: 31.66721916, Observed Error: 31.66721725
76: Expected Error: 31.66490364, Observed Error: 31.66490173
77: Expected Error: 31.64472198, Observed Error: 31.64472008
78: Expected Error: 31.60426331, Observed Error: 31.60426140
79: Expected Error: 31.59858513, Observed Error: 31.59858513
80: Expected Error: 31.59515572, Observed Error: 31.59515190
81: Expected Error: 31.57742882, Observed Error: 31.57742691
82: Expected Error: 31.57664680, Observed Error: 31.57664299
83: Expected Error: 31.39446259, Observed Error: 31.39446068
84: Expected Error: 31.31418991, Observed Error: 31.31418419
85: Expected Error: 31.31080246, Observed Error: 31.31079865
86: Expected Error: 31.29058266, Observed Error: 31.29058075
87: Expected Error: 31.04101562, Observed Error: 31.04101181
88: Expected Error: 31.01611710, Observed Error: 31.01611137
89: Expected Error: 30.91753960, Observed Error: 30.91753578
90: Expected Error: 30.84838867, Observed Error: 30.84838486
91: Expected Error: 30.79187775, Observed Error: 30.79187584
92: Expected Error: 30.74956894, Observed Error: 30.74956703
93: Expected Error: 30.70682907, Observed Error: 30.70682716
94: Expected Error: 30.65678024, Observed Error: 30.65678024
95: Expected Error: 30.60519791, Observed Error: 30.60519409
96: Expected Error: 30.58900833, Observed Error: 30.58900642
97: Expected Error: 30.53119087, Observed Error: 30.53118896
98: Expected Error: 30.50727654, Observed Error: 30.50727463
99: Expected Error: 30.42715836, Observed Error: 30.42715645
100: Expected Error: 30.42344856, Observed Error: 30.42344666
101: Expected Error: 30.29963684, Observed Error: 30.29963303
102: Expected Error: 30.24663925, Observed Error: 30.24663734
103: Expected Error: 30.21789551, Observed Error: 30.21789551
104: Expected Error: 30.11298180, Observed Error: 30.11297989
105: Expected Error: 29.82257652, Observed Error: 29.82257080
106: Expected Error: 29.79319763, Observed Error: 29.79319382
107: Expected Error: 29.77016068, Observed Error: 29.77015305
108: Expected Error: 29.68859482, Observed Error: 29.68858910
109: Expected Error: 29.67515755, Observed Error: 29.67515182
110: Expected Error: 29.67515755, Observed Error: 29.67514992
111: Expected Error: 29.65816307, Observed Error: 29.65815735
112: Expected Error: 29.65656853, Observed Error: 29.65656090
113: Expected Error: 29.63611984, Observed Error: 29.63611412
114: Expected Error: 29.63279915, Observed Error: 29.63278961
115: Expected Error: 29.61605644, Observed Error: 29.61605072
116: Expected Error: 29.58203506, Observed Error: 29.58202553
117: Expected Error: 29.58099747, Observed Error: 29.58098412
118: Expected Error: 29.57722092, Observed Error: 29.57721138
119: Expected Error: 29.31823349, Observed Error: 29.31822395
120: Expected Error: 29.27331543, Observed Error: 29.27330780
121: Expected Error: 29.25188255, Observed Error: 29.25187302
122: Expected Error: 29.24701881, Observed Error: 29.24701118
123: Expected Error: 29.23362923, Observed Error: 29.23362160
124: Expected Error: 29.23096275, Observed Error: 29.23095512
125: Expected Error: 29.14173508, Observed Error: 29.14172935
126: Expected Error: 29.09116554, Observed Error: 29.09115791
127: Expected Error: 29.08094788, Observed Error: 29.08094025
```