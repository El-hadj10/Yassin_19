# visual/bouclier.py
# Rendu SVG/Matplotlib polar du Bouclier de Yassin × 19
# Couche 1 : cercle polaire, 19 secteurs (anges), versets mult-19 en or
# Couche 2 : noyau central (يس + 7 résiduels)
# Couche 3 : intensité de pulsation Ya/Sin par secteur

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")  # pas d'affichage GUI — export fichier
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Polices arabes via matplotlib (pas de reshaper requis pour le SVG export)
plt.rcParams["font.family"] = ["DejaVu Sans", "Noto Naskh Arabic"]

# ── Couleurs ──────────────────────────────────────────────────────────────────
COLOR_BG       = "#0a0a1a"   # fond nuit
COLOR_SECTOR   = "#1a1a3a"   # secteur normal
COLOR_GOLDEN   = "#FFD700"   # verset multiple de 19 (or)
COLOR_CORE     = "#2a0a0a"   # noyau central
COLOR_SEAL     = "#C0A060"   # يس central
COLOR_TEXT     = "#e0d8c0"   # texte clair
COLOR_ANGEL    = "#4466aa"   # arc ange
COLOR_PULSE_LO = "#1a3a5a"   # pulsation basse (peu de ي/س)
COLOR_PULSE_HI = "#00aaff"   # pulsation haute (beaucoup de ي/س)

TOTAL_ANGELS = 19
OUTPUT_FILE  = "bouclier_yassin_19.svg"


def _ya_sin_color(ya: int, sin: int, max_val: int) -> str:
    """Retourne une couleur interpolée selon l'intensité Ya+Sin du secteur."""
    if max_val == 0:
        return COLOR_PULSE_LO
    ratio = min((ya + sin) / max_val, 1.0)
    r1, g1, b1 = 0x1a, 0x3a, 0x5a
    r2, g2, b2 = 0x00, 0xaa, 0xff
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    return f"#{r:02x}{g:02x}{b:02x}"


def draw_shield(sectors_data: dict, stats: dict, output: str = OUTPUT_FILE) -> str:
    """
    Génère le Bouclier de Yassin en SVG.

    Parameters
    ----------
    sectors_data : dict  — sortie de core.structure.build_sectors()
    stats        : dict  — sortie de core.analyzer.global_stats()
    output       : str   — chemin du fichier SVG de sortie

    Returns
    -------
    str — chemin absolu du fichier généré
    """
    sectors = sectors_data["sectors"]
    core    = sectors_data["core"]

    fig = plt.figure(figsize=(14, 14), facecolor=COLOR_BG)
    ax  = fig.add_subplot(111, projection="polar")
    ax.set_facecolor(COLOR_BG)
    ax.set_theta_zero_location("N")   # 0° en haut
    ax.set_theta_direction(-1)        # sens horaire (comme les sourates)
    ax.set_axis_off()

    theta_step = 2 * math.pi / TOTAL_ANGELS  # angle par secteur

    # Calcul de l'intensité Ya+Sin max pour la normalisation couleur
    sector_ya_sin = []
    for s in sectors:
        ya  = sum(r["ya_count"]  for r in s["verses"])
        sin = sum(r["sin_count"] for r in s["verses"])
        sector_ya_sin.append(ya + sin)
    max_ya_sin = max(sector_ya_sin) if sector_ya_sin else 1

    # ── Dessin des 19 secteurs ─────────────────────────────────────────────
    for idx, s in enumerate(sectors):
        theta_start = idx * theta_step
        theta_end   = theta_start + theta_step
        thetas      = np.linspace(theta_start, theta_end, 60)

        has_golden  = any(r["mult_19"] for r in s["verses"])
        pulse_color = _ya_sin_color(
            sum(r["ya_count"]  for r in s["verses"]),
            sum(r["sin_count"] for r in s["verses"]),
            max_ya_sin
        )

        # Remplissage du secteur (anneau entre r=0.35 et r=1.0)
        r_inner = np.full_like(thetas, 0.35)
        r_outer = np.full_like(thetas, 1.00)

        fill_color = COLOR_GOLDEN if has_golden else pulse_color
        alpha      = 0.85 if has_golden else 0.55

        ax.fill_between(thetas, r_inner, r_outer,
                        color=fill_color, alpha=alpha, linewidth=0)

        # Bordure d'arc extérieur
        ax.plot(thetas, r_outer,
                color=COLOR_GOLDEN if has_golden else COLOR_ANGEL,
                linewidth=1.2 if has_golden else 0.6, alpha=0.9)

        # Ligne radiale de séparation
        ax.plot([theta_start, theta_start], [0.35, 1.0],
                color="#334466", linewidth=0.5, alpha=0.7)

        # Numéro de l'ange
        theta_mid = theta_start + theta_step / 2
        ax.text(theta_mid, 1.10,
                f"{s['angel']}",
                ha="center", va="center",
                color=COLOR_GOLDEN if has_golden else COLOR_TEXT,
                fontsize=7, fontweight="bold")

        # Numéros des versets du secteur
        verse_nums = " · ".join(str(r["num"]) for r in s["verses"])
        ax.text(theta_mid, 0.68,
                verse_nums,
                ha="center", va="center",
                color=COLOR_TEXT, fontsize=5.5, alpha=0.8)

    # ── Noyau central (يس + 7 résiduels) ──────────────────────────────────
    core_circle = plt.Circle((0, 0), 0.35,
                              transform=ax.transData._b,
                              color=COLOR_CORE, zorder=5)
    # On dessine le noyau via un patch polaire
    thetas_full = np.linspace(0, 2 * math.pi, 200)
    ax.fill(thetas_full, np.full_like(thetas_full, 0.35),
            color=COLOR_CORE, alpha=0.95, zorder=5)

    # Sceau يس au centre
    ax.text(0, 0, "يس",
            ha="center", va="center",
            color=COLOR_SEAL,
            fontsize=28, fontweight="bold",
            zorder=10, transform=ax.transData)

    # Versets résiduels en cercle autour du sceau
    n_core = len(core)
    for i, r in enumerate(core):
        angle = (2 * math.pi / n_core) * i - math.pi / 2
        rx    = 0.18 * math.cos(angle)
        ry    = 0.18 * math.sin(angle)
        color = COLOR_GOLDEN if r["mult_19"] else COLOR_TEXT
        ax.text(rx, ry,
                str(r["num"]),
                ha="center", va="center",
                color=color, fontsize=6, zorder=10,
                transform=ax.transData)

    # ── Titre et statistiques ──────────────────────────────────────────────
    title = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ\nبُوقِلَّةُ يٰسٓ × ١٩"
    fig.text(0.5, 0.97, title,
             ha="center", va="top",
             color=COLOR_GOLDEN, fontsize=13,
             fontweight="bold")

    ya_sin_info = (
        f"ي = {stats['total_ya']}   س = {stats['total_sin']}   "
        f"ي+س = {stats['total_ya_sin']}  (mod 19 = {stats['ya_sin_mod19']})\n"
        f"Abjad total = {stats['total_abjad']}  (mod 19 = {stats['total_abjad_mod19']})\n"
        f"Versets × 19 : {stats['mult_19_verses']}"
    )
    fig.text(0.5, 0.03, ya_sin_info,
             ha="center", va="bottom",
             color=COLOR_TEXT, fontsize=7.5, alpha=0.85)

    # Légende
    legend_handles = [
        mpatches.Patch(color=COLOR_GOLDEN,   alpha=0.85, label="Verset ×19 (or)"),
        mpatches.Patch(color=COLOR_PULSE_HI, alpha=0.55, label="Forte densité ي/س (bleu)"),
        mpatches.Patch(color=COLOR_PULSE_LO, alpha=0.55, label="Faible densité ي/س"),
        mpatches.Patch(color=COLOR_CORE,     alpha=0.95, label="Noyau central (7 résiduels)"),
    ]
    ax.legend(handles=legend_handles,
              loc="lower right", bbox_to_anchor=(1.25, -0.05),
              facecolor="#111122", edgecolor=COLOR_ANGEL,
              labelcolor=COLOR_TEXT, fontsize=7.5)

    plt.tight_layout()
    plt.savefig(output, format="svg",
                facecolor=COLOR_BG, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return output
