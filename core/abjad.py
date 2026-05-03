# core/abjad.py
# Dictionnaire Abjad complet (système Mashriqî classique)
# Source : table Abjad standard (Alif=1 ... Ghayn=1000)

ABJAD_MAP = {
    # Lettres de base
    'ا': 1,   'أ': 1,  'إ': 1,  'آ': 1,  'ٱ': 1,
    'ب': 2,
    'ج': 3,
    'د': 4,
    'ه': 5,   'ة': 5,
    'و': 6,   'ؤ': 6,
    'ز': 7,
    'ح': 8,
    'ط': 9,
    'ي': 10,  'ى': 10, 'ئ': 10,
    'ك': 20,
    'ل': 30,
    'م': 40,
    'ن': 50,
    'س': 60,
    'ع': 70,
    'ف': 80,
    'ص': 90,
    'ق': 100,
    'ر': 200,
    'ش': 300,
    'ت': 400,  'ث': 500,
    'خ': 600,
    'ذ': 700,
    'ض': 800,
    'ظ': 900,
    'غ': 1000,
}

# Caractères à ignorer (signes diacritiques, ponctuation, etc.)
_IGNORED = set('ًٌٍَُِّْٰٓٔ۟۠ۡ\u0670\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0653\u0654\u0655\u0656\u0657\u0658\u0659\u065a\u065b\u065c\u065d\u065e\u065f\u06d6\u06d7\u06d8\u06d9\u06da\u06db\u06dc\u06dd\u06de\u06df\u06e0\u06e1\u06e2\u06e3\u06e4\u06e5\u06e6\u06e7\u06e8\u06e9\u06ea\u06eb\u06ec\u06ed\u06ee\u06ef ،؟\u200f\u200e\n\r\t')


def abjad_value(text: str) -> int:
    """Retourne la valeur Abjad totale d'une chaîne arabe."""
    total = 0
    for char in text:
        if char in ABJAD_MAP:
            total += ABJAD_MAP[char]
    return total


def abjad_word(word: str) -> int:
    """Retourne la valeur Abjad d'un mot (alias lisible)."""
    return abjad_value(word)


def check_19_signature(text: str) -> bool:
    """Retourne True si la valeur Abjad du texte est un multiple de 19."""
    val = abjad_value(text)
    return val > 0 and val % 19 == 0


if __name__ == "__main__":
    # Test rapide : valeur de "يس"
    seal = "يس"
    print(f"Valeur Abjad de «يس» : {abjad_value(seal)}")  # attendu : 70
    print(f"Signature 19 de «يس» : {check_19_signature(seal)}")
