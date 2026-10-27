"""Five Levain tasks per language, with and without the voice file.

    python test/tasks.py en fr es

Each text is a fresh call to claude-sonnet-5-5 with the same request. "with"
puts the full voice file the interview produced (test/interview/claude-<lang>
-full.txt) in the system prompt, the way a project's instructions are read;
"without" has no system prompt. Output: test/tasks/<lang>/<task>-<with|without>.txt
"""
import concurrent.futures as cf, pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import api

TASKS = {
    "en": {
        "intro": "I run Levain, a bakery at 3 Mill Lane, London. ",
        "tail": " Just the text, no comments.",
        "page": "Write the paragraph for the rye loaf on our website. The facts: it takes two days. Forty loaves a day, ready at ten. The levain is fed twice a day and the dough rests overnight in the cold.",
        "instagram": "Write an Instagram caption: the rye is back this Saturday, forty loaves, from ten.",
        "reply": "A customer wrote to us: \"I came at eleven on Saturday and the rye was sold out, the second Saturday in a row. Why don't you bake more?\" Write our reply. The facts: the rye takes two days, so we bake forty loaves. Customers can order for Saturday on our website.",
        "newsletter": "Write the opening paragraph of our November newsletter. The news: from 1 November the country loaf (800 g) is baked twice a day, at dawn and at noon.",
        "linkedin": "Write a LinkedIn post: Levain starts wholesale in spring 2027, for cafés and restaurants nearby. Businesses that are interested can write to hello@levain.example.",
    },
    "fr": {
        "intro": "Je tiens Levain, une boulangerie de la rue du Moulin 3, à Lausanne. ",
        "tail": " Seulement le texte, sans commentaire.",
        "page": "Écris le paragraphe du pain de seigle pour notre site. Les faits : il lui faut deux jours. Quarante pains par jour, prêts à dix heures. Le levain est nourri deux fois par jour et la pâte repose une nuit au froid.",
        "instagram": "Écris une légende Instagram : le seigle revient ce samedi, quarante pains, dès dix heures.",
        "reply": "Un client nous a écrit : « Je suis venu samedi à onze heures et il n'y avait plus de seigle, pour la deuxième fois de suite. Pourquoi vous n'en faites pas plus ? » Écris notre réponse. Les faits : le seigle demande deux jours, alors nous en cuisons quarante. On peut commander pour le samedi sur notre site.",
        "newsletter": "Écris le paragraphe d'ouverture de notre lettre d'information de novembre. La nouvelle : dès le 1er novembre, le pain de campagne (800 g) est cuit deux fois par jour, à l'aube et à midi.",
        "linkedin": "Écris une publication LinkedIn : Levain commence la vente en gros au printemps 2027, pour les cafés et les restaurants du quartier. Les entreprises intéressées peuvent écrire à hello@levain.example.",
    },
    "es": {
        "intro": "Llevo Levain, una panadería de la calle del Molino 3, en Madrid. ",
        "tail": " Solo el texto, sin comentarios.",
        "page": "Escribe el párrafo del pan de centeno para nuestra web. Los datos: tarda dos días. Cuarenta panes al día, listos a las diez. Alimentamos la masa madre dos veces al día y la masa reposa una noche en frío.",
        "instagram": "Escribe un texto para Instagram: el centeno vuelve este sábado, cuarenta panes, desde las diez.",
        "reply": "Un cliente nos escribió: «Vine el sábado a las once y ya no quedaba centeno, por segundo sábado seguido. ¿Por qué no hacéis más?». Escribe nuestra respuesta. Los datos: el centeno tarda dos días, así que horneamos cuarenta. Se puede encargar para el sábado en nuestra web.",
        "newsletter": "Escribe el párrafo de apertura de nuestro boletín de noviembre. La novedad: desde el 1 de noviembre, el pan de pueblo (800 g) se hornea dos veces al día, al amanecer y a mediodía.",
        "linkedin": "Escribe una publicación de LinkedIn: Levain empieza la venta al por mayor en la primavera de 2027, para cafeterías y restaurantes del barrio. Las empresas interesadas pueden escribir a hello@levain.example.",
    },
}
NAMES = ["page", "instagram", "reply", "newsletter", "linkedin"]


def run(lang, task, cond):
    t = TASKS[lang]
    out = HERE / "tasks" / lang / f"{task}-{cond}.txt"
    if out.exists():
        return
    system = (HERE / "interview" / f"claude-{lang}-full.txt").read_text(encoding="utf-8") if cond == "with" else None
    text = api.call("claude-sonnet-5-5", [{"role": "user", "content": t["intro"] + t[task] + t["tail"]}],
                    system=system, max_tokens=8000, tag=f"task-{lang}-{task}-{cond}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    jobs = [(l, t, c) for l in sys.argv[1:] for t in NAMES for c in ("without", "with")]
    with cf.ThreadPoolExecutor(6) as ex:
        for f in cf.as_completed([ex.submit(run, *j) for j in jobs]):
            f.result()
    print(f"{len(jobs)} texts, spent ${api.spent():.4f}")
