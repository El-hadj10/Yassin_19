# core/export.py
# Exporte les données analysées vers web/data.json pour la visualisation D3.js

import json
from pathlib import Path

from core.analyzer  import load_verses, analyze, global_stats
from core.structure import build_sectors


def export_json(output_path: str = "web/data.json") -> str:
    """
    Génère web/data.json à partir de l'analyse complète de Yassin.
    Retourne le chemin du fichier créé.
    """
    verses       = load_verses()
    results      = analyze(verses)
    stats        = global_stats(results)
    sectors_data = build_sectors(results)

    data = {
        "stats": stats,
        "sectors": [
            {
                "angel":  s["angel"],
                "verses": s["verses"],
            }
            for s in sectors_data["sectors"]
        ],
        "core": sectors_data["core"],
    }

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return str(out)
