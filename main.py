# main.py — Bouclier de Yassin × 19
# Orchestrateur : analyse → structure → visualisation

from core.analyzer  import load_verses, analyze, global_stats
from core.structure import build_sectors, sector_summary
from visual.bouclier import draw_shield

OUTPUT_SVG = "bouclier_yassin_19.svg"


def main():
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

    print(f"\n[ Génération du bouclier SVG → {OUTPUT_SVG} ... ]")
    path = draw_shield(sectors_data, stats, OUTPUT_SVG)
    print(f"  → Fichier généré : {path}\n")
    print("✓ Bouclier de Yassin × 19 — terminé.")


if __name__ == "__main__":
    main()
