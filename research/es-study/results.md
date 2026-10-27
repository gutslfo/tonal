# Spanish AI tells: what was measured

Run on 26 October 2026. Raw numbers: `results-raw.md`, produced by `analyze.py`. Samples: `samples/claude/` and `samples/codex/`. Grade M throughout: measured here, small sample, read by someone who is not a native speaker. A native reader has not checked any of it yet.

## Why a study at all

No Spanish equivalent of Wikipedia's "Signs of AI writing" was found, and no corpus study of Spanish model output for brand copy. What circulates in Spanish are blog lists. The longest one ([El Androide Feliz, 2024](https://elandroidefeliz.com/chatgpt-frases-y-palabras-mas-frecuentes/)) is visibly a translation of the English list: *tapiz* for tapestry, *testimonio* for testament, *bullicioso* for bustling, *reino* for realm. The brief rules out translated tells, so the lists were tested instead of trusted.

## Design

- Machine side: six fictional businesses (Valencia, Buenos Aires, Bogotá, Sevilla, Ciudad de México, Valparaíso; none of them Levain) times the five genres of the before and after test: the main paragraph of a website, an Instagram caption, a reply to an unhappy customer, a newsletter opening and a LinkedIn post. One fresh call per text, a plain founder prompt in Spanish, no style instruction, "Solo el texto, sin comentarios" at the end. 30 texts from claude-sonnet-5-5 (API, no system prompt, $0.15) and 30 from Codex CLI 0.163 (`codex exec`, the ChatGPT stand-in). Codex loaded Pierre's global AGENTS.md, which holds operating rules and no writing rules; its event logs show it ran no command. 8,041 words in all.
- Human side: the human half of AuTexTification 2023, Spanish: 20,349 texts, 1,032,974 words, all written before 2023 (news, hotel and restaurant reviews, how-to wiki pages, tweets).
- A phrase counts as over-used when it appears at least four times, in texts for at least three of the six businesses (so one shop's own vocabulary does not count), and at least five times more often per word than in the human texts.
- A phrase becomes a rule in the kit only with a second signal: the same reflex in the humanizer's English or French patterns, or in a published Spanish list.

## Limits, stated before the findings

- Genre confound: the human corpus holds no brand copy, no customer-service replies and no Instagram captions. Part of what the models over-use is the genre itself. That is why a second signal is required.
- AuTexTification strips every quotation mark from its texts (counted: zero " “ ” in a million words, human and generated alike). Quotes are not compared.
- 60 texts is small. A phrase seen in four texts is a lead, not a law.
- Two models, one run each, on 26 October 2026. Gemini is not in the sample.

## Kept: measured and confirmed by a second signal

| tell | measured | second signal |
|---|---|---|
| *en el corazón de* + a place ("en el corazón de Valencia") | 5.0 per 10k words against 0.1 in the human texts; 4 Claude texts, 0 Codex | humanizer 4 "in the heart of", 37 "au cœur de" |
| *No es X, es Y*, and its two-sentence form *No fue X. Fue Y.* | 5.4 per 10k for Claude against at most 0.6 in any human domain; 0 for Codex | humanizer 9; Borja Girón 2026 "el falso contraste dramático" |
| Lists of three, *X, Y y Z* ("con barro, paciencia y las manos", "cálidos, únicos e irrepetibles") | 31 (Claude) and 40 (Codex) per 10k against 5 to 17 in the human domains | humanizer 10 and 40 |
| *artesanal*, *artesanía* | 5.0 against 0.3; 3 Claude texts | humanizer 37 "savoir-faire artisanal"; Levain's own banned word |
| Customer-service formulas: *lamento (sinceramente) las molestias*, *entiendo que*, *gracias por escribirnos / por avisarnos*, *Estimado/a cliente*, *Un cordial saludo*, *sus comentarios nos ayudan a mejorar* | *lamento* 11.2 against 0.1; *gracias por* 12.4 against 0.2; *Estimado/a* in 2 of 6 Claude replies | humanizer 22 (servile tone), 20 |
| The values clause: *porque creemos que*, *creemos que*, *sabemos que* | *creemos que* 6.2 against 0.1; *sabemos que* 5.0 against 0.1 | humanizer 1 and 27 (significance and authority stated rather than shown) |
| The closing invitation: *te esperamos*, *¡Nos vemos en…!*, *si algún día pasan por…* | *te esperamos* 5.0 against 0.0; 3 Claude texts | humanizer 25 (generic upbeat ending); FR 37 "n'hésitez pas à" |
| Chat formatting pasted as copy: emoji at the head of lines, markdown `**bold**`, a hashtag block, arrow lists | emoji in 9 of 30 Claude texts and 6 of 30 Codex; `**` in 5 Claude texts (it prints as asterisks on Instagram and LinkedIn); hashtags under all 6 Claude LinkedIn posts, none under Codex's; → lists in 2 Claude LinkedIn posts | humanizer 15, 18, 39 |
| Staccato and aphorism in LinkedIn posts ("La respuesta fue no.", "Nada se pierde del todo. Se reubica.") | read, not counted | humanizer 31 and 32; Borja Girón "la sentencia pseudo-filosófica" |

## Found but not kept as rules (one signal only)

- *cada pieza*, *cada detalle*, *cada sorbo* (165 times the human rate for *cada pieza*, but no second source).
- *sin prisa(s)*: 4 Claude texts, 0 human uses, no second source.
- *a quienes* ("para quienes buscan…"): 40 times the human rate in both models, no second source.
- Codex opens or closes LinkedIn posts with *Hola, soy* / *Soy Tomás, fundador de…* (4 of 6). Only one model, no second source.

## Hypotheses that the counts did not support

- The translated lists. Of the 48 items checked from Borja Girón (2026) and El Androide Feliz (2024), 46 never appear in the 60 texts. *magia* appears once, *viaje* in three texts at a rate barely above the human one (3.7 against 2.0). *tapiz*, *testimonio*, *sumérgete*, *en conclusión*, *en la era digital*: zero. These lists describe older English-trained output, not what a 2026 model writes in Spanish for a shop.
- The raya. Claude used it 1.8 times per 10k words, Codex never; the one single raya was a signature line ("— Tomás Fuentes"). The raya is correct Spanish for asides and dialogue ([RAE, Diccionario panhispánico de dudas, "raya"](https://www.rae.es/dpd/raya), read 26.10.2026), and the same entry says the closing raya of an aside is never dropped, "ni siquiera cuando el inciso ocupa el final del enunciado". So the kit keeps the RAE rule: an aside between two rayas is Spanish, a single dash that swings the sentence English-style is not. No ban.
- The gerund tail (", creando…", ", generando…"), the Spanish twin of the English -ing tail. The models used it less than the human writers did (1.8 and 0 per 10k against 4 to 11). Not a tell in this sample.
- Title Case headings. The one line flagged was a book title, correctly capitalised. Not seen.

## A Spanish-specific rule the sample surfaced

Both models switched to voseo for the Buenos Aires shop on their own (*tenés*, *podés*, *escribinos*), so regional variety is handled. What drifts is the form of address. Claude answered four of its six unhappy customers with *usted* (two of them opening on *Estimado/a cliente*) and two with *tú* or *vos*; Codex used *tú* five times and the plural *ustedes* once, for a couple. Nothing in the prompts decided it. The voice file has to fix *tú*, *usted* or *vos*, and the country, the way the French file fixes *tu* or *vous* (humanizer 39).
