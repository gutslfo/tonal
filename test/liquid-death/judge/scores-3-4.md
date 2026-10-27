# Judge and style scores, 2 runs of six items

| | close: mean rank of 5 | close: ranked first | spot: mean rank of 6 | spot: taken for the real one | trigram cosine to real | words vs real |
|---|---|---|---|---|---|---|
| none | 3.83 | 2 of 12 | 5.75 | 0 of 12 | 0.507 | 4.0x |
| line | 4.33 | 0 of 12 | 4.92 | 0 of 12 | 0.513 | 7.2x |
| samples | 2.33 | 4 of 12 | 2.92 | 0 of 12 | 0.485 | 2.9x |
| file | 2.92 | 1 of 12 | 4.00 | 0 of 12 | 0.479 | 3.2x |
| kit | 1.58 | 5 of 12 | 2.42 | 0 of 12 | 0.460 | 2.8x |
| real | | | 1.00 | 12 of 12 | 1.000 | 1.0x |

Per item: {"close": {"samples": [1, 2, 3, 3, 1, 4, 1, 2, 2, 3, 1, 5], "kit": [2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2], "file": [3, 3, 2, 2, 3, 5, 3, 3, 3, 1, 4, 3], "line": [4, 4, 5, 4, 5, 3, 4, 5, 5, 4, 5, 4], "none": [5, 5, 4, 5, 4, 1, 5, 4, 4, 5, 3, 1]}, "spot": {"real": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "samples": [2, 4, 4, 3, 2, 4, 2, 3, 2, 3, 2, 4], "kit": [3, 2, 2, 2, 3, 2, 3, 2, 3, 2, 3, 2], "file": [4, 3, 3, 4, 4, 5, 4, 4, 4, 4, 4, 5], "line": [5, 5, 5, 5, 6, 3, 5, 5, 6, 5, 6, 3], "none": [6, 6, 6, 6, 5, 6, 6, 6, 5, 6, 5, 6]}}
