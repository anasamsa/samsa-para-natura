"""Vitrina privada de trabajos de Samsa para Natura y Avon (19/11/2026).
_base.css + _ia.css + _show.css + _natura.css + _body.html -> artifact.html (para revisar en Claude) e index.html.
En _body.html, {{r:img/archivo.jpg}} se reemplaza por la proporción ancho/alto de esa imagen (para las filas .frow)."""
import re
from pathlib import Path
from PIL import Image
H = Path(__file__).parent
css = "\n".join((H/f).read_text() for f in ("_base.css", "_ia.css", "_show.css", "_natura.css"))
FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap">\n'

def ratio(m):
    w, h = Image.open(H/m.group(1)).size
    return f"{w/h:.4f}"

body = re.sub(r"\{\{r:([^}]+)\}\}", ratio, (H/"_body.html").read_text())
missing = [s for s in re.findall(r'(?:src|data-src|poster)="(img/[^"]+)"', body) if not (H/s).exists()]
if missing: print("FALTAN:", sorted(set(missing)))
head = ('<title>Samsa para Natura</title>\n<meta name="robots" content="noindex, nofollow">\n'
        '<meta name="description" content="Trabajos de Samsa Creative para Natura y Avon. Documento privado.">\n'
        + FONT + f'<style>\n{css}\n</style>\n')
(H/"artifact.html").write_text('<meta name="claude:viewport-fit-sides" content="cover">' + head + body)
(H/"index.html").write_text('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + head + '</head>\n<body>\n' + body + '\n</body>\n</html>\n')
used = sorted(set(re.findall(r'(?:src|data-src|poster)="(img/[^"]+)"', body)))
(H/"_files.txt").write_text("\n".join(used))
print("ok", len(used), "archivos")
