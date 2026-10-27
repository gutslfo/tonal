"""Spanish brand copy written by two models, for the tells study.

Six fictional businesses (none of them Levain, which is the test brand) times the
five genres of the before/after test. Each text comes from a fresh call with a
plain founder prompt and no style instruction: the point is to see what the
models write by default.

    python generate.py claude    # claude-sonnet-5-5 through api.py (ledgered)
    python generate.py codex     # codex exec, the ChatGPT stand-in

Existing outputs are skipped, so a run can be resumed.
"""
import concurrent.futures as cf
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent))

BUSINESSES = {
    "taller-ocre": dict(
        name="Taller Ocre", what="un taller de cerámica en Valencia", founder="Lucía Ferrer", role="fundadora",
        facts="tazas y platos hechos a torno, esmalte de ceniza de naranjo, doce piezas por hornada, aptos para lavavajillas",
        ig="la nueva hornada de tazas sale el sábado",
        complaint="Me llegó la taza con una grieta en el asa y nadie me contesta el correo desde hace una semana.",
        nl="el horno nuevo y por qué las entregas de octubre se retrasan diez días",
        li="por qué decidió no vender en grandes almacenes"),
    "rueda-lenta": dict(
        name="Rueda Lenta", what="un taller de bicicletas en Villa Crespo, Buenos Aires", founder="Martín Sosa", role="fundador",
        facts="reparación y puesta a punto, turno en 48 horas, repuestos usados revisados con tres meses de garantía",
        ig="hay talleres gratuitos de mecánica básica el primer sábado de cada mes",
        complaint="Pagué la puesta a punto y a los dos días se me volvió a salir la cadena.",
        nl="la temporada de lluvias y cómo cuidar los frenos",
        li="lo que aprendió en diez años arreglando bicicletas"),
    "cafe-altamira": dict(
        name="Café Altamira", what="un tostador de café de especialidad en Bogotá", founder="Daniela Rojas", role="fundadora",
        facts="lotes de cinco kilos, cafés de Huila y Nariño, tostado los martes, envío en 48 horas dentro de Bogotá",
        ig="llegó un lote nuevo de Nariño, lavado, con notas de panela y mandarina",
        complaint="Pedí el café molido para prensa francesa y me llegó molido fino.",
        nl="por qué sube el precio de la bolsa de 500 gramos",
        li="pagar más a los caficultores"),
    "fisio-ribera": dict(
        name="Fisioterapia Ribera", what="una clínica de fisioterapia en Sevilla", founder="Javier Morales", role="fundador",
        facts="sesiones de 50 minutos, siempre con el mismo fisioterapeuta, ejercicios para casa en cada visita",
        ig="desde noviembre abren los sábados por la mañana",
        complaint="Esperé 25 minutos en recepción y luego la sesión duró media hora.",
        nl="el dolor de espalda de quien teletrabaja",
        li="por qué sus sesiones duran 50 minutos y no 30"),
    "libreria-la-tilde": dict(
        name="La Tilde", what="una librería de barrio en Coyoacán, Ciudad de México", founder="Ana Paula Méndez", role="fundadora",
        facts="libros nuevos y de segunda mano, club de lectura los jueves, pedidos especiales en una semana",
        ig="el club de lectura de noviembre lee Pedro Páramo",
        complaint="Encargué un libro hace tres semanas y todavía no llega; me dijeron que tardaba una semana.",
        nl="los diez años de la librería",
        li="por qué las librerías de barrio siguen abiertas"),
    "hostal-quillay": dict(
        name="Hostal Quillay", what="un hostal de ocho habitaciones en Valparaíso, Chile", founder="Tomás Fuentes", role="fundador",
        facts="desayuno con pan amasado, vista al puerto desde seis habitaciones, check-in hasta las 22 h, sin ascensor",
        ig="ya están abiertas las reservas para el verano",
        complaint="La habitación daba a la calle y no pudimos dormir por el ruido; en la web decía vista al puerto.",
        nl="lo que cambió en el hostal este invierno",
        li="dejar un trabajo en Santiago para abrir un hostal"),
}

GENRES = {
    "web": "Escribe el párrafo principal de la página web de {name}, {what}. Datos: {facts}.",
    "instagram": "Escribe el texto de una publicación de Instagram de {name} ({what}) para anunciar que {ig}.",
    "reply": "Soy {founder}, de {name} ({what}). Un cliente nos escribió esta queja: «{complaint}» Escribe mi respuesta.",
    "newsletter": "Escribe el primer párrafo del boletín mensual de {name} ({what}). Este mes el tema es {nl}.",
    "linkedin": "Escribe una publicación de LinkedIn para {founder}, {role} de {name} ({what}), sobre {li}.",
}
TAIL = " Solo el texto, sin comentarios."


def prompts():
    for b, d in BUSINESSES.items():
        for g, t in GENRES.items():
            yield f"{b}-{g}", t.format(**d) + TAIL


def run_claude(key, prompt, out):
    import api
    out.write_text(api.call("claude-sonnet-5-5", [{"role": "user", "content": prompt}],
                            max_tokens=2000, tag=f"es-study:{key}") + "\n", encoding="utf-8")


def run_codex(key, prompt, out):
    # Pierre's global ~/.codex/AGENTS.md loads regardless (operating rules, no style
    # rules); the prompt forbids commands and the events log is checked for any.
    empty = tempfile.mkdtemp(prefix="tonal-codex-")
    p = subprocess.run([shutil.which("codex"), "exec", "--skip-git-repo-check", "--ephemeral", "--sandbox",
                        "read-only", "-C", empty, "--json", "-o", str(out), "-"],
                       input="Do not run any command or read any file. Answer this request directly.\n\n" + prompt,
                       capture_output=True, text=True, encoding="utf-8", timeout=600)
    (out.parent / f"{key}.events.jsonl").write_text(p.stdout, encoding="utf-8")
    if p.returncode or not out.exists():
        raise RuntimeError(f"{key}: codex exit {p.returncode} {p.stderr[-300:]}")


if __name__ == "__main__":
    who = sys.argv[1]
    fn, workers = {"claude": (run_claude, 6), "codex": (run_codex, 4)}[who]
    outdir = HERE / "samples" / who
    outdir.mkdir(parents=True, exist_ok=True)
    todo = [(k, p, outdir / f"{k}.txt") for k, p in prompts() if not (outdir / f"{k}.txt").exists()]
    with cf.ThreadPoolExecutor(workers) as ex:
        for f in cf.as_completed([ex.submit(fn, *t) for t in todo]):
            f.result()
    print(f"{who}: {len(list(outdir.glob('*.txt')))} texts in {outdir}")
