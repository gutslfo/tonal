# Liquid Death, the real texts behind this test

Every text here is Liquid Death's own copy, read off liquiddeath.com on 2026-10-26 (the Shopify product feed `products.json` and the rendered pages). The brand name alone is changed: "Liquid Death" became "Grave Water" everywhere, in the samples, the requests and the real texts the judges see. The writing model knows Liquid Death's voice from its training. A founder using Tonal has a brand no model has read about, so the test hides the name to recreate that. The name stays death-themed so that the jokes in the texts still make sense.

Nothing else was edited: spelling, curly or straight quotes, capitals and the one emoji are as published. Cuts are listed below.

## Samples, given to the founder in `en.md`

| Text | Source | Date |
|---|---|---|
| 1, about page | https://liquiddeath.com/pages/manifesto | page created 2021-05-30, updated 2025-02-09 |
| 2, four FAQ answers | https://liquiddeath.com/pages/faq | page created 2021-09-02; read as live on 2026-10-26 |
| 3, Sinister Ginger page | https://liquiddeath.com/products/sinister-ginger | product created 2026-07-06 |
| 4, gift card | https://liquiddeath.com/products/gift-cards | created 2025-05-23 |
| 4, Welcome To Health doormat | https://liquiddeath.com/products/welcome-to-health-doormat | created 2024-12-11 |
| 4, The Death Dispenser | https://liquiddeath.com/products/death-dispenser | created 2021-07-27 |
| 4, Freeze To Death cold plunge | https://liquiddeath.com/products/freeze-to-death-cold-plunge | created 2024-09-17 |

Cuts: the about page's closing form ("Tell us about you:"), the gift card's legal "Fine Print" paragraph.

## Held out, in `heldout.json`

Six product texts the interview never sees. All six were created between 2026-07-13 and 2026-08-18. The writing model's training data stops earlier, so it cannot have read them. The requests give the facts the real text uses, plus what the product photo shows (a skull-covered silver tankard, a red three-eyed head as a pot, a tee printed like a "thank you" plastic bag). They were written before any model wrote a word, and none of them describes the voice.

| Id | Source | Created |
|---|---|---|
| mug | https://liquiddeath.com/products/mug-of-doom | 2026-08-07 |
| mitts | https://liquiddeath.com/products/liquid-death-x-deathgrip-murder-mitts | 2026-08-07 |
| sleeping-bag | https://liquiddeath.com/products/liquid-death-x-rumpl-body-bag-sleeping-bag | 2026-07-30 |
| planter | https://liquiddeath.com/products/pot-head-planter | 2026-08-07 |
| tee | https://liquiddeath.com/products/teenage-shirtbag-tee-unisex | 2026-07-13 |
| energy | https://liquiddeath.com/products/blood-zero | 2026-08-18 |

Cuts: the tee's link line ("Shop the Women's Ringer here."), and the energy page's spec list, which keeps only its opening paragraph.

## Limits known before the run

All six held-out texts are short product descriptions from one shop, so they test one kind of text only. The samples carry the brand's best-known line, "murder your thirst", and a model may recognise Liquid Death from it. The outputs are searched for the real name to catch that.

## Left out of the public repository

The public copy leaves out every file that holds these texts in full: `en.md`, `heldout.json`, `blind/`, the interview transcripts and the judge prompts. The voice files and the judge's answers quote a few sentences; the texts the models wrote are all there.
