# main.py — Bouclier de Yassin × 19
# Orchestrateur : analyse → structure → visualisation (SVG + D3.js)

import argparse
import os
import sys

from core.analyzer  import load_verses, analyze, global_stats
from core.structure import build_sectors, sector_summary
from core.export    import export_json

OUTPUT_SVG = "bouclier_yassin_19.svg"


def _draw_shield_if_available(sectors_data: dict, stats: dict, output_svg: str, skip_svg: bool) -> str | None:
    """
    Dessine le SVG si matplotlib/numpy sont disponibles.
    Retourne le chemin du SVG ou None si ignoré.
    """
    if skip_svg:
        print("[ SVG ignore (--skip-svg actif) ]")
        return None

    try:
        from visual.bouclier import draw_shield
    except ModuleNotFoundError as exc:
        print("[ SVG non genere: dependances absentes ]")
        print(f"  → Detail: {exc}")
        print("  → Sous Termux, tu peux continuer avec la version web (web/data.json).\n")
        return None

    print(f"\n[ Génération du bouclier SVG → {output_svg} ... ]")
    path = draw_shield(sectors_data, stats, output_svg)
    print(f"  → Fichier généré : {path}\n")
    return path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyse la sourate Yassin et génère les artefacts SVG/JSON."
    )
    parser.add_argument(
        "--skip-svg",
        action="store_true",
        help="N'essaie pas de générer le SVG (utile sur Termux sans matplotlib).",
    )
    parser.add_argument(
        "--output-svg",
        default=OUTPUT_SVG,
        help=f"Chemin du fichier SVG de sortie (par defaut: {OUTPUT_SVG}).",
    )
    return parser


def main():
    args = _build_parser().parse_args()
    py_cmd = os.path.basename(sys.executable) or "python3"

    print("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n")
    print("[ Chargement des versets... ]")
    verses  = load_verses()
    print(f"  → {len(verses)} versets chargés.\n")

    print("[ Analyse Abjad + fréquences ي/س... ]")
    results = analyze(verses)
    stats   = global_stats(results)

    print(f"  → Abjad total     : {stats['total_abjad']}  (mod 19 = {stats['total_abjad_mod19']})")
    print(f"  → Total ي         : {stats['total_ya']}")
    print(f"  → Total س         : {stats['total_sin']}")
    print(f"  → Total ي+س       : {stats['total_ya_sin']}  (mod 19 = {stats['ya_sin_mod19']})")
    print(f"  → Versets ×19     : {stats['mult_19_verses']}\n")

    print("[ Construction des 19 secteurs... ]")
    sectors_data = build_sectors(results)
    sector_summary(sectors_data)

    _draw_shield_if_available(sectors_data, stats, args.output_svg, args.skip_svg)

    print("[ Export JSON pour le bouclier D3.js → web/data.json ... ]")
    json_path = export_json("web/data.json")
    print(f"  → Fichier généré : {json_path}")
    print("  → Pour lancer le bouclier interactif :")
    print(f"      {py_cmd} -m http.server 8000 --directory web")
    print("      puis ouvre : http://localhost:8000\n")

    print("✓ Bouclier de Yassin × 19 — terminé.")


if __name__ == "__main__":
    main()
