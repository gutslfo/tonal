# Tonal, method

Tonal turns a founder's own texts into a voice file an AI assistant follows. This file holds every rule the kit uses, where it comes from and how much weight it carries. A rule that is not here is not in the kit.

Written 26 October 2026.

## Grades

| grade | means |
|---|---|
| A | The platform's own documentation, or the authority on the language (RAE). Read on the date given. |
| B | Established guidance written and maintained by practitioners: Wikipedia's editors' guides on AI writing, the Mailchimp content style guide, the humanizer skill built on them. |
| C | A vendor blog or an informal list. Used only when something above confirms it, or labelled as a lead. |
| H | A house rule: Taykon's own practice, carried over from the Brand Book interview or from Pierre's voice file. Kept because it worked there, not because anyone proved it. |
| M | Measured in this repository, on a small sample. The numbers and their limits are in `research/`. |

## Sources

- **humanizer**: `~/.claude/skills/humanizer/SKILL.md`, patterns 1 to 40. Patterns 1 to 33 come from [blader/humanizer](https://github.com/blader/humanizer) (MIT), itself built on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Patterns 34 to 36 adapt StoryScope (arXiv 2604.03136, a fiction study). Patterns 37 to 40 are Taykon additions (H).
- **WP-fr**: French Wikipedia's own guide, [Aide:Identifier l'usage d'une IA générative](https://fr.wikipedia.org/wiki/Aide:Identifier_l%27usage_d%27une_IA_g%C3%A9n%C3%A9rative), read 26.10.2026. Spanish Wikipedia has no equivalent: the English page links to eight languages (German, Finnish, French, Hebrew, Portuguese, Russian, Thai, Chinese) and not to Spanish (Wikipedia API, 26.10.2026).
- **Mailchimp**: [Content Style Guide, Voice and Tone](https://styleguide.mailchimp.com/voice-and-tone/), [Writing Goals and Principles](https://styleguide.mailchimp.com/writing-principles/) and [Writing Email Newsletters](https://styleguide.mailchimp.com/writing-email-newsletters/), read 26.10.2026.
- **NN/g**: Amy Schade, [Inverted Pyramid: Writing for Comprehension](https://www.nngroup.com/articles/inverted-pyramid/), Nielsen Norman Group, 11 February 2018.
- **LinkedIn**: [Best Practices for Sponsored Content](https://www.linkedin.com/help/lms/answer/39571) (Marketing Solutions Help) and [LinkedIn Pages Best Practices](https://business.linkedin.com/marketing-solutions/linkedin-pages/best-practices), read 26.10.2026.
- **Instagram**: the @creators announcement on Threads that captions take five hashtags at most, read through [Social Media Today](https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/) (Andrew Hutchinson, 18 December 2025). Where the feed folds a caption or a post is not published by either platform; the figures in circulation (about 125 characters on Instagram, about three lines on LinkedIn) are measurements by tool makers.
- **HBR**: ["Sorry" Is Not Enough](https://hbr.org/2018/01/sorry-is-not-enough), Harvard Business Review, January and February 2018 issue, and the IdeaCast episode "For Better Customer Service, Offer Options, Not Apologies". Read as the summary page; the study's method is behind the paywall.
- **Glean**: [How to create a brand voice guide for AI tools](https://www.glean.com/perspectives/how-to-create-a-brand-voice-guide-for-ai-tools), a vendor blog dated 1 June 2026.
- **Brand Book**: `Tools/Brand Book/references/interview.md`, `intake.md`, `canon.md` section 6. The interview that produced the Levain brand book.
- **voice-pierre**: `~/.claude/skills/humanizer/voice-pierre.md`, a voice file drawn from real samples. The model for the full file's structure.
- **ES study**: `research/es-study/results.md`. 60 Spanish texts from two models against a million words of pre-2023 human Spanish.
- **Platforms**: `research/platforms-2026-10-26.md`, the help pages of ChatGPT, Claude and Gemini read on build day.
- **RAE**: [Diccionario panhispánico de dudas](https://www.rae.es/dpd/), read 26.10.2026.

## How a voice is drawn from samples

The founder's own texts are the material, not their description of themselves. Adjectives ("warm", "bold", "friendly") describe every brand and constrain no model; a sample shows sentence length, person, what gets named, what never gets claimed. So the interview asks for texts first, reads them, and only then asks questions, each one proposing answers drawn from what the texts already do. The founder confirms or corrects. The voice file then states the voice as behaviours a reader could check on any paragraph, gives the AI three pairs built from the founder's own sentences, and ends with a check the AI runs on its own draft.

The one text the founder would hate to have written does as much work as the five they like: it shows the edge of the voice, which a list of liked texts cannot.

## Rules for the interview

| ID | rule | source | grade |
|---|---|---|---|
| I1 | Ask for three to five texts the founder wrote and likes, and one text, theirs or anyone's, they would hate to have written. Before any question. | Brief; Glean ("annotated samples"); humanizer Voice Calibration (a sample outranks the rules) | H, C, B |
| I2 | One question per message. | Brand Book interview.md | H |
| I3 | Each question comes with two to four drafted answers, the recommended one first, written from the founder's samples. "Decide for me" is a valid answer. | Brand Book interview.md | H |
| I4 | Say which part of the voice file each question shapes. | Brand Book interview.md | H |
| I5 | Every five questions, a short running summary of what has been decided. | Brand Book interview.md | H |
| I6 | About fifteen minutes: twelve questions at most after the samples. | Brief | H |
| I7 | Answer in the founder's language; write the voice file in it. | Brief | H |
| I8 | Draft answers from what is specific in the samples, never the answer any brand would give. | humanizer 36 (convergence on the obvious version) | B |
| I9 | Never add a fact the founder did not give: no figure, award, year or customer. A gap is a question, not a guess. | humanizer Process ("does the rewrite invent facts"), 5, 21 | B |
| I11 | Settle the job and the shape of each kind of text: what the reader should do or feel after reading, and how the text opens, how long it runs, how it ends, whether it has a list. Draft the job from what the samples already ask of their readers; take the shape from the samples when they show that kind of text. | Mailchimp ("Before you start writing, ask yourself: What purpose does this serve?"); M, step 3: with the first version of the file, the texts were half as long and Pierre read them as descriptive, their marketing job lost (26.10.2026); M, Grave Water test (V11) | B, M |
| I10 | Budget the two files in words as well as characters, and show the count: about 200 words for the short file, about 1,100 for the full one. The founder checks the count where the field shows it. | Platforms (ChatGPT's 1,500-character field); M, step 3 measures whether the model holds it | A, M |

## Rules for the voice file

| ID | rule | where it lands | source | grade |
|---|---|---|---|---|
| V1 | Two sizes: short, 1,500 characters at most, for every custom-instructions field including free ChatGPT; full, 8,000 at most. | Both files | Platforms (ChatGPT Free and Go: 1,500); 8,000 is Tonal's own cap, no platform publishes one for projects or skills | A, H |
| V2 | Plain text. No markdown, no headings with symbols, so it pastes into any field unchanged. | Both files | Taykon practice: the same file has to survive four different fields | H |
| V3 | Name who the brand writes for, concretely: who they are, what they already know, what they come for. | Full: "Who we write for" | Glean (voice, tone and audience kept separate) | C |
| V4 | State the voice as four to six behaviours a reader could check: sentence length, person (we, I, the brand's name), form of address, what the brand names, what it never claims. No adjectives without a behaviour. | Both files | Glean (observable behaviours over adjectives); voice-pierre (each rule proved by a verbatim line) | C, H |
| V5 | Write the voice as pairs, "X but not Y". | Full: "The voice" | Mailchimp ("weird but not inappropriate, smart but not snobbish"); Brand Book canon section 6 | B, H |
| V6 | The voice stays, the tone and the shape move by kind of text: website, newsletter, email to one person, Instagram, LinkedIn, customer reply. | Full: "Each kind of text" | Mailchimp ("You have the same voice all the time, but your tone changes."); Glean (tone per scenario) | B, C |
| V7 | Clear before clever. | Full: "The voice" | Mailchimp ("it's always more important to be clear than entertaining") | B |
| V8 | Fix the form of address and the variety of the language: you; tu or vous; tú, usted or vos, and the country. | Both files | humanizer 39 (tutoiement or vouvoiement checked, not guessed); ES study (Claude used usted in four replies of six, tú in two, with nothing to decide it) | B, M |
| V9 | Words the brand never uses: its own list, then the AI tells for its language, from the tells list. | Both files (short: the five that matter most) | Glean (preferred, banned, use sparingly); humanizer 7, 37; ES study | C, B, M |
| V10 | Three annotated pairs, "write this, not this", built from the founder's samples: the line from their text, the generic line a model would write instead, and one clause saying what the difference is. | Full: "Write this, not this" | Glean (annotated samples, rewrite examples); humanizer before and after method; voice-pierre (verbatim proof) | C, B, H |
| V11 | The founder's samples outrank the tells list and the shape rules: if they use a dash, a list of three or an emoji, the file keeps it at their frequency, and a kind of text they show takes its shape from them. | Full: "Each kind of text", "When this file and our texts disagree" | humanizer Voice Calibration; M, Grave Water test (`test/RESULTS.md`, 26 and 27.10.2026): with the shape rules over the samples, every text opened on the facts and ran about three times the brand's length; with the samples' shape, the kit passed a bar set before the run | B, M |
| V12 | Match the format to where the text goes: no markdown on Instagram or LinkedIn (asterisks print as asterisks), no headings in a reply, hashtags only if the brand uses them, no emoji at the head of lines unless the samples do it. | Full: "Tone by channel" | humanizer 15, 18, 39; ES study (markdown bold in 5 of 30 Claude texts, a hashtag block under all 6 Claude LinkedIn posts) | B, M |
| V13 | Never invent facts: the AI writes only what the brief or the founder's material holds, and asks only for a fact the text cannot do its job without; otherwise it writes without it. | Both files | humanizer Process, 5, 21; M, Grave Water test (`test/RESULTS.md`): told to ask for any missing price, the AI put a price placeholder in seven of ten product texts that needed none | B, M |
| V14 | End with a check the AI runs on its draft before answering: the banned words, the tells, the form of address, the shape for the kind of text, whether it still does its job, one question ("could any other brand have written this?"). | Both files (short: one line) | Glean (rubric); humanizer Process ("what makes this obviously AI"); humanizer 36; V15 | C, B |
| V15 | Every text has a job. Keep the reason to act and carry it with facts, never with praise. Shorter is not better when the text stops doing its job. | Both files | Mailchimp ("every word we say informs and encourages"; "What purpose does this serve?"); M, step 3 (see I11) | B, M |
| V16 | Website: what the reader came for goes in the first sentence. | Full: "Each kind of text" | NN/g ("Readers can stop reading at any point on the page and still come away with the main point.") | B |
| V17 | Newsletter: the news first, one purpose per email, ending on the one next step with its link. | Full: "Each kind of text" | Mailchimp newsletters ("Put the most important information first." "Write with a clear purpose." "Make the reader's next step obvious, and close each campaign with a call to action." "Limit links to the most important resources.") | B |
| V18 | Email to one person: say what happens next and whom to contact. | Full: "Each kind of text" | Mailchimp newsletters ("Make the next step clear"), carried over to a single reader; Levain's own email | B, H |
| V19 | Instagram: the reason to stop goes in the first line; hashtags none, or five at most; end on what to do when there is something to do. | Full: "Each kind of text" | Instagram (five hashtags, "fewer, more targeted hashtags"); the fold is a tool makers' measurement | A, C |
| V20 | LinkedIn: the news or a question in the first two lines; the reader addressed as "you"; hashtags none, or three to five; end on the next step. | Full: "Each kind of text" | LinkedIn ("relevant, short, and authentic"; "Start with a question or quote to hook the reader and use 'You' to speak to your audience"; "Identify 3-5 hashtags ... add them to your posts when relevant"); the fold is a tool makers' measurement; the closing step from V17 | A, C, B |
| V21 | Reply to an unhappy customer: sorry once, at the start, for what went wrong; then what is being done and when, a choice when there is one, a person to contact. | Full: "Each kind of text" | HBR ("An apology that extends beyond the first seconds of an interaction can reduce customer satisfaction"; satisfaction follows visible effort to solve the problem; offer options) | B |

V16 to V21 give the shape of a kind of text the founder's samples do not show, and never its words. The words always come from the samples, and so does the shape of every kind of text they show (V11): a brand that never uses hashtags keeps none on LinkedIn, and a brand whose product pages open on a joke keeps that opening.

## The AI tells list

Readable in five minutes: the reflexes that show up in brand copy, each with one before and after. Each after keeps what the before was for, whether that is bringing people in, selling or reassuring, and says it with the facts the before holds. A line with no fact behind it gets no rewrite: the after says which fact to give the AI. (V15; the first version cut every after to its shortest form, and Pierre read the results as bland, 26.10.2026.) Patterns about encyclopedia articles (notability, "challenges and future prospects", knowledge-cutoff disclaimers) are left out: a founder does not write those.

### English, from the humanizer (B)

| ID | tell | humanizer |
|---|---|---|
| EN1 | Puffing up significance: "stands as a testament", "a pivotal moment", "deeply rooted" | 1 |
| EN2 | Brochure words: nestled, in the heart of, vibrant, rich, boasts, stunning, must-visit | 4 |
| EN3 | The AI word list: delve, tapestry, landscape, crucial, pivotal, enhance, foster, showcase | 7 |
| EN4 | "Not just X, it's Y", and the clipped tail ("no guessing") | 9 |
| EN5 | Everything in threes | 10, 40 |
| EN6 | The em dash used as punctuation | 14 |
| EN7 | Bold, emoji and chat formatting pasted into copy | 15, 18, 39 |
| EN8 | Chat leftovers: "I hope this helps", "Here's a…", "Let me know if…" | 20 |
| EN9 | Servile customer replies: "Great question!", "We sincerely apologize for any inconvenience" | 22 |
| EN10 | The upbeat send-off: "Exciting times ahead", "We can't wait to see you" | 25 |
| EN11 | Staccato drama and aphorisms: "No shortcuts. No compromises. Just bread." | 31, 32 |
| EN12 | Fake-candid openers: "Honestly?", "Here's the thing" | 33 |
| EN13 | The version anyone would write: nothing in it only this brand could say | 36 |

### French, from the humanizer and French Wikipedia (B, H)

| ID | tell | source |
|---|---|---|
| FR1 | Le vocabulaire de brochure : au cœur de, niché, véritable, incontournable, authentique, chaleureux, convivial, univers, expérience | humanizer 37; WP-fr ("ton promotionnel", "emphase excessive") |
| FR2 | « Allier tradition et modernité », « mettre un point d'honneur à » | humanizer 37 |
| FR3 | L'échelle de connecteurs : De plus, Par ailleurs, En outre, Enfin, En conclusion | humanizer 37 |
| FR4 | Les participes en cascade : permettant, offrant, garantissant | humanizer 37 (twin of 3) |
| FR5 | « Non seulement… mais également », « ce n'est pas X, c'est Y » | humanizer 37, 9 |
| FR6 | Tout par trois, et les listes sans « et » | humanizer 10, 40 (H) |
| FR7 | Le tiret cadratin comme ponctuation | humanizer 14 |
| FR8 | Gras, émojis, majuscules à chaque mot d'un titre | humanizer 15, 17, 18; WP-fr ("majuscules superflues dans les titres", « **mot** ») |
| FR9 | « N'hésitez pas à nous contacter », « Au plaisir de vous accueillir » | humanizer 37, 25 |
| FR10 | La réponse client servile : « Nous sommes sincèrement désolés pour la gêne occasionnée » | humanizer 22 |
| FR11 | La formule creuse, la langue de bois | WP-fr ("stéréotypes, phrases creuses ou superficielles", « langue de bois ») |
| FR12 | La version que tout le monde écrirait | humanizer 36 |

### Spanish, from the study (M) and the RAE (A)

Every Spanish tell below was measured in `research/es-study/` and confirmed by a second signal. None is translated from the English list; the translated lists that circulate in Spanish were tested and failed (46 of 48 items never appear in 60 model texts).

| ID | tell | evidence |
|---|---|---|
| ES1 | *En el corazón de* + lugar | 5.0 per 10k words against 0.1 human; humanizer 4, 37 |
| ES2 | *No es X, es Y* / *No fue X. Fue Y.* | 5.4 per 10k (Claude) against at most 0.6 human; humanizer 9; Borja Girón 2026 |
| ES3 | Todo de tres en tres: *con barro, paciencia y las manos* | 31 to 40 per 10k against 5 to 17 human; humanizer 10 |
| ES4 | *Artesanal*, *artesanía* | 5.0 against 0.3; humanizer 37 |
| ES5 | Fórmulas de atención al cliente: *lamento las molestias*, *entiendo que*, *Estimado/a cliente*, *Un cordial saludo* | *lamento* 11.2 against 0.1; humanizer 22 |
| ES6 | La declaración de valores: *porque creemos que*, *sabemos que* | 6.2 and 5.0 against 0.1; humanizer 1, 27 |
| ES7 | El cierre de invitación: *te esperamos*, *¡Nos vemos en…!* | 5.0 against 0.0; humanizer 25 |
| ES8 | Formato de chat pegado: emojis al inicio de línea, `**negritas**`, bloque de hashtags, listas con flechas | 9 of 30 texts with emoji, 5 with `**`; humanizer 15, 18, 39 |
| ES9 | Frases sentencia y golpes cortos: *Nada se pierde del todo. Se reubica.* | read in the LinkedIn samples; humanizer 31, 32; Borja Girón |
| ES10 | La raya que gira la frase a la inglesa, sin raya de cierre | RAE, DPD "raya": the closing raya of an aside is never dropped (A). Rare in the sample (M) |
| ES11 | La versión que cualquiera escribiría | humanizer 36 |

Not in the Spanish list, because the counts did not support them: the gerund tail (the models used it less than human writers), Title Case headings (not seen), and the translated vocabulary (*tapiz*, *testimonio*, *sumérgete*). See `research/es-study/results.md`.

The Spanish tells were measured by a non-native reader and have not been read by a native speaker. The kit says so wherever it shows them.

## Where to paste it

| ID | rule | source | grade |
|---|---|---|---|
| P1 | ChatGPT, short file: Settings, Personalization (web) or Customize ChatGPT (mobile), Custom Instructions. 1,500 characters on Free and Go, 5,000 on paid plans. | Platforms | A |
| P2 | ChatGPT, full file: a project, ••• then Project settings, instructions. Project instructions override the account's custom instructions. No published limit. | Platforms | A |
| P3 | Custom GPTs are closed to new creation on personal accounts and are being retired. The kit does not send anyone there. | Platforms | A |
| P4 | Claude, short file: Settings, Your Claude, Instructions. Full file: a project, Set project instructions. Projects are open to free accounts (five at most). | Platforms | A |
| P5 | Claude Styles: the help page is gone (404). The kit does not send anyone there. | Platforms | A |
| P6 | Gemini, full file: a skill, Customize, Skills, Create, Create manually; name, description, instructions. Over 18, Keep Activity on. Gems become read only on 17 November 2026. A skill made by hand holds no files (files come only with an uploaded skill), so the founder's texts go below the full file, under OUR TEXTS: Google advises examples within the instructions (read 27.10.2026). | Platforms | A |
| P7 | Gemini picks a skill by its name and description only, so the description names every kind of text the brand writes, and the founder can name the skill in a chat. Description limit: 1,024 characters. | Platforms | A |

## How the kit is tested

Step 3 of the brief, results in `test/`. The interview runs on claude-sonnet-5-5 through the API in English, French and Spanish, with a scripted founder (claude-haiku-5-5) answering from Levain's brand book and three sample texts written for Levain, labelled fictional. The ChatGPT run is done by Codex CLI standing in, and says so. Five tasks in three languages, with and without the voice file, each in a fresh call; `scan.py` counts the tells a script can see. Ten texts go to Pierre blind, the key in a separate file. Every number on the page and in the post comes from that run.
