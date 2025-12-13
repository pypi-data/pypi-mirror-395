"""
German-Privacy-Shield CLI
Kommandozeilenschnittstelle für die Dokument-Redaktion
"""

import argparse
import sys
from pathlib import Path

from .client import GermanPrivacyShield, Redactor
from .knowledge_base import PrivacyMode, DocumentType


def main():
    parser = argparse.ArgumentParser(
        prog='german-privacy-shield',
        description='DSGVO-konforme Dokument-Redaktion - Entwickelt von Keyvan (Keyvan.ai)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # PII-Erkennung
  german-privacy-shield detect rechnung.png

  # Dokument schwärzen
  german-privacy-shield redact rechnung.png -o rechnung_redacted.png

  # Mit strenger Sicherheitsstufe
  german-privacy-shield redact dokument.pdf --mode strict

  # Batch-Verarbeitung
  german-privacy-shield batch ./input/ ./output/

Sicherheitsstufen:
  strict    - Alle PIIs, Unterschriften, Fotos (höchste Sicherheit)
  balanced  - Standard DSGVO: Namen, Adressen, Bankdaten
  loose     - Nur kritische Daten: IBAN, Steuer-ID

Dokumenttypen:
  invoice   - Rechnung
  contract  - Vertrag
  id_card   - Ausweis/Pass
  tax       - Steuerbescheid
  medical   - Arztbrief
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Verfügbare Befehle')

    # detect subcommand
    detect_parser = subparsers.add_parser('detect', help='PII-Erkennung ohne Schwärzung')
    detect_parser.add_argument('image', help='Pfad zum Dokument-Bild')
    detect_parser.add_argument('--mode', '-m', choices=['strict', 'balanced', 'loose'],
                              default='balanced', help='Sicherheitsstufe')
    detect_parser.add_argument('--type', '-t', choices=['invoice', 'contract', 'id_card', 'tax', 'medical'],
                              help='Dokumenttyp für bessere Erkennung')
    detect_parser.add_argument('--json', '-j', action='store_true', help='Ausgabe als JSON')
    detect_parser.add_argument('--model', default='german-privacy-shield', help='Ollama Modellname')

    # redact subcommand
    redact_parser = subparsers.add_parser('redact', help='Dokument schwärzen')
    redact_parser.add_argument('image', help='Pfad zum Dokument-Bild')
    redact_parser.add_argument('--output', '-o', help='Ausgabepfad (Standard: *_redacted.*)')
    redact_parser.add_argument('--mode', '-m', choices=['strict', 'balanced', 'loose'],
                              default='balanced', help='Sicherheitsstufe')
    redact_parser.add_argument('--type', '-t', choices=['invoice', 'contract', 'id_card', 'tax', 'medical'],
                              help='Dokumenttyp')
    redact_parser.add_argument('--labels', '-l', action='store_true', help='Labels über geschwärzten Bereichen')
    redact_parser.add_argument('--model', default='german-privacy-shield', help='Ollama Modellname')

    # batch subcommand
    batch_parser = subparsers.add_parser('batch', help='Mehrere Dokumente verarbeiten')
    batch_parser.add_argument('input_dir', help='Eingabeverzeichnis')
    batch_parser.add_argument('output_dir', help='Ausgabeverzeichnis')
    batch_parser.add_argument('--pattern', '-p', default='*.png', help='Datei-Pattern (Standard: *.png)')
    batch_parser.add_argument('--mode', '-m', choices=['strict', 'balanced', 'loose'],
                              default='balanced', help='Sicherheitsstufe')
    batch_parser.add_argument('--model', default='german-privacy-shield', help='Ollama Modellname')

    # version
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1.0')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Privacy Mode mapping
    mode_map = {
        'strict': PrivacyMode.STRICT,
        'balanced': PrivacyMode.BALANCED,
        'loose': PrivacyMode.LOOSE
    }

    # Document Type mapping
    type_map = {
        'invoice': DocumentType.INVOICE,
        'contract': DocumentType.CONTRACT,
        'id_card': DocumentType.ID_CARD,
        'tax': DocumentType.TAX_NOTICE,
        'medical': DocumentType.MEDICAL
    }

    try:
        if args.command == 'detect':
            shield = GermanPrivacyShield(model=args.model, mode=mode_map[args.mode])
            doc_type = type_map.get(args.type) if args.type else None

            print(f"Analysiere: {args.image}")
            print(f"Modus: {args.mode.upper()}")
            print("-" * 50)

            result = shield.detect_pii(args.image, doc_type=doc_type)

            if not result.success:
                print(f"FEHLER: {result.error}")
                sys.exit(1)

            if args.json:
                import json
                output = {
                    'success': True,
                    'pii_count': result.pii_count,
                    'items': [{'label': p.label, 'text': p.text} for p in result.pii_items]
                }
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                print(f"\nGefundene PIIs: {result.pii_count}")
                print("-" * 50)
                for i, pii in enumerate(result.pii_items, 1):
                    print(f"  {i}. [{pii.label.upper()}] {pii.text}")

        elif args.command == 'redact':
            redactor = Redactor(model=args.model, mode=mode_map[args.mode])
            doc_type = type_map.get(args.type) if args.type else None

            print(f"Schwärze: {args.image}")
            print(f"Modus: {args.mode.upper()}")
            print("-" * 50)

            result = redactor.redact(
                args.image,
                output_path=args.output,
                doc_type=doc_type,
                draw_labels=args.labels
            )

            if not result.success:
                print(f"FEHLER: {result.error}")
                sys.exit(1)

            print(f"\nGefundene PIIs: {result.pii_count}")
            for i, pii in enumerate(result.pii_items, 1):
                print(f"  {i}. [{pii.label.upper()}] {pii.text}")
            print("-" * 50)
            print(f"Geschwärztes Dokument: {result.output_path}")

        elif args.command == 'batch':
            redactor = Redactor(model=args.model, mode=mode_map[args.mode])

            print(f"Batch-Verarbeitung: {args.input_dir} -> {args.output_dir}")
            print(f"Pattern: {args.pattern}")
            print(f"Modus: {args.mode.upper()}")
            print("-" * 50)

            results = redactor.redact_batch(
                args.input_dir,
                args.output_dir,
                pattern=args.pattern
            )

            success_count = sum(1 for r in results if r.success)
            total_pii = sum(r.pii_count for r in results)

            print(f"\nVerarbeitet: {len(results)} Dokumente")
            print(f"Erfolgreich: {success_count}")
            print(f"PIIs geschwärzt: {total_pii}")

    except KeyboardInterrupt:
        print("\nAbgebrochen.")
        sys.exit(1)
    except Exception as e:
        print(f"FEHLER: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
