# German-Privacy-Shield

**DSGVO-konforme Dokument-Redaktion mit KI**

Erkennt und schwärzt personenbezogene Daten (PII) in deutschen Dokumenten automatisch.
Läuft 100% lokal mit Ollama - keine Cloud, keine Datenübertragung.

## Highlights

- **100% Lokal** - Läuft komplett auf Ihrer Hardware mit Ollama
- **DSGVO-konform** - Basiert auf Art. 4 DSGVO, Art. 6 DSGVO, Par. 26 BDSG
- **Smart Knowledge Injection** - DSGVO-Wissen direkt im Modell integriert
- **Multi-Mode** - Drei Sicherheitsstufen (strict, balanced, loose)
- **Dokumenttyp-Erkennung** - Optimiert für Rechnungen, Verträge, Ausweise, etc.
- **Nur 1.9GB** - Läuft auf jeder Consumer-GPU und CPUs

## Installation

```bash
pip install german-privacy-shield
```

### Voraussetzungen

1. **Ollama** installieren: https://ollama.com
2. **Modell** laden:
```bash
ollama pull Keyvan/german-privacy-shield
```

## Schnellstart

### Python API

```python
from german_privacy_shield import GermanPrivacyShield, Redactor, PrivacyMode

# PII-Erkennung
shield = GermanPrivacyShield(mode=PrivacyMode.BALANCED)
result = shield.detect_pii("rechnung.png")

for pii in result.pii_items:
    print(f"[{pii.label}] {pii.text}")

# Dokument schwärzen
redactor = Redactor(mode=PrivacyMode.STRICT)
result = redactor.redact("rechnung.png", "rechnung_redacted.png")
print(f"Geschwärzt: {result.pii_count} PIIs")
```

### CLI

```bash
# PII-Erkennung
german-privacy-shield detect rechnung.png

# Dokument schwärzen
german-privacy-shield redact rechnung.png -o rechnung_redacted.png

# Mit strenger Sicherheitsstufe
german-privacy-shield redact dokument.png --mode strict

# Batch-Verarbeitung
german-privacy-shield batch ./input/ ./output/
```

## Sicherheitsstufen

| Modus | Beschreibung | Anwendungsfall |
|-------|--------------|----------------|
| `strict` | Alle PIIs, Unterschriften, Fotos | Maximaler Datenschutz, AI-Training |
| `balanced` | Namen, Adressen, Bankdaten | Standard DSGVO-Compliance |
| `loose` | Nur IBAN, Steuer-ID, Sozialvers. | Minimale Schwärzung |

## Erkannte PII-Kategorien

- **Identität**: Namen, Geburtsdaten, Ausweisnummern
- **Kontakt**: Adressen, Telefon, E-Mail
- **Finanzen**: IBAN, BIC, Kontonummern, Beträge
- **Biometrie**: Unterschriften, Fotos, Gesichter
- **Gesundheit**: Diagnosen, Versicherungsnummern
- **Arbeit**: Personalnummern, Gehalt
- **Steuern**: Steuernummern, Steuer-ID

## Dokumenttypen

Das Modell ist für folgende Dokumenttypen optimiert:

- **invoice** - Rechnungen
- **contract** - Verträge
- **id_card** - Ausweise und Reisepässe
- **tax** - Steuerbescheide
- **medical** - Arztbriefe und medizinische Dokumente

```python
from german_privacy_shield import Redactor, DocumentType

redactor = Redactor()
result = redactor.redact("rechnung.png", doc_type=DocumentType.INVOICE)
```

## API Referenz

### GermanPrivacyShield

```python
class GermanPrivacyShield:
    def __init__(
        self,
        model: str = "german-privacy-shield",
        mode: PrivacyMode = PrivacyMode.BALANCED,
        host: Optional[str] = None  # Ollama Host URL
    )

    def detect_pii(
        self,
        image_path: str,
        doc_type: Optional[DocumentType] = None,
        custom_rules: Optional[List[str]] = None
    ) -> RedactionResult
```

### Redactor

```python
class Redactor(GermanPrivacyShield):
    def redact(
        self,
        image_path: str,
        output_path: Optional[str] = None,
        doc_type: Optional[DocumentType] = None,
        custom_rules: Optional[List[str]] = None,
        draw_labels: bool = False
    ) -> RedactionResult

    def redact_batch(
        self,
        input_dir: str,
        output_dir: str,
        pattern: str = "*.png"
    ) -> List[RedactionResult]
```

## Rechtlicher Hintergrund

German-Privacy-Shield basiert auf:

- **Art. 4 DSGVO** - Definition personenbezogener Daten
- **Art. 6 DSGVO** - Rechtmäßigkeit der Verarbeitung
- **Par. 26 BDSG** - Pseudonymisierung und Anonymisierung
- **Par. 22 BDSG** - Besondere Kategorien (Gesundheit, Religion)

## Performance

| Hardware | Zeit pro Dokument |
|----------|-------------------|
| RTX 4060 8GB | ~5 Sekunden |
| RTX 3060 12GB | ~6 Sekunden |
| CPU (keine GPU) | ~15 Sekunden |

## Systemanforderungen

- Python 3.9+
- Ollama v0.1.0+
- 4GB+ VRAM (GPU) oder 8GB+ RAM (CPU)
- 2GB Speicherplatz für Modell

## Verwandte Projekte

- [german-ocr](https://github.com/Keyvanhardani/german-ocr) - OCR für deutsche Dokumente
- [german-ocr-turbo](https://ollama.com/Keyvan/german-ocr-turbo) - Schnelles OCR-Modell

## Lizenz

Apache 2.0

## Autor

**Keyvan Hardani** - [keyvan.ai](https://keyvan.ai)

---

Made with privacy in Germany
