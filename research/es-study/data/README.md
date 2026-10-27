# Human reference data (not committed)

AuTexTification 2023, Spanish subtask 1, from https://huggingface.co/datasets/symanto/autextification2023 (licence CC BY-NC-SA 4.0, which is why the files stay out of this MIT repository). Download the two Spanish TSVs of subtask 1 into this folder as `autext-es-train.tsv` and `autext-es-test.tsv`, then run `python -I ../analyze.py`.

The study uses the rows labelled `human` in the domains news, reviews, wiki and tweets. All of them predate 2023. The dataset strips quotation marks from every text, so quotes are not compared.
