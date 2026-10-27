# Test results, 26 October 2026

Levain is a fictional bakery. Sam, its founder, is played by claude-haiku-5-5 from a fact sheet (`test/levain/`). Nobody edited anything between the first message and the voice file.

## Two runs in English

The first run used a voice file with no job for each kind of text, and Levain's samples held nothing that sold. Its texts came out half as long as the ones written without the file, and Pierre read them as descriptive: the reason to come, to order or to write had gone out with the tells. The kit now has the interview settle the job and the shape of each kind of text (METHOD.md, I11 and V15 to V21), and Levain's samples now include the newsletter that brought in most of its Saturday orders. The second run, the same day, used that kit. The first run's files are in `test/v1/`.

The French and Spanish kits were changed the same way but not run again that day: both reruns together would have passed the $4 cap. Until the section "French and Spanish on the current kit", every French and Spanish figure is from the first kit.

## The interview

The prompt was pasted as the first message, with no system prompt, and the run stopped at the first message holding the full voice file.

| Run | Interviewer turns | Short file | Full file |
|---|---|---|---|
| Claude, English, second kit | 16 | 1,264 / 1,500 characters, 218 words | 6,581 / 8,000, 1,226 words |
| Claude, English, first kit | 16 | 1,349 / 1,500, 241 words | 5,673 / 8,000, 1,044 words |
| Claude, French, first kit | 17 | 1,252 / 1,500, 225 words | 6,318 / 8,000, 1,152 words |
| Claude, Spanish, first kit | 16 | 1,074 / 1,500, 177 words | 5,502 / 8,000, 966 words |
| Codex, English, first kit | 13 | 995 / 1,500, 163 words | 5,628 / 8,000, 932 words |

Sizes are from `python check.py short|full <file>`, which counts characters the way the platforms do (an emoji counts as two). All ten files fit.

In the second run the interviewer drafted each job from what Levain's samples ask of their readers: the website "tells how the bread is made and when the rye is ready", the newsletter "sells the Saturday rye, so the reader orders on the website and a loaf waits at the counter with their name on it", an email says "what happens next and whom to ask". Levain has no LinkedIn sample, so the file reads "LinkedIn: not written for now. If I ask for a LinkedIn post, ask me for its job first."

In the first run Claude's last turn ran out of tokens at 8,000 in all three languages, because it thinks through both files before writing them. The limit was raised to 16,000 and the same call was sent again from the saved transcript. The second run fit in 16,000.

Codex stands in for ChatGPT: the Codex CLI on gpt-6-astra, through Pierre's ChatGPT account, in one thread resumed turn by turn. Its event log holds 26 messages and no command or file read. Pierre's global `~/.codex/AGENTS.md` loads in every Codex session. The sentence case and the ban on italics in its file come from the founder sheet, not from AGENTS.md. ChatGPT itself, in the browser, was not tested.

Codex wrote its header as "Voice file for Levain" rather than in capitals, so the test missed the end. The two models then traded thanks for 12 more turns until Codex sent an empty reply and the founder call failed. The detector now ignores case, and the files are taken from turn 13, where the interview ended. In turn 14 Codex wrote a revised file after a remark from the founder; that version is not used.

The scripted founder is fussier than a real one, and it sometimes talked about "the brief" or "the facts". Both interviewers answered that they had seen no brief and asked for the texts.

## Five tasks, with and without the file

Five requests per language, each sent twice to claude-sonnet-5-5: once with the Claude voice file as the system prompt, once with nothing. The texts are in `test/tasks/`. The texts without the file do not depend on the kit, so both English runs share them.

`test/scan.py` counts what a script can see (`test/scan.md` has every row):

| | English, second kit | English, first kit | French | Spanish |
|---|---|---|---|---|
| Tells without the file | 15 | 15 | 25 | 27 |
| Tells with the file | 0 | 0 | 0 | 0 |
| Words without / with | 496 / 310 | 496 / 259 | 512 / 184 | 616 / 231 |

Emoji and hashtags account for most of the count. The scan cannot see invented facts or a lost job, so every text was read by hand.

With the second file the LinkedIn request first came back as a question: "Before I write it, I need the job of this post." The request already said that interested businesses can write to hello@levain.example, so the question was not needed, and the rule the interview wrote is stricter than it should be. The founder's one-line answer went back as a second turn ("Its job: cafés and restaurants near Mill Lane write to hello@levain.example if they want our bread."), and the post is from that turn. The question is in `test/tasks/en/linkedin-with-question.txt`.

### Read by hand

Without the file, the English and French replies say forty loaves "each week" (« par semaine »), a unit no request gave; the page request says forty a day. Other texts added things that were never given: pastries and local delivery in the French LinkedIn post, "for years" in the English one, soups and stews in the Spanish newsletter. All nine page, Instagram and newsletter texts praised the taste, the crust or the crumb.

With the second English file, each text keeps the job its kind of text has. The newsletter gives the news, then what it changes for the reader: "so you no longer have to come in the morning". The reply says sorry once, gives the reason, then the way to make sure of a loaf ("a loaf will wait at the counter with your name on it") and whom to ring. The LinkedIn post opens on the news and ends on the address to write to. The caption says what and when in its first line.

Three things the second file got wrong. The about page's "the next bake is for the day after tomorrow" comes back in the page, the caption and the reply, where it contradicts forty loaves a day and a rye baked for Saturday: the file states it as a rule, and the model repeats it. The LinkedIn post adds "so each bake is planned two days ahead", which is in neither the request nor the file. And the page without the file ends on an invitation ("Come to Levain at 3 Mill Lane early, because when they're gone, they're gone"), where the page with it ends on "You can collect from us at 3 Mill Lane."

With the first files, two sentences added something that is in neither the request nor the file: "so the crumb is set by the time we bake" (English page) and « El resto del pan sigue como estaba » (Spanish newsletter). The Spanish reply signs « [Tu nombre] », because the Spanish file says the person who answers signs but never names Sam.

## Blind pairs

The five English pairs in `test/blind/pairs.md` are from the second run, in random order, with the request above each pair. Picks go in `picks.md` before `key.json` is opened. They are Pierre's to make, and not made yet. The first run's pairs were never picked; they are in `test/v1/blind/`. The results PDF prints each pair with its label, so picks made after reading it are not blind.

## A real brand: Liquid Death, as Grave Water

Levain shows that the file removes tells, but Levain's voice was written by us, so nothing could say whether a text sounded like it. This test uses a brand with its own published texts and checks the result against them. Liquid Death's copy is in `test/liquid-death/`, with every source and date in `SOURCES.md`. The brand is renamed Grave Water throughout, because the writing model knows Liquid Death and a Tonal user's brand is one it has never read about.

Four real texts went to the founder (`en.md`): the about page, four FAQ answers, a drink page and four merch descriptions. The founder could answer only from them or say "decide for me", and it corrected the interviewer in 11 of its 16 replies. The voice file came after 17 turns, 1,334 words. Six product descriptions created between 13 July and 18 August 2026, after the writing model's training, were held back. Each became a neutral request with the facts only, and each request was written four ways by claude-sonnet-5-5:

- none: the request alone;
- line: the founder's own description in one line, "dark, deadpan humor that jokes about death and murder while promoting healthy, low-sugar drinks";
- samples: the four real texts pasted, with "Write in the same voice";
- file: the voice file.

A GPT judge (gpt-6-astra through Codex) ranked them twice, shuffled afresh each time. "Close" shows the real text and asks which of the four comes closest to its voice. "Spot" shows the brand's four sample texts and five candidates, the real one among them, and asks which the brand wrote. The scores are in `judge/scores.md`, and the prompts and raw answers sit beside them.

| | Close: mean rank of 4 | Close: ranked first | Spot: mean rank of 5 | Words against the real text, median |
|---|---|---|---|---|
| none | 3.08 | 2 of 12 | 4.58 | 4.0 times |
| line | 3.00 | 0 of 12 | 3.83 | 7.2 times |
| samples | 1.58 | 9 of 12 | 2.08 | 2.9 times |
| file | 2.33 | 1 of 12 | 3.50 | 3.2 times |

The judge found the real text in all 12 spot rounds: no version passed for the brand. Character trigrams put all four between 0.48 and 0.51 of the real text, so that measure separates nothing and is left out of the verdict.

The file beats no instructions and the founder's one line on both measures. Pasting the four texts beats the file on both: by the same margin as the file beats no instructions on "close" (0.75 of a rank), and by more on "spot" (1.42 against 1.08). On this test, the whole interview does worse than a paste of four texts.

### Read by hand

The real texts are one paragraph of 30 to 60 words that opens on the joke. Without the file, the texts carry bold titles, bullet lists and a slogan to close. With the one line, they add more of everything, up to 266 words, with jokes down to the bullet points. With the samples, they keep one to three paragraphs and no markdown, and the kind of joke the brand makes ("so every sip is a firm handshake with the dead").

With the file, three of its own rules pull every text away from the brand:
- "Put what the reader came for in the first sentence" makes each one open on the facts restated ("The Mug of Doom is a tankard-style mug in antique silver"), where the brand opens on the joke.
- "Every text has a job" ends five of the six on "add it to your cart". In the real six, only the mittens close on a call to buy, and there it is the joke ("Buy these limited edition mittens now or die a horrible death. Your call.").
- "Specs stay plain and exact", learned from the drink page, adds a spec list to four of the five merch texts. No real merch text has one.

The file also bans "clean" as a wellness word, and the brand's own energy text says "a clean refreshing taste". On that item the judge ranked the text without instructions closest, both times: the real energy text barely jokes.

What this says about the kit: the file's general rules about shape outweighed what the samples showed, and the samples themselves carried the voice better than the file's description of it. That points at two changes: the file could carry the founder's best texts word for word, and the shape rules could yield to what those texts do. The kit's own guide already asks for something close to the first, which the next part tests. The second has not been made.

### The kit as its guide sets it up

`kit/en/where-to-paste.md` tells ChatGPT and Claude users to add their sample texts to the project, next to the full file. The four ways above gave the model the file alone, which is not how the kit is meant to be used. A fifth way, kit, gives it the file, then the four texts as a project file. The judge ran twice more with all five, shuffled afresh (`judge/scores-3-4.md`):

| | Close: mean rank of 5 | Close: ranked first | Spot: mean rank of 6 | Words against the real text, median |
|---|---|---|---|---|
| none | 3.83 | 2 of 12 | 5.75 | 4.0 times |
| line | 4.33 | 0 of 12 | 4.92 | 7.2 times |
| samples | 2.33 | 4 of 12 | 2.92 | 2.9 times |
| file | 2.92 | 1 of 12 | 4.00 | 3.2 times |
| kit | 1.58 | 5 of 12 | 2.42 | 2.8 times |

The kit comes first on both measures, ahead of the pasted texts by 0.75 of a rank on "close" and 0.50 on "spot". The other four keep the order they had in runs 1 and 2. The judge again found the real text in all 12 spot rounds.

Read by hand, the kit texts still have the file's shape. All six open on the product and its facts, four of the five merch texts carry a spec list (in Title Case on two of them), and they run 2.8 times as long as the real ones. Three of the six end on a call to buy, against five of six with the file alone. So the texts beside the file soften its rules without overturning them, and the judge's preference does not mean the kit writes like the brand: no version passed for the brand's own.

On this test the kit works best the way its guide says to set it up, and better than a paste of four texts. Two things follow. The guide gave Gemini users no place for their texts: the skill held the full file only. Since 27 October the texts go below the file, in the skill's instructions. And the shape rules could yield to the founder's texts, which the next part tests.

### Shape rules that yield to the founder's texts

The English kit was changed on 26 October (commit 03e9405): the interview now settles each kind of text's shape (how it opens, how long it runs, how it ends, whether it has a list) from the founder's texts when they show that kind. The file says the template's shape rules apply only to the kinds the texts do not show, and "our texts win" now covers shape. The interview ran again on Grave Water with the same founder (`interview-2/`, 17 turns, 7,162 of 8,000 characters). The new file splits the shop page in two, a drink page with its spec list and a merch page with "no fixed opener. It ends on a joke or a spec."

The six requests were written with the new file alone (file-2) and with the file and the texts (kit-2). The judge ran twice on five of them, the three best from before and the two new (`judge/scores-5-6.md`):

| | Close: mean rank of 5 | Close: ranked first | Spot: mean rank of 6 | Words against the real text, median |
|---|---|---|---|---|
| samples | 3.33 | 1 of 12 | 3.75 | 2.9 times |
| file | 3.67 | 2 of 12 | 4.58 | 3.2 times |
| kit | 2.25 | 4 of 12 | 3.25 | 2.8 times |
| file-2 | 3.17 | 0 of 12 | 5.25 | 2.4 times |
| kit-2 | 2.58 | 5 of 12 | 3.17 | 1.3 times |

Overall, kit-2 ties kit. By hand, the change did what it was for: three of the six kit-2 texts and four of the six file-2 texts open on the joke ("Your hands will die someday."), where no kit text did; no kit-2 merch text ends on a call to buy; and kit-2 runs 1.3 times the real length, against 2.8 for kit.

It also brought a new failure. The new file gives the merch page a job that includes "what it costs in time or money", and the template's facts rule says "If a price, a date or a name is missing, ask me for it". None of the six requests gave a price, so seven of the ten new merch texts carry a price placeholder, and four end on a note to the user ("I need the price before this can go live"). Split by that, on the four products where kit-2 wrote a finished text it ranks 1.62 on "close" and 2.00 on "spot", against 2.62 and 3.75 for kit. On the two where it asked for the price, it falls to 4.50 and 5.50. The split was made after reading the texts, on four products and two runs, so it shows where the loss comes from rather than proving the gain.

### A facts rule that asks only for what the text needs, and the last test

The facts rule was changed on 26 October (commit b73f981): "Never make up a price, a date or a name. Ask me for one only if the text cannot do its job without it; otherwise write the text without it." The short file got the same rule. The pass bar was written in that commit before the run, with Pierre's approval: the new kit (kit-3, its file plus the four texts) passes if its mean rank beats kit's on both "close" and "spot", and no kit-3 text carries a placeholder or a note to the user. Pass: ship this kit. Fail: ship the kit of runs 3 and 4. Testing stops either way.

The interview ran a third time on Grave Water (`interview-3/`, 17 turns, 6,785 of 8,000 characters). Its last turn first stopped at the 16,000-token limit before writing anything; it was sent again unchanged with a 32,000-token limit and used 28,694. The judge ran twice on the five ways (`judge/scores-7-8.md`):

| | Close: mean rank of 5 | Close: ranked first | Spot: mean rank of 6 | Words against the real text, median |
|---|---|---|---|---|
| samples | 3.83 | 0 of 12 | 4.92 | 2.9 times |
| file | 4.08 | 0 of 12 | 5.25 | 3.2 times |
| kit | 2.75 | 1 of 12 | 3.83 | 2.8 times |
| kit-2 | 2.92 | 4 of 12 | 3.50 | 1.3 times |
| kit-3 | 1.42 | 7 of 12 | 2.50 | 1.8 times |

kit-3 passes: 1.42 against 2.75 on "close", 2.50 against 3.83 on "spot", and none of the six texts carries a placeholder or a note, read by hand. The English kit as it stands after b73f981 is the one to ship. The judge still found the real text in all 12 spot rounds.

Read by hand, all six open on the joke and run one paragraph of 39 to 66 words. The energy text says "clean and refreshing", the brand's own words, which the first two files banned and the third does not. Two flaws: three of the six open on "Yes.", a move the brand makes once in its samples, and the tee text never names the Teenage Shirtbag Tee, which the request gave.

French and Spanish got the same two changes on 27 October (commit 60b90f1) and ran on Levain the same day (below).

Limits: six texts of one kind (merch descriptions) from one shop, eight judge runs, one judge model, one founder played by a model. The pass bar was met once, in two runs. The four samples carry "murder your thirst", which a model may recognise; the real name appears in none of the 48 texts.

Pierre's blind picks: `test/liquid-death/blind/texts.md` holds the five texts per product in random order. It was made before the kit texts and does not include them. The picks are to be made before this section is read, and are not made yet. The chat already said that the file versions open on the facts and end on the cart, so the picks are not fully blind.

## French and Spanish on the current kit

The French and Spanish kits as changed on 27 October (commit 60b90f1) run on Levain the way the English one did: the interview with the same founder sheets, then the five requests with and without the full file, the file alone in the system prompt as before. The earlier French and Spanish run moves to `test/v1/`.

The bar, set in this commit before the run, with Pierre's go. Per language, the run passes if the interview reaches the voice file with no human edit; `check.py` passes both files; `scan.py` finds no more tells with the file than without; and no text written with the file carries a placeholder, a note to the user, or a question in place of the text. Invented facts are read by hand and reported, not scored. Pass or fail, the page shows these texts, and a failure is stated beside them.

Spanish passes. French fails on the last criterion: its LinkedIn text is a question.

| Run | Interviewer turns | Short file | Full file |
|---|---|---|---|
| Claude, French, current kit | 16 | 1,292 / 1,500 characters, 231 words | 7,331 / 8,000, 1,353 words |
| Claude, Spanish, current kit | 15 | 1,305 / 1,500, 227 words | 6,731 / 8,000, 1,197 words |

Both interviews reached the voice file with no human edit. The last turn fit in 32,000 tokens, the French one with 30,520 used. The French file ends on a code fence and the Spanish one on « ----- fin ----- », so `extract.py` now stops at both.

| | French | Spanish |
|---|---|---|
| Tells without the file | 18 | 26 |
| Tells with the file | 0 | 0 |
| Words without / with | 553 / 277 | 596 / 293 |

Without the file, the French count is 3 stock phrases, 3 emoji and 12 hashtags; the Spanish one is 4 words from the kit list, 1 stock phrase, 6 emoji, 12 hashtags and 3 bold. The texts without the file were written again too, so the counts differ from the first run's 25 and 27.

The French LinkedIn text, in full, is in `test/tasks/fr/linkedin-with.txt`. It opens « Avant d'écrire pour LinkedIn, j'ai une question : nos textes n'en montrent aucun et nous n'y sommes pas, d'après mon fichier de voix. Ma consigne est de vous demander d'abord. », asks whether the post comes from a Levain page or a personal account, and offers to write it at once in the plain form. The file told it to ask. In the interview the interviewer offered three answers for LinkedIn, and the founder, played by the model, took the third: « LinkedIn n'est pas un canal pour Levain : nous n'y sommes pas », which the founder sheet does not say. The file then reads « Avant d'écrire quoi que ce soit pour LinkedIn, demande-moi », against its own facts rule, which asks only for what the text cannot do without. The second English run asked the same way (above). The French file says the same of the newsletter, and the newsletter was written, since the request names the November newsletter.

Read by hand, with the file. In French, the page, the caption, the reply and the newsletter hold nothing beyond the request and the founder's own texts, with two details. The page repeats « puis nous recommençons pour après-demain » from the about page beside forty loaves a day, as the second English file did. The reply puts « Si la commande ne passe pas » before the founder's « appelez la boutique et demandez-moi ». In Spanish, the page times the two feedings « por la mañana y por la tarde », which neither the request nor the file gives, and ties forty loaves to the two days with « Por eso ». The LinkedIn post says « Nuestro pan tarda días en hacerse » where only the rye was said to take two days, and promises « te diremos qué día se hornea cada pan y cuántos hay », which nobody gave. The caption, the reply and the newsletter are clean; « te lo apartamos » in the reply reads ordering for Saturday as setting a loaf aside.

Without the file, the texts invent taste and method: « un caractère franc et légèrement acidulé » and a levain fed « matin et soir » in the French page, « sabor profundo » in the Spanish one, forty loaves « cada semana » in the Spanish reply. Both LinkedIn posts carry emoji, hashtags and self-praise (« vraie relation de confiance », « mucho cariño por el oficio »).

Against the first kit (`test/v1/`), the Spanish reply now signs Sam instead of « [Tu nombre] », and « El resto del pan sigue como estaba » is gone from the newsletter. The texts with the file run 277 and 293 words, against 184 and 231 with the first files.

## Not done

No native speaker has read the Spanish kit or the Spanish results. The French and Spanish kits ran on Levain only, not on a real brand. The French LinkedIn rule that failed is unchanged.

## Cost

$7.38 in API calls. The French and Spanish run on the current kit cost $1.71: $0.87 for the French interview, $0.68 for the Spanish one, both founders included, and $0.16 for the twenty texts. The Liquid Death test cost $2.83. The first interview cost $0.58 and its 36 texts $0.30: six were written twice because the first one-line condition carried the founder's refusal around its description (`oneline-raw.txt`), and the six kit texts cost $0.10. The second interview cost $0.56 and its 12 texts $0.18. The third cost $1.13, $0.19 of it for the last turn cut at 16,000 tokens, and its six texts $0.08. Before it, $2.84. The first run cost $2.29, including a $0.33 estimate for three calls cut off before the log recorded them; the brief estimated under $2, and the gap is the interviewer's thinking on the last turn. The second English run cost $0.55: $0.49 for the interview, $0.06 for the five texts and the LinkedIn answer. The stop was at $4; Pierre raised it to $5 and $5.50 on 26 October, to $5.75 on 27 October for the reruns, and to $8.25 the same day for the French and Spanish run. Codex ran on Pierre's ChatGPT plan and is not in the ledger.
