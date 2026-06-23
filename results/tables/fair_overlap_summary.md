# Fair-Overlap Metrics

This table recomputes trajectory errors after cropping each sequence to the common timestamp interval shared by ground truth, ORB-SLAM3, and OpenVINS.

APE RMSE is computed after rigid position alignment on the common interval. Local delta RMSE measures frame-to-frame translation delta disagreement on timestamp-associated poses; it is a local consistency metric, not a full evo pose RPE replacement.

| Sequence | System | Overlap start (s) | Overlap end (s) | Overlap duration (s) | Matched poses | Fair APE RMSE (m) | Local delta RMSE (m) |
|---|---|---:|---:|---:|---:|---:|---:|
| MH_01_easy | orbslam3 | 1403636624.662620 | 1403636762.743556 | 138.081 | 2762 | 0.042271 | 0.003892 |
| MH_01_easy | openvins | 1403636624.662620 | 1403636762.743556 | 138.081 | 2746 | 0.090792 | 0.002050 |
| MH_03_medium | orbslam3 | 1403637149.987150 | 1403637264.393319 | 114.406 | 2289 | 0.032327 | 0.004714 |
| MH_03_medium | openvins | 1403637149.987150 | 1403637264.393319 | 114.406 | 2281 | 0.137622 | 0.004811 |
| MH_05_difficult | orbslam3 | 1403638539.292190 | 1403638630.547830 | 91.256 | 1825 | 0.065589 | 0.005087 |
| MH_05_difficult | openvins | 1403638539.292190 | 1403638630.547830 | 91.256 | 1823 | 0.242839 | 0.004257 |

