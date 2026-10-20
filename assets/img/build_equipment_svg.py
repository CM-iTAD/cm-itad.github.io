"""
Generates the equipment schematics on lab.html.

These are ORIGINAL orthographic line drawings, proportioned from the lab's own
machines. They deliberately replace the vendor marketing photographs that were
collected in /machines: those are the manufacturers' copyrighted images (one
still carries a visible retailer watermark), and DESIGN.md §7 rules out stock
imagery anyway. A schematic is also honest in a way a photoreal render is not —
it reads as a diagram rather than as a photograph of a machine we may not own
in that exact configuration.

Palette and stroke weights come from assets/css/site.css. Re-run after editing:
    python assets/img/build_equipment_svg.py
"""
import os
from xml.sax.saxutils import escape

INK, INK2, HAIR = "#11243B", "#46586D", "#D6DFEA"
BLUE, AMBER, PANEL = "#1D70B3", "#995F0B", "#E9EFF6"
W, H = 800, 500  # 16:10, matching .card__media

HEAD = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
    'width="{w}" height="{h}" role="img" aria-label="{alt}">'
    '<title>{alt}</title>'
    '<rect width="{w}" height="{h}" fill="#fff"/>'
    '<g fill="none" stroke="{ink}" stroke-width="1.6" '
    'stroke-linecap="square" stroke-linejoin="miter">'
)
FOOT = "</g></svg>"


def esc(t):
    """XML-escape. SVG in an <img> is parsed as strict XML: a bare `&` in a
    label is a fatal error and the browser renders nothing at all."""
    return escape(str(t), {'"': "&quot;"})


def label(x, y, text, size=12, fill=INK2, anchor="start", weight=500):
    return (f'<text x="{x}" y="{y}" font-family="IBM Plex Mono, ui-monospace, monospace" '
            f'font-size="{size}" font-weight="{weight}" letter-spacing="1.1" '
            f'fill="{fill}" text-anchor="{anchor}" stroke="none">{esc(text)}</text>')


def baseline(y=430, x0=90, x1=710):
    return f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{HAIR}" stroke-width="1.4"/>'


def dim_v(x, y0, y1, text):
    """Vertical dimension line with amber ticks — the spec-sheet motif."""
    return (f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{AMBER}" stroke-width="1.2"/>'
            f'<line x1="{x-5}" y1="{y0}" x2="{x+5}" y2="{y0}" stroke="{AMBER}" stroke-width="1.6"/>'
            f'<line x1="{x-5}" y1="{y1}" x2="{x+5}" y2="{y1}" stroke="{AMBER}" stroke-width="1.6"/>'
            + label(x + 11, (y0 + y1) / 2 + 4, text, 11, AMBER))


def creatbot():
    """Large-format enclosed FDM: cubic body, glazed door, lower filament bays."""
    s = [baseline()]
    s.append(f'<rect x="250" y="120" width="300" height="250" fill="{PANEL}"/>')      # body
    s.append('<rect x="250" y="120" width="300" height="250"/>')
    s.append(f'<rect x="268" y="150" width="200" height="160" fill="#fff"/>')          # door glass
    s.append('<rect x="268" y="150" width="200" height="160"/>')
    s.append(f'<line x1="458" y1="170" x2="458" y2="290" stroke="{INK2}" stroke-width="3"/>')  # handle
    s.append('<rect x="486" y="150" width="46" height="30"/>')                          # screen
    s.append(f'<rect x="486" y="150" width="46" height="30" fill="{BLUE}" opacity=".18" stroke="none"/>')
    s.append('<rect x="250" y="370" width="300" height="56"/>')                         # base cabinet
    s.append('<rect x="276" y="384" width="118" height="30"/>')                         # filament bay
    s.append('<rect x="406" y="384" width="118" height="30"/>')
    s.append('<path d="M352 120 L352 104 L448 104 L448 120"/>')                         # carry handle
    s.append(f'<line x1="300" y1="188" x2="436" y2="188" stroke="{INK2}" stroke-width="1.2"/>')  # gantry
    s.append('<rect x="352" y="182" width="30" height="20"/>')                          # dual hotend
    s.append('<rect x="386" y="182" width="30" height="20"/>')
    s.append(f'<line x1="286" y1="292" x2="450" y2="292" stroke="{INK2}" stroke-width="1.6"/>')  # bed
    s.append(label(250, 90, "CREATBOT D600 PRO 2", 13, INK, weight=600))
    s.append(label(250, 462, "LARGE-FORMAT FDM · DUAL EXTRUDER", 11, INK2))
    return s


def bambu():
    """Compact enclosed FDM with the AMS material unit seated on top."""
    s = [baseline()]
    s.append(f'<rect x="300" y="128" width="200" height="74" fill="{PANEL}"/>')          # AMS
    s.append('<rect x="300" y="128" width="200" height="74"/>')
    for cx in (338, 376, 424, 462):                                                      # spools
        s.append(f'<circle cx="{cx}" cy="165" r="19" stroke="{INK2}" stroke-width="1.3"/>')
        s.append(f'<circle cx="{cx}" cy="165" r="6" stroke="{INK2}" stroke-width="1.3"/>')
    s.append(f'<rect x="300" y="202" width="200" height="206" fill="{PANEL}"/>')          # body
    s.append('<rect x="300" y="202" width="200" height="206"/>')
    s.append(f'<rect x="318" y="232" width="164" height="140" fill="#fff"/>')             # window
    s.append('<rect x="318" y="232" width="164" height="140"/>')
    s.append('<rect x="306" y="210" width="34" height="22"/>')                            # screen
    s.append(f'<rect x="306" y="210" width="34" height="22" fill="{BLUE}" opacity=".18" stroke="none"/>')
    s.append(f'<line x1="332" y1="262" x2="468" y2="262" stroke="{INK2}" stroke-width="1.2"/>')
    s.append('<rect x="382" y="256" width="32" height="20"/>')                            # hotend
    s.append(f'<line x1="330" y1="352" x2="470" y2="352" stroke="{INK2}" stroke-width="1.6"/>')  # bed
    s.append('<rect x="300" y="408" width="200" height="20"/>')                           # foot
    s.append(label(300, 98, "BAMBU LAB X1E + AMS", 13, INK, weight=600))
    s.append(label(300, 462, "ENCLOSED FDM · MULTI-MATERIAL", 11, INK2))
    return s


def raise3d():
    """Enclosed dual-extruder FDM; build volume verified from the manual."""
    s = [baseline()]
    s.append(f'<rect x="276" y="136" width="248" height="236" fill="{PANEL}"/>')
    s.append('<rect x="276" y="136" width="248" height="236"/>')
    s.append(f'<rect x="294" y="162" width="166" height="176" fill="#fff"/>')
    s.append('<rect x="294" y="162" width="166" height="176"/>')
    s.append('<rect x="472" y="162" width="40" height="30"/>')                            # screen
    s.append(f'<rect x="472" y="162" width="40" height="30" fill="{BLUE}" opacity=".18" stroke="none"/>')
    s.append(f'<line x1="310" y1="196" x2="444" y2="196" stroke="{INK2}" stroke-width="1.2"/>')
    s.append('<rect x="356" y="190" width="26" height="18"/>')
    s.append('<rect x="386" y="190" width="26" height="18"/>')
    s.append(f'<line x1="306" y1="318" x2="448" y2="318" stroke="{INK2}" stroke-width="1.6"/>')
    s.append('<rect x="276" y="372" width="248" height="54"/>')                           # base
    s.append(f'<circle cx="500" cy="286" r="26" stroke="{INK2}" stroke-width="1.3"/>')     # spool
    s.append(f'<circle cx="500" cy="286" r="8" stroke="{INK2}" stroke-width="1.3"/>')
    s.append(dim_v(560, 196, 318, "300 mm"))
    s.append(label(276, 106, "RAISE3D PRO3", 13, INK, weight=600))
    s.append(label(276, 462, "BUILD VOLUME 300 × 300 × 300 mm", 11, AMBER))
    return s


def toplaser():
    """Flatbed CO2 laser cutter, lid raised."""
    s = [baseline(y=426, x0=80, x1=720)]
    s.append('<path d="M186 236 L214 150 L586 150 L614 236 Z"/>')                         # raised lid
    s.append(f'<path d="M198 228 L220 162 L390 162 L390 228 Z" fill="{PANEL}" stroke="{HAIR}"/>')
    s.append(f'<path d="M410 162 L580 162 L602 228 L410 228 Z" fill="{PANEL}" stroke="{HAIR}"/>')
    s.append(f'<rect x="170" y="236" width="460" height="86" fill="{PANEL}"/>')            # body
    s.append('<rect x="170" y="236" width="460" height="86"/>')
    s.append(f'<rect x="196" y="252" width="330" height="54" fill="#fff"/>')               # bed
    s.append('<rect x="196" y="252" width="330" height="54"/>')
    for x in range(210, 520, 26):                                                          # honeycomb hint
        s.append(f'<line x1="{x}" y1="256" x2="{x}" y2="302" stroke="{HAIR}" stroke-width="1"/>')
    s.append(f'<line x1="196" y1="262" x2="526" y2="262" stroke="{INK2}" stroke-width="1.4"/>')  # gantry
    s.append('<rect x="340" y="256" width="18" height="16"/>')                              # head
    s.append(f'<line x1="349" y1="272" x2="349" y2="292" stroke="{AMBER}" stroke-width="1.8"/>')  # beam
    s.append('<rect x="546" y="252" width="66" height="54"/>')                              # control panel
    s.append(f'<rect x="556" y="262" width="46" height="20" fill="{BLUE}" opacity=".18" stroke="none"/>')
    s.append('<path d="M206 322 L206 400 M594 322 L594 400"/>')                             # legs
    s.append(f'<circle cx="206" cy="410" r="10"/><circle cx="594" cy="410" r="10"/>')       # casters
    s.append(label(170, 120, "TOP LASER TOPI-1610TN", 13, INK, weight=600))
    s.append(label(170, 462, "CO2 FLATBED · SHEET CUTTING & ENGRAVING", 11, INK2))
    return s


PLATES = {
    "equip-creatbot-d600.svg": ("CreatBot D600 Pro 2 large-format FDM printer, front elevation", creatbot),
    "equip-bambu-x1e.svg":     ("Bambu Lab X1E printer with the AMS material unit on top, front elevation", bambu),
    "equip-raise3d-pro3.svg":  ("Raise3D Pro3 enclosed dual-extruder FDM printer, front elevation", raise3d),
    "equip-toplaser-1610.svg": ("TOP Laser TOPI-1610TN flatbed CO2 laser cutter with the lid raised, front elevation", toplaser),
}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for name, (alt, fn) in PLATES.items():
        body = "".join(fn())
        svg = HEAD.format(w=W, h=H, alt=esc(alt), ink=INK) + body + FOOT
        p = os.path.join(here, name)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(svg)
        print(f"{name:28s} {len(svg):6,d} bytes")
