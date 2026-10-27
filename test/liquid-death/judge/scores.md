# Judge and style scores, 2 runs of six items

| | close: mean rank of 4 | close: ranked first | spot: mean rank of 5 | spot: taken for the real one | trigram cosine to real | words vs real |
|---|---|---|---|---|---|---|
| none | 3.08 | 2 of 12 | 4.58 | 0 of 12 | 0.507 | 4.0x |
| line | 3.00 | 0 of 12 | 3.83 | 0 of 12 | 0.513 | 7.2x |
| samples | 1.58 | 9 of 12 | 2.08 | 0 of 12 | 0.485 | 2.9x |
| file | 2.33 | 1 of 12 | 3.50 | 0 of 12 | 0.479 | 3.2x |
| real | | | 1.00 | 12 of 12 | 1.000 | 1.0x |

Per item: {"close": {"samples": [1, 1, 1, 1, 1, 4, 1, 1, 1, 2, 1, 4], "line": [2, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 3], "file": [3, 3, 2, 2, 3, 3, 2, 2, 2, 1, 3, 2], "none": [4, 4, 4, 4, 2, 1, 4, 4, 3, 4, 2, 1]}, "spot": {"real": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "samples": [2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2], "file": [3, 4, 3, 3, 4, 4, 4, 3, 4, 3, 3, 4], "line": [4, 3, 4, 4, 5, 2, 3, 4, 5, 4, 5, 3], "none": [5, 5, 5, 5, 3, 5, 5, 5, 3, 5, 4, 5]}}
