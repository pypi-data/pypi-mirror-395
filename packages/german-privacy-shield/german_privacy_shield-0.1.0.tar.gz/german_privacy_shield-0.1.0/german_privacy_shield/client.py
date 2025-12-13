"""
German-Privacy-Shield Client
Hauptklasse für die DSGVO-konforme Dokument-Redaktion
"""

import json
import re
import base64
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

try:
    import ollama
except ImportError:
    ollama = None

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
    ImageDraw = None

from .knowledge_base import KnowledgeBase, PrivacyMode, DocumentType


@dataclass
class PIIResult:
    """Ergebnis einer PII-Erkennung"""
    label: str
    text: str
    confidence: float = 1.0
    box: Optional[List[int]] = None  # [ymin, xmin, ymax, xmax] falls verfügbar


@dataclass
class RedactionResult:
    """Ergebnis einer Redaktion"""
    success: bool
    pii_count: int
    pii_items: List[PIIResult]
    output_path: Optional[str] = None
    raw_response: Optional[str] = None
    error: Optional[str] = None


class GermanPrivacyShield:
    """
    Hauptklasse für die PII-Erkennung mit Ollama.

    Beispiel:
        shield = GermanPrivacyShield()
        result = shield.detect_pii("rechnung.png")
        print(result.pii_items)
    """

    DEFAULT_MODEL = "german-privacy-shield"
    FALLBACK_MODEL = "qwen3-vl:2b"

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        mode: PrivacyMode = PrivacyMode.BALANCED,
        host: Optional[str] = None
    ):
        """
        Initialisiert den Privacy Shield Client.

        Args:
            model: Ollama Modellname (Standard: german-privacy-shield)
            mode: Sicherheitsstufe (strict, balanced, loose)
            host: Optional - Ollama Host URL
        """
        if ollama is None:
            raise ImportError("ollama package not installed. Run: pip install ollama")

        self.model = model
        self.mode = mode
        self.host = host
        self._client = ollama.Client(host=host) if host else None

    def _call_ollama(self, prompt: str, image_path: str) -> str:
        """Ruft Ollama mit Bild auf"""
        messages = [{
            'role': 'user',
            'content': prompt,
            'images': [image_path]
        }]

        if self._client:
            response = self._client.chat(model=self.model, messages=messages)
        else:
            response = ollama.chat(model=self.model, messages=messages)

        return response['message']['content']

    def _parse_response(self, content: str) -> List[PIIResult]:
        """Parst die Ollama-Antwort und extrahiert PIIs"""
        pii_items = []

        # Versuche JSON zu finden und zu parsen
        json_match = re.search(r'\[[\s\S]*?\]', content)
        if json_match:
            try:
                data = json.loads(json_match.group())
                for item in data:
                    if isinstance(item, dict):
                        pii = PIIResult(
                            label=item.get('label', 'unknown'),
                            text=item.get('text', ''),
                            confidence=item.get('confidence', 1.0),
                            box=item.get('box')
                        )
                        # Duplikate vermeiden
                        if not any(p.text == pii.text and p.label == pii.label for p in pii_items):
                            pii_items.append(pii)
            except json.JSONDecodeError:
                pass

        # Fallback: Versuche Textformat zu parsen (- [KATEGORIE]: text)
        if not pii_items:
            pattern = r'-\s*\[([^\]]+)\]:\s*(.+)'
            for match in re.finditer(pattern, content):
                pii = PIIResult(
                    label=match.group(1).lower().strip(),
                    text=match.group(2).strip()
                )
                pii_items.append(pii)

        return pii_items

    def detect_pii(
        self,
        image_path: Union[str, Path],
        doc_type: Optional[DocumentType] = None,
        custom_rules: Optional[List[str]] = None
    ) -> RedactionResult:
        """
        Erkennt personenbezogene Daten in einem Dokument.

        Args:
            image_path: Pfad zum Bild
            doc_type: Optional - Dokumenttyp für bessere Erkennung
            custom_rules: Optional - Zusätzliche Regeln

        Returns:
            RedactionResult mit gefundenen PIIs
        """
        image_path = str(image_path)

        if not Path(image_path).exists():
            return RedactionResult(
                success=False,
                pii_count=0,
                pii_items=[],
                error=f"Datei nicht gefunden: {image_path}"
            )

        # Prompt bauen
        prompt = KnowledgeBase.build_redaction_prompt(
            mode=self.mode,
            doc_type=doc_type,
            custom_rules=custom_rules
        )

        try:
            # Ollama aufrufen
            raw_response = self._call_ollama(prompt, image_path)

            # Antwort parsen
            pii_items = self._parse_response(raw_response)

            return RedactionResult(
                success=True,
                pii_count=len(pii_items),
                pii_items=pii_items,
                raw_response=raw_response
            )

        except Exception as e:
            return RedactionResult(
                success=False,
                pii_count=0,
                pii_items=[],
                error=str(e)
            )

    def set_mode(self, mode: PrivacyMode) -> None:
        """Ändert die Sicherheitsstufe"""
        self.mode = mode


class Redactor(GermanPrivacyShield):
    """
    Erweiterte Klasse mit Bild-Schwärzungsfunktion.

    Beispiel:
        redactor = Redactor()
        result = redactor.redact("rechnung.png", "rechnung_redacted.png")
    """

    def __init__(
        self,
        model: str = GermanPrivacyShield.DEFAULT_MODEL,
        mode: PrivacyMode = PrivacyMode.BALANCED,
        host: Optional[str] = None,
        redaction_color: tuple = (0, 0, 0)  # Schwarz
    ):
        super().__init__(model=model, mode=mode, host=host)

        if Image is None:
            raise ImportError("Pillow package not installed. Run: pip install Pillow")

        self.redaction_color = redaction_color

    def _find_text_regions(
        self,
        image: Image.Image,
        pii_items: List[PIIResult]
    ) -> List[Dict[str, Any]]:
        """
        Findet die ungefähren Regionen für die PIIs im Bild.

        Hinweis: Dies ist eine vereinfachte Version. Für präzise Koordinaten
        wird OCR mit Bounding Boxes (z.B. PaddleOCR) empfohlen.
        """
        regions = []
        img_width, img_height = image.size

        for i, pii in enumerate(pii_items):
            if pii.box:
                # Normalisierte Koordinaten (0-1000) in Pixel umrechnen
                box = pii.box
                if max(box) <= 1000:
                    y1 = int((box[0] / 1000) * img_height)
                    x1 = int((box[1] / 1000) * img_width)
                    y2 = int((box[2] / 1000) * img_height)
                    x2 = int((box[3] / 1000) * img_width)
                else:
                    y1, x1, y2, x2 = box

                regions.append({
                    'box': (x1, y1, x2, y2),
                    'label': pii.label,
                    'text': pii.text
                })

        return regions

    def redact(
        self,
        image_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        doc_type: Optional[DocumentType] = None,
        custom_rules: Optional[List[str]] = None,
        draw_labels: bool = False
    ) -> RedactionResult:
        """
        Erkennt PIIs und schwärzt sie im Bild.

        Args:
            image_path: Pfad zum Eingabebild
            output_path: Pfad für das geschwärzte Bild (Standard: *_redacted.*)
            doc_type: Optional - Dokumenttyp
            custom_rules: Optional - Zusätzliche Regeln
            draw_labels: Ob Kategorie-Labels gezeichnet werden sollen

        Returns:
            RedactionResult mit Pfad zum geschwärzten Bild
        """
        image_path = Path(image_path)

        if output_path is None:
            output_path = image_path.parent / f"{image_path.stem}_redacted{image_path.suffix}"
        else:
            output_path = Path(output_path)

        # PIIs erkennen
        result = self.detect_pii(image_path, doc_type, custom_rules)

        if not result.success:
            return result

        if result.pii_count == 0:
            # Keine PIIs gefunden - Originalbild kopieren
            import shutil
            shutil.copy(image_path, output_path)
            result.output_path = str(output_path)
            return result

        try:
            # Bild laden
            image = Image.open(image_path).convert('RGB')
            draw = ImageDraw.Draw(image)

            # Regionen finden und schwärzen
            regions = self._find_text_regions(image, result.pii_items)

            for region in regions:
                box = region['box']
                # Rechteck zeichnen
                draw.rectangle(box, fill=self.redaction_color)

                if draw_labels:
                    # Label über dem geschwärzten Bereich
                    draw.text((box[0], box[1] - 15), f"[{region['label']}]", fill=(255, 0, 0))

            # Geschwärztes Bild speichern
            image.save(output_path)
            result.output_path = str(output_path)

        except Exception as e:
            result.success = False
            result.error = f"Fehler beim Schwärzen: {str(e)}"

        return result

    def redact_batch(
        self,
        input_dir: Union[str, Path],
        output_dir: Union[str, Path],
        pattern: str = "*.png",
        **kwargs
    ) -> List[RedactionResult]:
        """
        Schwärzt mehrere Dokumente in einem Verzeichnis.

        Args:
            input_dir: Eingabeverzeichnis
            output_dir: Ausgabeverzeichnis
            pattern: Datei-Pattern (Standard: *.png)
            **kwargs: Weitere Argumente für redact()

        Returns:
            Liste von RedactionResults
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        for image_path in input_dir.glob(pattern):
            output_path = output_dir / f"{image_path.stem}_redacted{image_path.suffix}"
            result = self.redact(image_path, output_path, **kwargs)
            results.append(result)

        return results
