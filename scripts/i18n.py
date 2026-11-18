"""Versión en gallego: traduce el HTML ya generado (nodos de texto y atributos) con el diccionario scripts/gl.py.
Lo que no esté en el diccionario se queda en castellano y se anota en scripts/gl_pendientes.txt."""
import re, json
from html import unescape
from pathlib import Path

try:
    from gl import GL
except Exception:  # pragma: no cover
    GL = {}
MISSING = set()
SUFFIX = ' | Pelucans · A Laracha'
SUFFIX_OG = ' | Pelucans'

def norm(t):
    return re.sub(r'\s+', ' ', t).strip()

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def tr_plain(text):
    """Devuelve la traducción de una cadena ya normalizada (o None)."""
    return GL.get(text)

def tr(text, attr=False):
    n = norm(unescape(text))
    if not n or not re.search(r'[A-Za-zÁÉÍÓÚáéíóúñÑ]', n):
        return text
    for suf in (SUFFIX, SUFFIX_OG):
        if n.endswith(suf):
            head = n[: -len(suf)]
            t = GL.get(head)
            if t is None:
                MISSING.add(head); return text
            return esc(t) + suf if not attr else (t.replace('"', '&quot;') + suf)
    t = GL.get(n)
    if t is None:
        MISSING.add(n)
        return text
    lead = text[: len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    out = t.replace('"', '&quot;') if attr else esc(t)
    return lead + out + trail

def to_galician(html, file):
    # 1) separar scripts/estilos (no se traducen salvo el JSON de servicios)
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', html, flags=re.S)
    out = []
    for part in parts:
        if part.startswith('<script'):
            if 'id="svc-data"' in part:
                m = re.search(r'(<script[^>]*>)(.*?)(</script>)', part, flags=re.S)
                data = json.loads(m.group(2).replace('<\\/', '</'))
                for d in data:
                    d['name'] = unescape(tr(d['name'])); d['short'] = unescape(tr(d['short']))
                    d['img'] = '../' + d['img'] if not d['img'].startswith('../') else d['img']
                part = m.group(1) + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + m.group(3)
            out.append(part); continue
        if part.startswith('<style'):
            out.append(part); continue
        # nodos de texto
        part = re.sub(r'>([^<>]+)<', lambda m: '>' + tr(m.group(1)) + '<', part)
        # atributos traducibles
        part = re.sub(r'\b(alt|title|aria-label|placeholder)="([^"]*)"', lambda m: f'{m.group(1)}="{tr(m.group(2), True)}"', part)
        part = re.sub(r'(<meta (?:name="description"|property="og:(?:title|description)") content=")([^"]*)(")', lambda m: m.group(1) + tr(m.group(2), True) + m.group(3), part)
        out.append(part)
    h = ''.join(out)
    # 2) idioma y rutas
    h = h.replace('<html lang="es">', '<html lang="gl">', 1)
    h = re.sub(r'(["\'])assets/', r'\1../assets/', h)
    h = h.replace(f'<a href="{file}" lang="es" aria-current="true">ES</a><a href="gl/{file}" lang="gl" hreflang="gl">GL</a>',
                  f'<a href="../{file}" lang="es" hreflang="es">ES</a><a href="{file}" lang="gl" aria-current="true">GL</a>')
    h = h.replace(f'<link rel="alternate" hreflang="es" href="{file}"><link rel="alternate" hreflang="gl" href="gl/{file}">',
                  f'<link rel="alternate" hreflang="es" href="../{file}"><link rel="alternate" hreflang="gl" href="{file}">')
    h = h.replace('<script src="../assets/js/site.js" defer>', "<script>window.PEL_ROOT='../'</script><script src=\"../assets/js/site.js\" defer>", 1)
    return h

def report():
    p = Path(__file__).parent / 'gl_pendientes.txt'
    p.write_text('\n'.join(sorted(MISSING)), encoding='utf-8')
    return len(MISSING)
