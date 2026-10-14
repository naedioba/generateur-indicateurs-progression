# -*- coding: utf-8 -*-
"""
Moteur du générateur — dessine des cercles et des barres de progression
à partir de zéro. Utilisé par generateur_progression.py.
Copyright © 2026 Mamadou Bâ Neige

Ce programme est un logiciel libre : vous pouvez le redistribuer et/ou le modifier
selon les termes de la GNU General Public License version 3 publiée par la Free
Software Foundation. Il est distribué SANS AUCUNE GARANTIE. Voir le fichier LICENSE.
This program is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License version 3 as published by the Free Software
Foundation. It is distributed WITHOUT ANY WARRANTY. See the LICENSE file.
"""

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SUR = 4   # sur-échantillonnage : on dessine 4 fois plus grand, puis on réduit

# Polices fournies avec le logiciel (dossier « polices »)
POLICES = {
    "DejaVu Sans": "DejaVuSans.ttf",
    "DejaVu Sans Bold": "DejaVuSans-Bold.ttf",
    "DejaVu Sans Condensed": "DejaVuSansCondensed.ttf",
    "DejaVu Sans Condensed Bold": "DejaVuSansCondensed-Bold.ttf",
}

# ------------------------------------------------------------ Réglages types
REGLAGES_CERCLE = {
    "taille": 92, "epaisseur": 11, "marge": 0, "bouts_ronds": True,
    "sens": "horaire",
    "arc": "#00FF00", "degrade": False, "arc2": "#008800",
    "piste": "#E8D6B0", "fond": "#000808", "fond_transparent": False,
    "texte_mode": "pourcent", "texte": "#FFC64A", "texte_taille": 15,
    "police": "DejaVu Sans",
}
REGLAGES_BARRE = {
    "largeur": 252, "hauteur": 24, "rayon": 4.5, "contour_ep": 1, "marge": 0,
    "bout_rond": False,
    "remplissage": "#00FF00", "degrade": False, "remplissage2": "#008800",
    "reste": "#E8D6B0", "contour": "#FFFFFF", "fond": "#000000",
    "fond_transparent": False,
    "texte_mode": "aucun", "texte": "#000000", "texte_taille": 14,
    "police": "DejaVu Sans Bold",
}
# Modèles prêts à l'emploi
MODELE_CREALITY = {**REGLAGES_CERCLE, "arc": "#39ACDE", "degrade": True, "arc2": "#3163DE",
                   "piste": "#101C20", "fond": "#000808", "texte": "#FFC64A",
                   "texte_taille": 15, "police": "DejaVu Sans"}
MODELE_BARRE = {**REGLAGES_BARRE, "remplissage": "#820000", "reste": "#000000",
                "contour": "#FFFFFF", "fond": "#000000", "texte_mode": "aucun"}


def hex_vers_rgb(h):
    h = str(h).strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"Couleur invalide : #{h}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def dossier_programme():
    if getattr(sys, "_MEIPASS", None):
        return Path(sys._MEIPASS)
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def charger_police(nom, taille_px):
    """Police fournie, ou fichier .ttf/.otf choisi par l'utilisateur."""
    taille_px = max(1, int(round(taille_px)))
    chemin = POLICES.get(nom)
    essais = []
    if chemin:
        essais.append(dossier_programme() / "polices" / chemin)
    else:
        essais.append(Path(nom))
    for p in essais:
        try:
            return ImageFont.truetype(str(p), taille_px)
        except Exception:
            pass
    try:
        return ImageFont.truetype("DejaVuSans.ttf", taille_px)
    except Exception:
        return ImageFont.load_default()


def _texte(mode, pct):
    if mode == "pourcent":
        return f"{pct}%"
    if mode == "signe":
        return "%"
    return ""


def _degrade(taille, c1, c2):
    """Image en dégradé vertical, de c1 (haut) à c2 (bas)."""
    w, h = taille
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        col.putpixel((0, y), tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2)))
    return col.resize((w, h))


def _composer(taille, fond, transparent, calques):
    """Assemble les calques (couleur ou image, masque) sur le fond, puis réduit."""
    W, H = taille
    if transparent:
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    else:
        img = Image.new("RGBA", (W, H), hex_vers_rgb(fond) + (255,))
    for source, masque in calques:
        if isinstance(source, Image.Image):
            couche = source.convert("RGBA")
        else:
            couche = Image.new("RGBA", (W, H), hex_vers_rgb(source) + (255,))
        couche.putalpha(masque)
        img = Image.alpha_composite(img, couche)
    final = (W // SUR, H // SUR)
    # réduction en alpha prémultiplié : pas de liseré sombre sur fond transparent
    img = img.convert("RGBa").resize(final, Image.LANCZOS).convert("RGBA")
    return img if transparent else img.convert("RGB")


def _masque_texte(taille, txt, police, centre):
    m = Image.new("L", taille, 0)
    if txt:
        ImageDraw.Draw(m).text(centre, txt, font=police, fill=255, anchor="mm")
    return m


def dessiner_cercle(r, pct):
    """Image d'un cercle de progression à pct % (0 à 100)."""
    S = SUR
    t = int(r["taille"])
    W = H = t * S
    c = W / 2
    R = t * S / 2 - float(r["marge"]) * S
    e = max(0.5, float(r["epaisseur"])) * S
    e = min(e, R)
    rm = R - e / 2                          # rayon au milieu de l'anneau

    anneau = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(anneau)
    d.ellipse([c - R, c - R, c + R, c + R], fill=255)
    d.ellipse([c - R + e, c - R + e, c + R - e, c + R - e], fill=0)

    arc = Image.new("L", (W, H), 0)
    if pct > 0:
        da = Image.new("L", (W, H), 0)
        dd = ImageDraw.Draw(da)
        balayage = 360 * min(pct, 100) / 100
        if r["sens"] == "horaire":
            a0, a1 = -90, -90 + balayage
        else:
            a0, a1 = -90 - balayage, -90
        if pct >= 100:
            dd.ellipse([c - R, c - R, c + R, c + R], fill=255)
        else:
            dd.pieslice([c - R, c - R, c + R, c + R], a0, a1, fill=255)
        arc = Image.composite(da, Image.new("L", (W, H), 0), anneau)
        if r["bouts_ronds"] and pct < 100:
            da2 = ImageDraw.Draw(arc)
            for a in (a0, a1):
                x = c + rm * math.cos(math.radians(a))
                y = c + rm * math.sin(math.radians(a))
                da2.ellipse([x - e / 2, y - e / 2, x + e / 2, y + e / 2], fill=255)

    piste = Image.composite(Image.new("L", (W, H), 255), Image.new("L", (W, H), 0), anneau)
    if r["degrade"]:
        src_arc = _degrade((W, H), hex_vers_rgb(r["arc"]), hex_vers_rgb(r["arc2"]))
    else:
        src_arc = r["arc"]
    police = charger_police(r["police"], float(r["texte_taille"]) * S)
    mtxt = _masque_texte((W, H), _texte(r["texte_mode"], pct), police, (c, c))
    return _composer((W, H), r["fond"], r["fond_transparent"],
                     [(r["piste"], piste), (src_arc, arc), (r["texte"], mtxt)])


def dessiner_barre(r, pct):
    """Image d'une barre de progression à pct % (0 à 100)."""
    S = SUR
    W, H = int(r["largeur"]) * S, int(r["hauteur"]) * S
    m = float(r["marge"]) * S
    t = max(0.0, float(r["contour_ep"])) * S
    rad = max(0.0, float(r["rayon"])) * S
    x0, y0, x1, y1 = m, m, W - m, H - m
    rad = min(rad, (x1 - x0) / 2, (y1 - y0) / 2)

    def rrect(masque, box, rr, val):
        bx0, by0, bx1, by1 = box
        if bx1 - bx0 <= 0 or by1 - by0 <= 0:
            return
        rr = max(0, min(rr, (bx1 - bx0) / 2, (by1 - by0) / 2))
        ImageDraw.Draw(masque).rounded_rectangle([bx0, by0, bx1 - 1, by1 - 1], radius=rr, fill=val)

    ext = Image.new("L", (W, H), 0)
    rrect(ext, (x0, y0, x1, y1), rad, 255)
    inte = Image.new("L", (W, H), 0)
    ix0, iy0, ix1, iy1 = x0 + t, y0 + t, x1 - t, y1 - t
    ri = max(rad - t, 0)
    rrect(inte, (ix0, iy0, ix1, iy1), ri, 255)
    contour = Image.composite(Image.new("L", (W, H), 0), ext, inte)   # ext moins int

    remp = Image.new("L", (W, H), 0)
    if pct > 0:
        xf = ix0 + (ix1 - ix0) * min(pct, 100) / 100
        if r["bout_rond"]:
            rrect(remp, (ix0, iy0, xf, iy1), (iy1 - iy0) / 2, 255)
        else:
            ImageDraw.Draw(remp).rectangle([ix0, iy0, xf - 1, iy1 - 1], fill=255)
        remp = Image.composite(remp, Image.new("L", (W, H), 0), inte)
    reste = Image.composite(Image.new("L", (W, H), 0), inte, remp)

    if r["degrade"]:
        src = _degrade((W, H), hex_vers_rgb(r["remplissage"]), hex_vers_rgb(r["remplissage2"]))
    else:
        src = r["remplissage"]
    police = charger_police(r["police"], float(r["texte_taille"]) * S)
    mtxt = _masque_texte((W, H), _texte(r["texte_mode"], pct), police, (W / 2, H / 2))
    return _composer((W, H), r["fond"], r["fond_transparent"],
                     [(r["contour"], contour), (r["reste"], reste), (src, remp),
                      (r["texte"], mtxt)])


def dessiner(type_, r, pct):
    return dessiner_cercle(r, pct) if type_ == "cercle" else dessiner_barre(r, pct)


def nom_fichier(prefixe, numero, suffixe, extension):
    return f"{prefixe}{numero}{suffixe}.{extension}"


def generer(type_, r, dossier, prefixe="", debut=0, suffixe="", extension="png",
            progression=None):
    """Génère les 101 images (0 à 100 %) dans le dossier ; renvoie leur nombre."""
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    for pct in range(101):
        img = dessiner(type_, r, pct)
        f = dossier / nom_fichier(prefixe, int(debut) + pct, suffixe, extension)
        if extension in ("jpg", "jpeg"):
            img.convert("RGB").save(f, quality=95, subsampling=0)
        else:
            img.save(f)
        if progression:
            progression(pct + 1, 101, f.name)
    return 101
