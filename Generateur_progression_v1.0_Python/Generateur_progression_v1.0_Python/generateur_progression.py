#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'indicateurs de progression / Progress Indicator Generator
Crée de zéro une série de 101 images (0 à 100 %) de cercle ou de barre de
progression — creates from scratch a series of 101 progress circle or bar images.
Copyright © 2026 Mamadou Bâ Neige

Ce programme est un logiciel libre : vous pouvez le redistribuer et/ou le modifier
selon les termes de la GNU General Public License version 3 publiée par la Free
Software Foundation. Il est distribué SANS AUCUNE GARANTIE. Voir le fichier LICENSE.
This program is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License version 3 as published by the Free Software
Foundation. It is distributed WITHOUT ANY WARRANTY. See the LICENSE file.

Lancement / Launch: python generateur_progression.py   (ou double-clic / or double-click)
Fichiers / Files: generateur_progression.py, moteur_generateur.py, polices/, aide/, icone.ico
Dépendances / Requirements: pip install pillow   (tkinter ships with Python)
"""

import sys
import os
import json
import locale
import webbrowser
from pathlib import Path

from PIL import Image

import moteur_generateur as mg

# ------------------------------------------------------- Auteur et contacts
VERSION = "1.0"
AUTEUR = "Mamadou Bâ Neige"
ANNEE = "2026"
CONTACTS = {
    "E-mail": "mamadou.ba@ugb.edu.sn",
    "Téléphone": "+221 77 645 14 45",
    "YouTube": "https://www.youtube.com/@mamadoubapassioninformatique",
    "Site web": "https://neigeba.com/",
}

# ============================================================ Langues / i18n
TEXTES = {
    "fr": {
        "nom": "Générateur d'indicateurs de progression",
        "droits": "Licence GNU GPL v3.",
        "type_cercle": "Cercle",
        "type_barre": "Barre",
        "forme": "Forme",
        "taille": "Taille (px)",
        "epaisseur": "Épaisseur de l'anneau (px)",
        "marge": "Marge autour (px)",
        "bouts_ronds": "Bouts de l'arc arrondis",
        "sens": "Sens de remplissage",
        "horaire": "Horaire",
        "antihoraire": "Antihoraire",
        "largeur": "Largeur (px)",
        "hauteur": "Hauteur (px)",
        "rayon": "Rayon des coins (px)",
        "contour_ep": "Épaisseur du contour (px)",
        "bout_rond": "Bout du remplissage arrondi",
        "couleurs": "Couleurs",
        "arc": "Arc (pourcentage)",
        "piste": "Reste du cercle",
        "remplissage": "Remplissage (pourcentage)",
        "reste": "Reste de la barre",
        "contour": "Contour",
        "texte": "Texte",
        "fond": "Fond",
        "degrade": "Dégradé, 2e couleur :",
        "fond_transparent": "Fond transparent (PNG)",
        "choisir": "Choisir…",
        "titre_texte": "Texte",
        "texte_mode": "Affichage",
        "pourcent": "Pourcentage (ex. 42%)",
        "signe": "Signe % seul",
        "aucun": "Aucun texte",
        "texte_taille": "Taille du texte (px)",
        "police": "Police",
        "autre_police": "Autre…",
        "dlg_police": "Choisir une police (.ttf, .otf)",
        "modeles": "Modèles",
        "mod_creality": "Modèle Creality (92 × 92)",
        "mod_barre": "Modèle barre (252 × 24)",
        "mod_vb": "Vert / beige",
        "ouvrir_modele": "Ouvrir…",
        "enregistrer_modele": "Enregistrer…",
        "dlg_ouvrir": "Ouvrir un modèle",
        "dlg_enregistrer": "Enregistrer le modèle",
        "fichier_modele": "Modèle de générateur",
        "m_modele_err": "Ce fichier n'est pas un modèle valide :\n{e}",
        "apercu": "Aperçu",
        "pourcentage": "Pourcentage : {p} %",
        "fichiers": "Fichiers",
        "sortie": "Dossier de sortie :",
        "parcourir": "Parcourir…",
        "dlg_sortie": "Dossier où créer les images",
        "prefixe": "Préfixe",
        "debut": "Premier numéro",
        "suffixe": "Suffixe",
        "format": "Format",
        "exemple": "Noms : {a}  …  {b}",
        "generer": "Générer les 101 images",
        "aide": "Aide (F1)",
        "a_propos": "À propos",
        "contacts": "Contacts :",
        "E-mail": "E-mail",
        "Téléphone": "Téléphone",
        "YouTube": "YouTube",
        "Site web": "Site web",
        "st_pret": "Réglez la forme et les couleurs, puis choisissez le dossier de sortie.",
        "st_invalide": "Valeur invalide : {champ}",
        "st_progres": "{i}/{n}  {nom}",
        "st_termine": "Terminé : {n} images créées.",
        "st_modele": "Modèle appliqué : {m}",
        "t_manquant": "Dossier manquant",
        "m_sortie": "Choisissez le dossier de sortie.",
        "t_invalide": "Valeur invalide",
        "m_invalide": "Vérifiez le champ « {champ} ».",
        "t_attention": "Attention",
        "m_ecraser": "{n} image(s) portant les mêmes noms existent déjà dans ce dossier.\n"
                     "Les remplacer ?",
        "t_termine": "Terminé",
        "m_termine": "{n} images créées dans :\n{d}",
        "t_erreur": "Erreur",
        "t_aide": "Aide",
        "m_aide_absente": "Manuel introuvable :\n{p}\n\nPlacez le dossier « aide » "
                          "à côté du programme.",
        "apropos_desc": "Création de séries d'images de progression (0 à 100 %) :\n"
                        "cercles et barres.\n\n"
                        "Logiciel libre sous licence GNU GPL version 3 (fichier LICENSE),\n"
                        "fourni SANS AUCUNE GARANTIE.\n\n"
                        "Polices DejaVu : licence libre Bitstream Vera\n"
                        "(voir LICENCE_DejaVu.txt).",
        "version": "version",
        "manuel": "generateur_progression_manuel_fr.html",
    },
    "en": {
        "nom": "Progress Indicator Generator",
        "droits": "Licensed under the GNU GPL v3.",
        "type_cercle": "Circle",
        "type_barre": "Bar",
        "forme": "Shape",
        "taille": "Size (px)",
        "epaisseur": "Ring thickness (px)",
        "marge": "Outer margin (px)",
        "bouts_ronds": "Rounded arc ends",
        "sens": "Fill direction",
        "horaire": "Clockwise",
        "antihoraire": "Counterclockwise",
        "largeur": "Width (px)",
        "hauteur": "Height (px)",
        "rayon": "Corner radius (px)",
        "contour_ep": "Border thickness (px)",
        "bout_rond": "Rounded fill end",
        "couleurs": "Colors",
        "arc": "Arc (percentage)",
        "piste": "Rest of the circle",
        "remplissage": "Fill (percentage)",
        "reste": "Rest of the bar",
        "contour": "Border",
        "texte": "Text",
        "fond": "Background",
        "degrade": "Gradient, 2nd color:",
        "fond_transparent": "Transparent background (PNG)",
        "choisir": "Choose…",
        "titre_texte": "Text",
        "texte_mode": "Display",
        "pourcent": "Percentage (e.g. 42%)",
        "signe": "% sign only",
        "aucun": "No text",
        "texte_taille": "Text size (px)",
        "police": "Font",
        "autre_police": "Other…",
        "dlg_police": "Choose a font (.ttf, .otf)",
        "modeles": "Presets",
        "mod_creality": "Creality preset (92 × 92)",
        "mod_barre": "Bar preset (252 × 24)",
        "mod_vb": "Green / beige",
        "ouvrir_modele": "Open…",
        "enregistrer_modele": "Save…",
        "dlg_ouvrir": "Open a preset",
        "dlg_enregistrer": "Save the preset",
        "fichier_modele": "Generator preset",
        "m_modele_err": "This file is not a valid preset:\n{e}",
        "apercu": "Preview",
        "pourcentage": "Percentage: {p}%",
        "fichiers": "Files",
        "sortie": "Output folder:",
        "parcourir": "Browse…",
        "dlg_sortie": "Folder in which to create the images",
        "prefixe": "Prefix",
        "debut": "First number",
        "suffixe": "Suffix",
        "format": "Format",
        "exemple": "Names: {a}  …  {b}",
        "generer": "Generate the 101 images",
        "aide": "Help (F1)",
        "a_propos": "About",
        "contacts": "Contacts:",
        "E-mail": "E-mail",
        "Téléphone": "Phone",
        "YouTube": "YouTube",
        "Site web": "Website",
        "st_pret": "Set the shape and colors, then choose the output folder.",
        "st_invalide": "Invalid value: {champ}",
        "st_progres": "{i}/{n}  {nom}",
        "st_termine": "Done: {n} images created.",
        "st_modele": "Preset applied: {m}",
        "t_manquant": "Missing folder",
        "m_sortie": "Choose the output folder.",
        "t_invalide": "Invalid value",
        "m_invalide": "Check the \u201c{champ}\u201d field.",
        "t_attention": "Warning",
        "m_ecraser": "{n} image(s) with the same names already exist in this folder.\n"
                     "Replace them?",
        "t_termine": "Done",
        "m_termine": "{n} images created in:\n{d}",
        "t_erreur": "Error",
        "t_aide": "Help",
        "m_aide_absente": "Manual not found:\n{p}\n\nPut the \"aide\" folder "
                          "next to the program.",
        "apropos_desc": "Creation of progress image series (0 to 100%):\n"
                        "circles and bars.\n\n"
                        "Free software under the GNU GPL version 3 (LICENSE file),\n"
                        "provided WITHOUT ANY WARRANTY.\n\n"
                        "DejaVu fonts: free Bitstream Vera license\n"
                        "(see LICENCE_DejaVu.txt).",
        "version": "version",
        "manuel": "generateur_progression_manual_en.html",
    },
}

_langue = {"code": "fr"}


def tr(cle, **kw):
    txt = TEXTES[_langue["code"]].get(cle, TEXTES["fr"].get(cle, cle))
    return txt.format(**kw) if kw else txt


def copyright_txt():
    return f"© {ANNEE} {AUTEUR}. {tr('droits')}"


def langue_systeme():
    try:
        if sys.platform == "win32":
            import ctypes
            return "fr" if (ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0xFF) == 0x0C else "en"
    except Exception:
        pass
    for v in (os.environ.get("LANG"), os.environ.get("LC_ALL"), (locale.getlocale() or [None])[0]):
        if v:
            return "fr" if v.lower().startswith("fr") else "en"
    return "en"


def _fichier_config():
    base = os.environ.get("APPDATA") or str(Path.home())
    return Path(base) / "generateur_progression.json"


def lire_langue():
    try:
        code = json.loads(_fichier_config().read_text(encoding="utf-8")).get("langue")
        if code in TEXTES:
            return code
    except Exception:
        pass
    return langue_systeme()


def enregistrer_langue(code):
    try:
        _fichier_config().write_text(json.dumps({"langue": code}), encoding="utf-8")
    except Exception:
        pass


def chemin_manuel(code=None):
    code = code or _langue["code"]
    return mg.dossier_programme() / "aide" / TEXTES[code]["manuel"]


# Description des réglages : (clé, nature) ; nature = int, float, bool, sens
FORME = {
    "cercle": [("taille", int), ("epaisseur", float), ("marge", float),
               ("bouts_ronds", bool), ("sens", "sens")],
    "barre": [("largeur", int), ("hauteur", int), ("rayon", float),
              ("contour_ep", float), ("marge", float), ("bout_rond", bool)],
}
COULEURS = {
    "cercle": ["arc", "piste", "texte", "fond"],
    "barre": ["remplissage", "reste", "contour", "texte", "fond"],
}
COULEUR_DEGRADE = {"cercle": ("arc", "arc2"), "barre": ("remplissage", "remplissage2")}
LIMITES = {"taille": (8, 2000), "largeur": (8, 4000), "hauteur": (4, 2000),
           "epaisseur": (0.5, 1000), "marge": (0, 1000), "rayon": (0, 1000),
           "contour_ep": (0, 1000), "texte_taille": (1, 1000)}
APERCU = {"cercle": (300, 300), "barre": (300, 300)}


# =================================================================== Fenêtre
def lancer_interface():
    import tkinter as tk
    from tkinter import ttk, filedialog, colorchooser, messagebox
    from PIL import ImageTk

    root = tk.Tk()
    root.resizable(False, False)
    try:
        icone = mg.dossier_programme() / "icone.ico"
        if icone.exists():
            root.iconbitmap(default=str(icone))
    except Exception:
        pass

    traduits = []
    a_retraduire = []

    def T(widget, cle, option="text"):
        traduits.append((widget, cle, option))
        widget.config(**{option: tr(cle)})
        return widget

    def bouton_colore(parent, cle, commande, fond, texte, survol,
                      police=("Segoe UI", 9, "bold"), padx=10, pady=3):
        b = tk.Button(parent, command=commande, bg=fond, fg=texte,
                      activebackground=survol, activeforeground=texte,
                      disabledforeground="#555555", font=police, relief="flat",
                      bd=0, padx=padx, pady=pady, cursor="hand2", highlightthickness=0)
        b.bind("<Enter>", lambda e: b.config(bg=survol) if str(b["state"]) == "normal" else None)
        b.bind("<Leave>", lambda e: b.config(bg=fond))
        return T(b, cle)

    # ---------- Variables (un jeu par type, conservé quand on change de type)
    def creer_vars(reglages):
        v = {}
        for k, val in reglages.items():
            v[k] = tk.BooleanVar(value=val) if isinstance(val, bool) else tk.StringVar(value=str(val))
        return v

    V = {"cercle": creer_vars(mg.REGLAGES_CERCLE), "barre": creer_vars(mg.REGLAGES_BARRE)}
    v_type = tk.StringVar(value="cercle")
    v_pct = tk.IntVar(value=42)
    v_sortie = tk.StringVar()
    v_prefixe = tk.StringVar(value="")
    v_debut = tk.StringVar(value="0")
    v_suffixe = tk.StringVar(value="")
    v_format = tk.StringVar(value="png")
    v_statut = tk.StringVar()
    statut = {"cle": "st_pret", "kw": {}}
    photo = {"img": None}

    def set_statut(cle, **kw):
        statut["cle"], statut["kw"] = cle, kw
        v_statut.set(tr(cle, **kw))

    def lire_reglages(type_=None):
        """Valeurs actuelles, vérifiées ; renvoie (réglages, champ fautif)."""
        type_ = type_ or v_type.get()
        r = {}
        for k, var in V[type_].items():
            val = var.get()
            base = (mg.REGLAGES_CERCLE if type_ == "cercle" else mg.REGLAGES_BARRE)[k]
            try:
                if isinstance(base, bool):
                    r[k] = bool(val)
                elif isinstance(base, int):
                    r[k] = int(float(str(val).replace(",", ".")))
                elif isinstance(base, float):
                    r[k] = float(str(val).replace(",", "."))
                elif k in ("sens", "texte_mode", "police"):
                    r[k] = val
                else:                       # couleur
                    mg.hex_vers_rgb(val)
                    r[k] = "#" + str(val).strip().lstrip("#").upper()
            except Exception:
                return None, k
            if k in LIMITES and not (LIMITES[k][0] <= r[k] <= LIMITES[k][1]):
                return None, k
        return r, None

    # ---------- Barre du haut
    haut = tk.Frame(root)
    haut.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(8, 0))
    lbl_titre = tk.Label(haut, font=("Segoe UI", 12, "bold"), fg="#1C2433")
    lbl_titre.pack(side="left")
    zone_type = tk.Frame(haut, bg="#00A000", padx=1, pady=1)
    zone_type.pack(side="left", padx=20)
    btn_type = {}
    zone_langue = tk.Frame(haut, bg="#1F5FBF", padx=1, pady=1)
    zone_langue.pack(side="right")
    btn_langue = {}

    def ouvrir_aide(event=None):
        p = chemin_manuel()
        if not p.exists():
            autre = chemin_manuel("en" if _langue["code"] == "fr" else "fr")
            if autre.exists():
                p = autre
            else:
                messagebox.showerror(tr("t_aide"), tr("m_aide_absente", p=p), parent=root)
                return "break"
        webbrowser.open(p.as_uri())
        return "break"

    bouton_colore(haut, "aide", ouvrir_aide, fond="#1F5FBF", texte="#FFFFFF",
                  survol="#3B7BDB").pack(side="right", padx=(0, 10))
    root.bind_all("<F1>", ouvrir_aide)

    # ---------- Colonnes
    col_g = tk.Frame(root)
    col_g.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=6)
    col_m = tk.Frame(root)
    col_m.grid(row=1, column=1, sticky="nsew", padx=5, pady=6)
    col_d = tk.Frame(root)
    col_d.grid(row=1, column=2, sticky="nsew", padx=(5, 10), pady=6)

    cadre_forme = T(ttk.LabelFrame(col_g, padding=8), "forme")
    cadre_forme.pack(fill="x")
    cadre_texte = T(ttk.LabelFrame(col_g, padding=8), "titre_texte")
    cadre_texte.pack(fill="x", pady=(8, 0))
    cadre_modeles = T(ttk.LabelFrame(col_g, padding=8), "modeles")
    cadre_modeles.pack(fill="x", pady=(8, 0))
    cadre_coul = T(ttk.LabelFrame(col_m, padding=8), "couleurs")
    cadre_coul.pack(fill="x")
    cadre_apercu = T(ttk.LabelFrame(col_d, padding=8), "apercu")
    cadre_apercu.pack(fill="both", expand=True)

    def vider(cadre):
        for w in cadre.winfo_children():
            w.destroy()
        traduits[:] = [(w, c, o) for (w, c, o) in traduits if w.winfo_exists()]

    # ---------- Forme (reconstruite selon le type)
    def construire_forme():
        vider(cadre_forme)
        type_ = v_type.get()
        for r, (cle, nature) in enumerate(FORME[type_]):
            var = V[type_][cle]
            if nature is bool:
                T(ttk.Checkbutton(cadre_forme, variable=var), cle).grid(
                    row=r, column=0, columnspan=2, sticky="w", pady=2)
            elif nature == "sens":
                T(ttk.Label(cadre_forme), cle).grid(row=r, column=0, sticky="w", pady=2)
                f = ttk.Frame(cadre_forme)
                f.grid(row=r, column=1, sticky="w")
                for val in ("horaire", "antihoraire"):
                    T(ttk.Radiobutton(f, variable=var, value=val), val).pack(side="left")
            else:
                T(ttk.Label(cadre_forme), cle).grid(row=r, column=0, sticky="w", pady=2)
                ttk.Spinbox(cadre_forme, textvariable=var, width=8,
                            from_=LIMITES[cle][0], to=LIMITES[cle][1],
                            increment=1 if nature is int else 0.5,
                            command=planifier_apercu).grid(row=r, column=1, sticky="w", padx=6)

    # ---------- Couleurs (reconstruites selon le type)
    pastilles = {}

    def valider_couleur(cle):
        type_ = v_type.get()
        val = V[type_][cle].get()
        try:
            mg.hex_vers_rgb(val)
            if cle in pastilles and pastilles[cle].winfo_exists():
                pastilles[cle].config(bg="#" + val.strip().lstrip("#")[:6])
            return True
        except ValueError:
            return False

    def choisir_couleur(cle):
        type_ = v_type.get()
        actuelle = V[type_][cle].get()
        try:
            mg.hex_vers_rgb(actuelle)
        except ValueError:
            actuelle = "#808080"
        _, hx = colorchooser.askcolor(color=actuelle, title=tr(cle if cle in TEXTES["fr"] else "couleurs"),
                                      parent=root)
        if hx:
            V[type_][cle].set(hx.upper())
            valider_couleur(cle)

    def ligne_couleur(cadre, r, cle, libelle=None, col=0):
        if libelle is not None:
            T(ttk.Label(cadre), libelle).grid(row=r, column=col, sticky="w", pady=3)
        p = tk.Label(cadre, width=4, relief="solid", bd=1, cursor="hand2")
        p.grid(row=r, column=col + 1, padx=6)
        p.bind("<Button-1>", lambda e, c=cle: choisir_couleur(c))
        pastilles[cle] = p
        e = ttk.Entry(cadre, textvariable=V[v_type.get()][cle], width=9)
        e.grid(row=r, column=col + 2)
        e.bind("<Return>", lambda ev, c=cle: valider_couleur(c))
        e.bind("<FocusOut>", lambda ev, c=cle: valider_couleur(c))
        T(ttk.Button(cadre, command=lambda c=cle: choisir_couleur(c)), "choisir").grid(
            row=r, column=col + 3, padx=(6, 0))
        valider_couleur(cle)

    def construire_couleurs():
        vider(cadre_coul)
        pastilles.clear()
        type_ = v_type.get()
        principale, seconde = COULEUR_DEGRADE[type_]
        r = 0
        for cle in COULEURS[type_]:
            ligne_couleur(cadre_coul, r, cle, cle)
            r += 1
            if cle == principale:
                f = ttk.Frame(cadre_coul)
                f.grid(row=r, column=0, columnspan=4, sticky="w", padx=(14, 0), pady=(0, 4))
                T(ttk.Checkbutton(f, variable=V[type_]["degrade"]), "degrade").grid(
                    row=0, column=0, sticky="w")
                ligne_couleur(f, 0, seconde, None, col=0)
                r += 1
        T(ttk.Checkbutton(cadre_coul, variable=V[type_]["fond_transparent"]),
          "fond_transparent").grid(row=r, column=0, columnspan=4, sticky="w", pady=(6, 0))

    # ---------- Texte (variables du type courant)
    v_mode_aff = tk.StringVar()
    v_police_aff = tk.StringVar()
    MODES = ("pourcent", "signe", "aucun")

    def construire_texte():
        vider(cadre_texte)
        type_ = v_type.get()
        T(ttk.Label(cadre_texte), "texte_mode").grid(row=0, column=0, sticky="w", pady=2)
        cb_mode = ttk.Combobox(cadre_texte, textvariable=v_mode_aff, state="readonly", width=19)
        cb_mode.grid(row=0, column=1, columnspan=2, sticky="w", padx=6)
        T(ttk.Label(cadre_texte), "texte_taille").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Spinbox(cadre_texte, textvariable=V[type_]["texte_taille"], width=8, from_=1,
                    to=1000, increment=1, command=planifier_apercu).grid(
            row=1, column=1, sticky="w", padx=6)
        T(ttk.Label(cadre_texte), "police").grid(row=2, column=0, sticky="w", pady=2)
        cb_pol = ttk.Combobox(cadre_texte, textvariable=v_police_aff, width=19,
                              values=list(mg.POLICES), state="readonly")
        cb_pol.grid(row=2, column=1, sticky="w", padx=6)
        T(ttk.Button(cadre_texte, command=autre_police), "autre_police").grid(row=2, column=2)

        def maj_listes():
            cb_mode.config(values=[tr(m) for m in MODES])
            v_mode_aff.set(tr(V[v_type.get()]["texte_mode"].get()))
        maj_listes()
        a_retraduire.append(maj_listes)
        pol = V[type_]["police"].get()
        v_police_aff.set(pol if pol in mg.POLICES else Path(pol).name)
        cb_mode.bind("<<ComboboxSelected>>", lambda e: choix_mode(cb_mode.current()))
        cb_pol.bind("<<ComboboxSelected>>", lambda e: V[v_type.get()]["police"].set(v_police_aff.get()))

    def choix_mode(i):
        if i >= 0:
            V[v_type.get()]["texte_mode"].set(MODES[i])

    def autre_police():
        f = filedialog.askopenfilename(title=tr("dlg_police"), parent=root,
                                       filetypes=[("TrueType / OpenType", "*.ttf *.otf *.ttc"),
                                                  ("*", "*.*")])
        if f:
            V[v_type.get()]["police"].set(f)
            v_police_aff.set(Path(f).name)

    # ---------- Modèles
    def appliquer_modele(reglages, nom_cle, debut=None, suffixe=None):
        type_ = v_type.get()
        for k, val in reglages.items():
            if k in V[type_]:
                V[type_][k].set(val)
        if debut is not None:
            v_debut.set(str(debut))
            v_suffixe.set(suffixe)
        reconstruire()
        set_statut("st_modele", m=tr(nom_cle))

    def construire_modeles():
        vider(cadre_modeles)
        type_ = v_type.get()
        f = ttk.Frame(cadre_modeles)
        f.pack(anchor="w")
        if type_ == "cercle":
            bord = tk.Frame(f, bg="#358BDE", padx=2, pady=2)
            bord.pack(side="left")
            bouton_colore(bord, "mod_creality",
                          lambda: appliquer_modele(mg.MODELE_CREALITY, "mod_creality", 2527, "_92x92"),
                          fond="#101C20", texte="#FFC64A", survol="#1E3038").pack()
            vb = mg.REGLAGES_CERCLE
        else:
            bord = tk.Frame(f, bg="#FFFFFF", padx=2, pady=2)
            bord.pack(side="left")
            bouton_colore(bord, "mod_barre",
                          lambda: appliquer_modele(mg.MODELE_BARRE, "mod_barre", 0, ""),
                          fond="#820000", texte="#FFFFFF", survol="#9A1A1A").pack()
            vb = mg.REGLAGES_BARRE
        bord2 = tk.Frame(f, bg="#00C800", padx=2, pady=2)
        bord2.pack(side="left", padx=8)
        bouton_colore(bord2, "mod_vb", lambda: appliquer_modele(vb, "mod_vb", 0, ""),
                      fond="#E8D6B0", texte="#2B2416", survol="#F3E6C8").pack()
        f2 = ttk.Frame(cadre_modeles)
        f2.pack(anchor="w", pady=(8, 0))
        T(ttk.Button(f2, command=ouvrir_modele), "ouvrir_modele").pack(side="left")
        T(ttk.Button(f2, command=enregistrer_modele), "enregistrer_modele").pack(side="left", padx=6)

    def enregistrer_modele():
        r, faute = lire_reglages()
        if faute:
            messagebox.showerror(tr("t_invalide"), tr("m_invalide", champ=tr(faute)), parent=root)
            return
        f = filedialog.asksaveasfilename(title=tr("dlg_enregistrer"), parent=root,
                                         defaultextension=".json",
                                         filetypes=[(tr("fichier_modele"), "*.json")])
        if not f:
            return
        donnees = {"programme": "generateur_progression", "version": VERSION,
                   "type": v_type.get(), "reglages": r,
                   "fichiers": {"prefixe": v_prefixe.get(), "debut": v_debut.get(),
                                "suffixe": v_suffixe.get(), "format": v_format.get()}}
        Path(f).write_text(json.dumps(donnees, indent=2, ensure_ascii=False), encoding="utf-8")

    def ouvrir_modele():
        f = filedialog.askopenfilename(title=tr("dlg_ouvrir"), parent=root,
                                       filetypes=[(tr("fichier_modele"), "*.json")])
        if not f:
            return
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
            type_ = d["type"]
            if type_ not in ("cercle", "barre"):
                raise ValueError(type_)
            for k, val in d["reglages"].items():
                if k in V[type_]:
                    V[type_][k].set(val)
            fi = d.get("fichiers", {})
            v_prefixe.set(fi.get("prefixe", ""))
            v_debut.set(str(fi.get("debut", 0)))
            v_suffixe.set(fi.get("suffixe", ""))
            v_format.set(fi.get("format", "png"))
        except Exception as ex:
            messagebox.showerror(tr("t_erreur"), tr("m_modele_err", e=ex), parent=root)
            return
        changer_type(type_)
        set_statut("st_modele", m=Path(f).name)

    # ---------- Aperçu
    case = tk.Frame(cadre_apercu, bg="#cccccc")
    case.pack()
    case.pack_propagate(False)
    lbl_img = tk.Label(case, bg="#cccccc", bd=0)
    lbl_img.place(relx=0.5, rely=0.5, anchor="center")
    lbl_pct = tk.Label(cadre_apercu, font=("Segoe UI", 10, "bold"))
    lbl_pct.pack(pady=(8, 0))
    curseur = ttk.Scale(cadre_apercu, from_=0, to=100, orient="horizontal", length=300,
                        command=lambda v: (v_pct.set(int(round(float(v)))), planifier_apercu()))
    curseur.pack(fill="x", pady=(2, 0))

    def damier(taille, pas=8):
        w, h = taille
        im = Image.new("RGB", (w, h), (255, 255, 255))
        px = im.load()
        for y in range(h):
            for x in range(w):
                if ((x // pas) + (y // pas)) % 2:
                    px[x, y] = (205, 205, 205)
        return im

    attente = {"id": None}

    def planifier_apercu(*_):
        if attente["id"]:
            root.after_cancel(attente["id"])
        attente["id"] = root.after(120, maj_apercu)

    def maj_apercu():
        attente["id"] = None
        lbl_pct.config(text=tr("pourcentage", p=v_pct.get()))
        maj_exemple()
        r, faute = lire_reglages()
        if faute:
            set_statut("st_invalide", champ=tr(faute))
            return
        if statut["cle"] == "st_invalide":
            set_statut("st_pret")
        type_ = v_type.get()
        try:
            img = mg.dessiner(type_, r, v_pct.get())
        except Exception as ex:
            v_statut.set(str(ex))
            return
        CL, CH = APERCU[type_]
        ech = min(CL / img.width, CH / img.height)
        if ech >= 1:
            z = int(ech)
            img = img.resize((img.width * z, img.height * z), Image.NEAREST)
        else:
            img = img.resize((max(1, round(img.width * ech)), max(1, round(img.height * ech))),
                             Image.LANCZOS)
        if img.mode == "RGBA":
            fond = damier(img.size)
            fond.paste(img, (0, 0), img)
            img = fond
        photo["img"] = ImageTk.PhotoImage(img)
        lbl_img.config(image=photo["img"])

    # ---------- Fichiers
    cadre_fich = T(ttk.LabelFrame(col_m, padding=8), "fichiers")
    cadre_fich.pack(fill="x", pady=(8, 0))
    T(ttk.Label(cadre_fich), "sortie").grid(row=0, column=0, sticky="w")
    ttk.Entry(cadre_fich, textvariable=v_sortie, width=34).grid(row=1, column=0, columnspan=3,
                                                                 sticky="w", pady=2)

    def choisir_sortie():
        d = filedialog.askdirectory(title=tr("dlg_sortie"), parent=root)
        if d:
            v_sortie.set(d)

    T(ttk.Button(cadre_fich, command=choisir_sortie), "parcourir").grid(row=1, column=3, padx=(6, 0))
    for c, (cle, var, larg) in enumerate([("prefixe", v_prefixe, 10), ("debut", v_debut, 8),
                                          ("suffixe", v_suffixe, 10)]):
        T(ttk.Label(cadre_fich), cle).grid(row=2, column=c, sticky="w", pady=(6, 0))
        ttk.Entry(cadre_fich, textvariable=var, width=larg).grid(row=3, column=c, sticky="w", padx=(0, 6))
    T(ttk.Label(cadre_fich), "format").grid(row=2, column=3, sticky="w", pady=(6, 0))
    ttk.Combobox(cadre_fich, textvariable=v_format, values=["png", "jpg", "bmp"],
                 state="readonly", width=5).grid(row=3, column=3, sticky="w")
    lbl_exemple = ttk.Label(cadre_fich, foreground="#555555")
    lbl_exemple.grid(row=4, column=0, columnspan=4, sticky="w", pady=(6, 0))

    def debut_int():
        try:
            return int(v_debut.get())
        except ValueError:
            return None

    def maj_exemple(*_):
        d = debut_int()
        if d is None:
            lbl_exemple.config(text=tr("st_invalide", champ=tr("debut")))
            return
        ext = v_format.get()
        lbl_exemple.config(text=tr("exemple", a=mg.nom_fichier(v_prefixe.get(), d, v_suffixe.get(), ext),
                                   b=mg.nom_fichier(v_prefixe.get(), d + 100, v_suffixe.get(), ext)))

    for var in (v_prefixe, v_debut, v_suffixe, v_format):
        var.trace_add("write", maj_exemple)

    # ---------- Bas : génération
    bas = ttk.Frame(root, padding=(10, 2, 10, 8))
    bas.grid(row=2, column=0, columnspan=3, sticky="ew")
    barre = ttk.Progressbar(bas, length=320, mode="determinate")
    barre.pack(side="left")
    ttk.Label(bas, textvariable=v_statut, width=56).pack(side="left", padx=8)

    def generer():
        r, faute = lire_reglages()
        if faute:
            messagebox.showerror(tr("t_invalide"), tr("m_invalide", champ=tr(faute)), parent=root)
            return
        d = debut_int()
        if d is None or d < 0:
            messagebox.showerror(tr("t_invalide"), tr("m_invalide", champ=tr("debut")), parent=root)
            return
        sortie = v_sortie.get().strip()
        if not sortie:
            messagebox.showwarning(tr("t_manquant"), tr("m_sortie"), parent=root)
            return
        ext = v_format.get()
        if r.get("fond_transparent") and ext != "png":
            r["fond_transparent"] = False        # seul le PNG garde la transparence
        existants = [n for n in range(101)
                     if (Path(sortie) / mg.nom_fichier(v_prefixe.get(), d + n, v_suffixe.get(), ext)).exists()]
        if existants and not messagebox.askyesno(tr("t_attention"),
                                                 tr("m_ecraser", n=len(existants)), parent=root):
            return

        def prog(i, n, nom):
            barre["maximum"] = n
            barre["value"] = i
            set_statut("st_progres", i=i, n=n, nom=nom)
            root.update_idletasks()

        bouton.config(state="disabled")
        try:
            n = mg.generer(v_type.get(), r, sortie, v_prefixe.get(), d, v_suffixe.get(), ext, prog)
        except Exception as ex:
            messagebox.showerror(tr("t_erreur"), str(ex), parent=root)
            return
        finally:
            bouton.config(state="normal")
        set_statut("st_termine", n=n)
        messagebox.showinfo(tr("t_termine"), tr("m_termine", n=n, d=sortie), parent=root)

    bouton = bouton_colore(bas, "generer", generer, fond="#00FF00", texte="#000000",
                           survol="#5CFF5C", police=("Segoe UI", 11, "bold"), padx=16, pady=6)
    bouton.pack(side="right")

    # ---------- Pied : copyright et contacts
    ttk.Separator(root).grid(row=3, column=0, columnspan=3, sticky="ew", padx=10)
    pied = tk.Frame(root)
    pied.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10, pady=(4, 2))
    lbl_copy = tk.Label(pied, fg="#444444", font=("Segoe UI", 9))
    lbl_copy.pack(side="left")

    def lien(cle, val):
        if cle == "E-mail":
            return "mailto:" + val
        if cle in ("YouTube", "Site web"):
            return val if val.startswith("http") else "https://" + val
        return None

    contacts = [(k, v.strip()) for k, v in CONTACTS.items() if v.strip()]
    ligne2 = tk.Frame(root)
    lbls_contacts = []
    if contacts:
        ligne2.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 8))
        T(tk.Label(ligne2, fg="#444444", font=("Segoe UI", 9)), "contacts").grid(row=0, column=0, sticky="nw")
    for i, (cle, val) in enumerate(contacts):
        url = lien(cle, val)
        court = val.split("://", 1)[-1]
        court = (court[4:] if court.startswith("www.") else court).rstrip("/")
        l = tk.Label(ligne2, font=("Segoe UI", 9, "underline" if url else ""),
                     fg="#1F5FBF" if url else "#444444", cursor="hand2" if url else "")
        if url:
            l.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
        l.grid(row=i // 2, column=1 + i % 2, sticky="w", padx=(10, 10))
        lbls_contacts.append((l, cle, court))

    def a_propos():
        sep = " : " if _langue["code"] == "fr" else ": "
        lignes = [f"{tr('nom')}  —  {tr('version')} {VERSION}", "", tr("apropos_desc"), "",
                  copyright_txt()]
        if contacts:
            lignes += ["", tr("contacts")] + [f"   {tr(k)}{sep}{v}" for k, v in contacts]
        messagebox.showinfo(tr("a_propos"), "\n".join(lignes), parent=root)

    T(tk.Button(pied, command=a_propos, relief="flat", bd=0, fg="#1F5FBF",
                cursor="hand2", font=("Segoe UI", 9)), "a_propos").pack(side="left", padx=12)

    # ---------- Type et reconstruction
    def reconstruire():
        a_retraduire[:] = [f for f in a_retraduire if getattr(f, "__name__", "") != "maj_listes"]
        construire_forme()
        construire_couleurs()
        construire_texte()
        construire_modeles()
        CL, CH = APERCU[v_type.get()]
        case.config(width=CL, height=CH)
        planifier_apercu()

    def changer_type(type_):
        v_type.set(type_)
        for c, b in btn_type.items():
            actif = c == type_
            b.config(bg="#00A000" if actif else "#FFFFFF", fg="#FFFFFF" if actif else "#006400")
        reconstruire()

    for type_ in ("cercle", "barre"):
        b = tk.Button(zone_type, width=8, relief="flat", bd=0, font=("Segoe UI", 9, "bold"),
                      cursor="hand2", highlightthickness=0, activebackground="#00C000",
                      activeforeground="#FFFFFF", command=lambda t=type_: changer_type(t))
        T(b, "type_" + type_).pack(side="left")
        btn_type[type_] = b

    # Toute modification d'un réglage met l'aperçu à jour
    for jeu in V.values():
        for var in jeu.values():
            var.trace_add("write", planifier_apercu)

    # ---------- Langue
    def changer_langue(code):
        _langue["code"] = code
        enregistrer_langue(code)
        traduits[:] = [(w, c, o) for (w, c, o) in traduits if w.winfo_exists()]
        for w, cle, opt in traduits:
            w.config(**{opt: tr(cle)})
        root.title(f"{tr('nom')} — {copyright_txt()}")
        lbl_titre.config(text=tr("nom"))
        for f in list(a_retraduire):
            f()
        lbl_copy.config(text=f"{tr('nom')} v{VERSION}  —  {copyright_txt()}")
        sep = " : " if code == "fr" else ": "
        for l, cle, val in lbls_contacts:
            l.config(text=f"{tr(cle)}{sep}{val}")
        v_statut.set(tr(statut["cle"], **statut["kw"]))
        lbl_pct.config(text=tr("pourcentage", p=v_pct.get()))
        maj_exemple()
        for c, b in btn_langue.items():
            actif = c == code
            b.config(bg="#1F5FBF" if actif else "#FFFFFF", fg="#FFFFFF" if actif else "#1F5FBF")

    for code in ("fr", "en"):
        b = tk.Button(zone_langue, text=code.upper(), width=3, relief="flat", bd=0,
                      font=("Segoe UI", 9, "bold"), cursor="hand2",
                      activebackground="#3B7BDB", activeforeground="#FFFFFF",
                      highlightthickness=0, command=lambda c=code: changer_langue(c))
        b.pack(side="left")
        btn_langue[code] = b

    set_statut("st_pret")
    curseur.set(v_pct.get())
    changer_type("cercle")
    changer_langue(_langue["code"])
    root.mainloop()


def main():
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")
    args = sys.argv[1:]
    code = None
    if "--lang" in args:
        i = args.index("--lang")
        if i + 1 < len(args):
            code = args[i + 1].lower()[:2]
    _langue["code"] = code if code in TEXTES else lire_langue()
    lancer_interface()


if __name__ == "__main__":
    main()
