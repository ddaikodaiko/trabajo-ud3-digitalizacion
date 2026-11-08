#!/usr/bin/env python3
"""Monta la web “TecnoElectro, rumbo a la nube” a partir de src/index.html."""
import hashlib
import re
from pathlib import Path

RAIZ = Path(__file__).parent
SRC = RAIZ / "src"
SITIO = RAIZ / "site"

TITULO = "TecnoElectro, rumbo a la nube"
DESCRIPCION = ("Trabajo de Digitalización (UD3): diagnóstico, servicios cloud, edge y fog, costes, "
               "seguridad y plan de migración de TecnoElectro S.L.")
EQUIPO = "Marcos Ramos, Gonzalo Redondo, Jaime Ramos y Victor Cerveros"

REPARTO = [
    ("1", "Marcos Ramos", "Diagnóstico y modelo de despliegue", [("diagnostico", "2. Diagnóstico")]),
    ("2", "Gonzalo Redondo", "Servicios, responsabilidades y acceso", [("servicios", "3. Servicios")]),
    ("3", "Jaime Ramos", "Edge, fog y mist, y costes", [("niveles", "4. Edge, fog y mist"), ("viabilidad", "5. Costes")]),
    ("4", "Victor Cerveros", "Seguridad y migración", [("viabilidad", "5. Seguridad"), ("migracion", "6. Migración")]),
]

UNSPLASH = "https://images.unsplash.com/"
FOTOS = {
    "tienda": ("photo-1740803292374-1b167c1558b1", "Zoshua Colah",
               "https://unsplash.com/photos/a-room-filled-with-lots-of-different-types-of-microwaves-q2Cri6LS8iI",
               "Estanterías de una tienda con pequeños electrodomésticos expuestos."),
    "tecnico": ("photo-1562941995-17dc31eaaf6d", "Blaz Erzetic",
                "https://unsplash.com/photos/man-soldering-wires-rP30_20fDpw",
                "Un técnico suelda los cables de una placa."),
    "almacen": ("photo-1592085198739-ffcad7f36b54", "Arno Senoner",
                "https://unsplash.com/photos/warehouse-shelving-with-stacked-boxes-yqu6tJkSQ_k",
                "Pasillo de un almacén con estanterías azules llenas de cajas."),
}

FUENTES = ("https://fonts.googleapis.com/css2?family=Saira+Semi+Condensed:wght@500;600;700"
           "&amp;family=Source+Sans+3:ital,wght@0,400..700;1,400&amp;display=swap")

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{fuentes}" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{fuentes}"></noscript>
<link rel="stylesheet" href="assets/estilos.css?v={v}">
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<nav class="barra" aria-label="Apartados del trabajo">
  <div class="barra__dentro">
    <a class="barra__marca" href="#inicio"><span class="barra__logo" aria-hidden="true"></span>TecnoElectro <em>· nube</em></a>
    <button class="barra__boton" type="button" aria-expanded="false" aria-controls="barra-lista">Apartados</button>
    <ol class="barra__lista" id="barra-lista">
{nav}
    </ol>
  </div>
</nav>
<main id="contenido">
{cuerpo}
</main>
<footer class="pie"><div class="pie__dentro"><p>Trabajo de clase de {equipo}. Digitalización, UD3. Esquemas de elaboración propia; fotos de Unsplash.</p><p><a href="#inicio">Volver arriba</a></p></div></footer>
<script src="assets/sitio.js?v={v}" defer></script>
</body>
</html>
"""

PRIORIDAD = {"critica": "Crítica", "alta": "Alta", "media": "Media"}
MODELO = {"saas": ("Software como servicio", "SaaS"), "paas": ("Plataforma como servicio", "PaaS"),
          "iaas": ("Infraestructura como servicio", "IaaS")}
ESTADO = {"si": ("✓", "Sí"), "no": ("✕", "No"), "parcial": ("◐", "En parte")}
TIPO = {"inicial": "Inicial", "recurrente": "Recurrente", "ambos": "Inicial y recurrente"}


def foto(clave, pie):
    ident, autor, pagina, alt = FOTOS[clave]
    urls = [(f"{UNSPLASH}{ident}?auto=format&amp;fit=crop&amp;w={a}&amp;h={a * 9 // 16}&amp;q=70", a) for a in (720, 1440)]
    srcset = ", ".join(f"{u} {a}w" for u, a in urls)
    carga = 'fetchpriority="high"' if clave == "tienda" else 'loading="lazy"'
    return (f'<figure class="foto"><img data-foto src="{urls[-1][0]}" srcset="{srcset}" sizes="(max-width: 72rem) 92vw, 68rem" '
            f'width="1440" height="810" alt="{alt}" {carga} decoding="async">'
            f'<figcaption>{pie}. <span>Foto: <a href="{pagina}">{autor}</a>, Unsplash.</span></figcaption></figure>')


def encargo(nombre, corto=False):
    if corto:
        return f"<strong>{nombre}</strong>"
    return f"Se encarga <strong>{nombre}</strong>"


def reparto():
    filas = "".join(f'<tr><th scope="row">{nombre}</th><td>{parte}</td><td>{", ".join(f"<a href=\"#{i}\">{t}</a>" for i, t in secc)}</td></tr>'
                    for n, nombre, parte, secc in REPARTO)
    return ('<div class="tabla"><table><thead><tr><th scope="col">Integrante</th><th scope="col">Parte</th>'
            '<th scope="col">Secciones</th></tr></thead><tbody>' + filas + "</tbody></table></div>")


def creditos():
    filas = "".join(f'<li>{autor}. <a href="{pagina}">{alt.rstrip(".")}</a>. Unsplash, licencia libre.</li>' for _, autor, pagina, alt in FOTOS.values())
    return '<h3 class="h-sub">Fotografías</h3><ul class="refs refs--fotos">' + filas + "</ul>"


def macros(cuerpo):
    cuerpo = re.sub(r"\{\{foto:([a-z]+)\|([^}]+)\}\}", lambda m: foto(m.group(1), m.group(2)), cuerpo)
    cuerpo = re.sub(r"\{\{encargo-corto:([^}]+)\}\}", lambda m: encargo(m.group(1), True), cuerpo)
    cuerpo = re.sub(r"\{\{encargo:([^}]+)\}\}", lambda m: encargo(m.group(1)), cuerpo)
    cuerpo = cuerpo.replace("{{reparto}}", reparto()).replace("{{creditos}}", creditos())
    cuerpo = re.sub(r"\{\{prioridad:(critica|alta|media)\}\}",
                    lambda m: f'<span class="prio prio--{m.group(1)}">{PRIORIDAD[m.group(1)]}</span>', cuerpo)
    cuerpo = re.sub(r"\{\{modelo:(saas|paas|iaas)\}\}",
                    lambda m: f'<span class="modelo modelo--{m.group(1)}" title="{MODELO[m.group(1)][0]}">{MODELO[m.group(1)][1]}</span>', cuerpo)
    cuerpo = re.sub(r"\{\{estado:(si|no|parcial)\}\}",
                    lambda m: f'<span class="estado estado--{m.group(1)}"><span class="estado__i" aria-hidden="true">{ESTADO[m.group(1)][0]}</span>{ESTADO[m.group(1)][1]}</span>', cuerpo)
    cuerpo = re.sub(r"\{\{tipo:(inicial|recurrente|ambos)\}\}",
                    lambda m: f'<span class="tipo tipo--{m.group(1)}">{TIPO[m.group(1)]}</span>', cuerpo)
    return cuerpo


def espacios_duros(cuerpo):
    cuerpo = re.sub(r"(\d) %", r"\1&nbsp;%", cuerpo)
    cuerpo = re.sub(r"(\d) °C", r"\1&nbsp;°C", cuerpo)
    cuerpo = re.sub(r"(\d) €", r"\1&nbsp;€", cuerpo)
    cuerpo = re.sub(r"(\d) \$", r"\1&nbsp;$", cuerpo)
    return cuerpo.replace(" × ", "&nbsp;× ")


def limpiar_texto(fragmento):
    fragmento = re.sub(r'<span class="supuesto">.*?</span>', "", fragmento, flags=re.S)
    return re.sub(r"<[^>]+>", "", fragmento).strip().replace('"', "&quot;")


def apilar_tabla(m):
    tabla = m.group(0)
    cab = re.search(r"<thead>(.*?)</thead>", tabla, flags=re.S)
    if not cab:
        return tabla
    etiquetas = [limpiar_texto(t) for t in re.findall(r"<th[^>]*>(.*?)</th>", cab.group(1), flags=re.S)]

    def fila(mf):
        pos = iter(range(len(etiquetas)))
        def celda(mc):
            i = next(pos, None)
            if i is None:
                return mc.group(0)
            return f'<{mc.group(1)} data-et="{etiquetas[i]}"{mc.group(2)}>'
        return re.sub(r"<(th|td)((?:\s[^>]*)?)>", celda, mf.group(0))

    cuerpo = re.search(r"<tbody>.*?</tbody>", tabla, flags=re.S)
    nuevo = re.sub(r"<tr>.*?</tr>", fila, cuerpo.group(0), flags=re.S)
    return tabla.replace(cuerpo.group(0), nuevo)


def apilable(html):
    return re.sub(r'<div class="tabla[^"]*">\s*<table>.*?</table>', apilar_tabla, html, flags=re.S)


def navegacion(cuerpo):
    filas = []
    for ident, nombre, n in re.findall(r'<section class="[^"]*" id="([^"]+)" data-etapa="([^"]+)" data-n="([^"]+)"', cuerpo):
        filas.append(f'      <li><a href="#{ident}"><span>{n}</span>{nombre}</a></li>')
    return "\n".join(filas)


def version():
    h = hashlib.sha1()
    for nombre in ("estilos.css", "sitio.js"):
        h.update((SITIO / "assets" / nombre).read_bytes())
    return h.hexdigest()[:8]


def main():
    cuerpo = (SRC / "index.html").read_text(encoding="utf-8")
    cuerpo = macros(cuerpo)
    cuerpo = espacios_duros(cuerpo)
    cuerpo = apilable(cuerpo)
    html = PLANTILLA.format(titulo=TITULO, descripcion=DESCRIPCION, fuentes=FUENTES, v=version(),
                            nav=navegacion(cuerpo), cuerpo=cuerpo.rstrip(), equipo=EQUIPO)
    if "{{" in html:
        i = html.index("{{")
        raise SystemExit("Macro sin resolver: " + html[i:i + 80])
    (SITIO / "index.html").write_text(html, encoding="utf-8")
    (SITIO / ".nojekyll").write_text("", encoding="utf-8")
    print("ok index.html", len(html))


if __name__ == "__main__":
    main()
