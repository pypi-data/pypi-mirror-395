import requests
from typing import Optional, Tuple, List

class Translator:
    """
    Gelişmiş Google Translate (unofficial) çeviri sınıfı.
    - Tek session (hızlı)
    - Uzun metin otomatik bölme
    - Auto-detect desteği
    - Hata yönetimi
    """

    URL = "https://translate.googleapis.com/translate_a/single"

    def __init__(self, timeout: int = 10, chunk_size: int = 4000):
        self.session = requests.Session()
        self.timeout = timeout
        self.chunk_size = chunk_size  # Google genelde 5k üstü metni keser

    def _split_text(self, text: str) -> List[str]:
        """Uzun metinleri Google limitlerine göre böler."""
        if len(text) <= self.chunk_size:
            return [text]

        parts = []
        current = ""

        for word in text.split():
            if len(current) + len(word) + 1 > self.chunk_size:
                parts.append(current)
                current = word
            else:
                current += " " + word if current else word

        if current:
            parts.append(current)

        return parts

    def _request(self, sl: str, tl: str, text: str):
        """Google Translate API istek işlemi."""
        params = {
            "client": "gtx",
            "sl": sl,
            "tl": tl,
            "dt": "t",
            "q": text
        }

        r = self.session.get(self.URL, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def _extract_translation(self, data) -> str:
        """Google'ın döndürdüğü karmaşık JSON içinden metni temiz çıkarır."""
        if not data or not isinstance(data, list):
            return ""

        try:
            return "".join(piece[0] for piece in data[0] if piece[0])
        except Exception:
            return ""

    def translate(self, sl: str, tl: str, text: str) -> Tuple[str, Optional[str]]:
        """
        Ana çeviri fonksiyonu.
        Döner:
            (çeviri, detected_lang)
        - detected_lang: sl="auto" olduğunda döner, yoksa None
        """

        parts = self._split_text(text)
        result_text = ""
        detected_lang = None

        for part in parts:
            data = self._request(sl, tl, part)
            translated = self._extract_translation(data)
            result_text += translated

            # Auto-detect dili API bazen 2. indexte döndürür
            if sl == "auto":
                try:
                    detected_lang = data[2]
                except:
                    pass

        return result_text, detected_lang


# ---- KOLAY ERİŞİM FONKSİYONU ---- #

def translate(sl: str, tl: str, text: str) -> str:
    """
    Hızlı kullanım için kısa fonksiyon.
    detected_lang döndürmez — sadece çeviri verir.
    """
    t = Translator()
    translated, _det = t.translate(sl, tl, text)
    return translated
