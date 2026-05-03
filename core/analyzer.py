# core/analyzer.py
# Analyse mathématique et fréquentielle de la Sourate Yassin
# Couche 1 : valeurs Abjad, multiples de 19
# Couche 2 : fréquences des initiales Ya (ي) et Sin (س)

from pathlib import Path
from core.abjad import abjad_value, check_19_signature

DATA_FILE = Path(__file__).parent.parent / "data" / "yassin.txt"

# Initiales de la Sourate (Muqatta'at)
YA  = 'ي'
SIN = 'س'


def load_verses(path: Path = DATA_FILE) -> list[str]:
    """Charge les 83 versets depuis le fichier texte (1 verset par ligne)."""
    with open(path, encoding="utf-8") as f:
        verses = [line.strip() for line in f if line.strip()]
    return verses


def analyze(verses: list[str]) -> list[dict]:
    """
    Pour chaque verset, calcule :
      - numéro (1-based)
      - texte
      - valeur abjad
      - multiple de 19 ?
      - compte de ي
      - compte de س
    """
    results = []
    for i, verse in enumerate(verses, 1):
        val = abjad_value(verse)
        results.append({
            "num":        i,
            "text":       verse,
            "abjad":      val,
            "mult_19":    val % 19 == 0 if val > 0 else False,
            "ya_count":   verse.count(YA),
            "sin_count":  verse.count(SIN),
        })
    return results


def global_stats(results: list[dict]) -> dict:
    """Statistiques globales sur la sourate."""
    total_ya  = sum(r["ya_count"]  for r in results)
    total_sin = sum(r["sin_count"] for r in results)
    total_abjad = sum(r["abjad"]   for r in results)
    mult_19_verses = [r["num"] for r in results if r["mult_19"]]

    return {
        "total_verses":      len(results),
        "total_abjad":       total_abjad,
        "total_abjad_mod19": total_abjad % 19,
        "total_ya":          total_ya,
        "total_sin":         total_sin,
        "total_ya_sin":      total_ya + total_sin,
        "ya_sin_mod19":      (total_ya + total_sin) % 19,
        "mult_19_verses":    mult_19_verses,
        "count_mult_19":     len(mult_19_verses),
    }


if __name__ == "__main__":
    verses  = load_verses()
    results = analyze(verses)
    stats   = global_stats(results)

    print("=== STATISTIQUES GLOBALES ===")
    print(f"Versets : {stats['total_verses']}")
    print(f"Valeur Abjad totale : {stats['total_abjad']}  (mod 19 = {stats['total_abjad_mod19']})")
    print(f"Total ي  : {stats['total_ya']}")
    print(f"Total س  : {stats['total_sin']}")
    print(f"Total ي+س : {stats['total_ya_sin']}  (mod 19 = {stats['ya_sin_mod19']})")
    print(f"Versets multiples de 19 ({stats['count_mult_19']}) : {stats['mult_19_verses']}")

    print("\n=== VERSETS MULTIPLES DE 19 ===")
    for r in results:
        if r["mult_19"]:
            print(f"  V{r['num']:02d} | Abjad={r['abjad']:6d} | {r['text'][:50]}…")
