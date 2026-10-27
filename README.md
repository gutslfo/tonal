# Tonal

A free kit that reads texts you wrote and turns them into a voice file: a text you give ChatGPT, Claude or Gemini so that what it writes for you sounds like your brand. In French, English and Spanish. It needs no account and no code, and the file it writes is yours.

## Use it

Open `kit/en/interview.txt` (or `kit/fr/`, `kit/es/`), copy all of it, and paste it into a new chat with ChatGPT, Claude or Gemini as your first message. It asks for three to five texts you wrote and like, and one you would hate to have written. It tells you what your texts do, then asks twelve questions at most, one per message, each with answers drafted from your texts. Pick one, correct one, or say "decide for me".

At the end it writes your voice file in two sizes, in plain text. The short one stays under 1,500 characters and goes where your assistant reads it in every chat. The full one stays under 8,000 and goes into a project or a skill, with your texts beside it. `kit/en/where-to-paste.md` gives the menus for each assistant, as their help pages showed them on 26 and 27 October 2026.

`site/index.html` holds the same kit as one page, with a copy button and a switch between the three languages.

## What is in the kit

Each language has its own folder in `kit/`, with the same five files:

- `interview.txt`, the prompt you paste. It carries both templates.
- `voice-short.txt` and `voice-full.txt`, the two templates the interview fills in, so you can read them before you start.
- `tells.md`, the AI tells the full file bans, each with a before and an after.
- `where-to-paste.md`, the setup for ChatGPT, Claude and Gemini.

No native speaker has read the Spanish version yet.

To measure a voice file you wrote or edited yourself: `python check.py short my-short.txt` or `python check.py full my-full.txt`. It counts characters the way a browser field does and fails over the limit.

## How it was made

`METHOD.md` lists every rule in the kit with its source and how much that source can be trusted. `test/RESULTS.md` has every test run, what it cost and where it falls short. There are two tests. Levain, a fictional bakery, was run in English on an earlier version of the kit, and in French and Spanish on the current one; the French LinkedIn text came back as a question, which fails the bar set before the run. The other, in English, used Liquid Death's published texts, renamed Grave Water so the models would not recognise the brand, with a second model judging the results blind. The brand's own texts are not in this repository; the texts the models wrote are.

The tests call the Claude API with your own key. `api.py` logs every call and its cost to `ledger.jsonl`, and refuses a call once the spend reaches its cap.

## Build and check

```
python kit/build.py       # assembles each interview.txt from its head and the two templates
python check.py           # every file against its limit, and each interview.txt up to date
python site/build.py      # the page
python site/carousel.py   # the LinkedIn PDF
python test/surfaces.py   # the page at 390 and 1440 px, and the copy button against the file
```

The last two drive a real browser through Playwright. `site/build.py` reads the Taykon colours and fonts from a folder outside this repository, so it will not run from a fresh copy. The page it built, `site/index.html`, is committed.

## Credits

The English tells come from the humanizer skill by blader ([github.com/blader/humanizer](https://github.com/blader/humanizer), MIT licence), which is built on Wikipedia's guide [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). The French ones also draw on French Wikipedia's guide [Identifier l'usage d'une IA générative](https://fr.wikipedia.org/wiki/Aide:Identifier_l%27usage_d%27une_IA_g%C3%A9n%C3%A9rative) and on Taykon Studio's own rules for French. The last tell, the version anyone would write, adapts StoryScope, a study of AI fiction (arXiv 2604.03136).

The Spanish tells come from a study made for this kit, in `research/es-study/`. It compares business texts written by two AI models with Spanish written by people before 2023, from the AuTexTification 2023 corpus (CC BY-NC-SA 4.0, so the corpus is not included here). The dash rule comes from the RAE's Diccionario panhispánico de dudas.

The page uses Overused Grotesk and Host Grotesk, both under the SIL Open Font License; the licence texts are in `site/fonts/`.

## Licence

MIT for the prompts and the scripts. Use the kit for your own brand or your clients' brands, or build on it; keep the copyright notice. The fonts keep their own licence, and the voice file you make with the kit belongs to you.

Made by Pierre Tran at [Taykon Studio](https://taykonstudio.com).
