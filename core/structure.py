# core/structure.py
# Répartition des 83 versets en 19 secteurs (anges gardiens)
# + noyau central = يس + les 7 versets résiduels (83 mod 19 = 7)

TOTAL_VERSES  = 83
TOTAL_ANGELS  = 19
RESIDUAL      = TOTAL_VERSES % TOTAL_ANGELS  # = 7 → noyau central


def build_sectors(results: list[dict]) -> dict:
    """
    Divise les 83 versets en :
      - 19 secteurs de 4 versets chacun (versets 1→76)
      - 1 noyau central avec les 7 versets résiduels (versets 77→83)

    Retourne un dict :
      {
        "sectors": [
            {"angel": 1, "verses": [résultat_v1, ..., résultat_v4]},
            ...
            {"angel": 19, "verses": [résultat_v73, ..., résultat_v76]},
        ],
        "core": [résultat_v77, ..., résultat_v83]
      }
    """
    body   = results[:TOTAL_VERSES - RESIDUAL]   # 76 versets
    core   = results[TOTAL_VERSES - RESIDUAL:]   # 7  versets

    sector_size = len(body) // TOTAL_ANGELS       # = 4

    sectors = []
    for angel in range(TOTAL_ANGELS):
        start = angel * sector_size
        end   = start + sector_size
        sectors.append({
            "angel":  angel + 1,
            "verses": body[start:end],
        })

    return {"sectors": sectors, "core": core}


def sector_summary(sectors_data: dict) -> None:
    """Affiche un résumé lisible de la structure."""
    print("=== STRUCTURE — 19 ANGES ===")
    for s in sectors_data["sectors"]:
        nums    = [r["num"] for r in s["verses"]]
        golden  = [r["num"] for r in s["verses"] if r["mult_19"]]
        tag     = " ★" if golden else ""
        print(f"  Ange {s['angel']:02d} | Versets {nums[0]}–{nums[-1]}{tag}")

    print(f"\n=== NOYAU CENTRAL (يس + {RESIDUAL} résiduels) ===")
    for r in sectors_data["core"]:
        tag = " ★" if r["mult_19"] else ""
        print(f"  V{r['num']:02d}{tag} | Abjad={r['abjad']:6d} | {r['text'][:45]}…")
