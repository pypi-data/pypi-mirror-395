"""
Knowledge Base - DSGVO-Wissen und Privacy Modes
Enthält vorgefertigte Prompts für verschiedene Dokumenttypen und Sicherheitsstufen
"""

from enum import Enum
from typing import Dict, List, Optional


class PrivacyMode(Enum):
    """Sicherheitsstufen für die PII-Erkennung"""
    STRICT = "strict"      # Alle PIIs, Unterschriften, Gesichter, Handschrift
    BALANCED = "balanced"  # Standard DSGVO: Namen, Adressen, Bankdaten
    LOOSE = "loose"        # Nur kritische Daten: IBAN, Sozialversicherungsnummer


class DocumentType(Enum):
    """Unterstützte Dokumenttypen"""
    INVOICE = "invoice"        # Rechnung
    CONTRACT = "contract"      # Vertrag
    ID_CARD = "id_card"        # Ausweis/Pass
    TAX_NOTICE = "tax_notice"  # Steuerbescheid
    MEDICAL = "medical"        # Arztbrief
    GENERAL = "general"        # Allgemein


class KnowledgeBase:
    """
    Enthält das injizierte DSGVO-Wissen für verschiedene Dokumenttypen.
    Basiert auf Art. 4 DSGVO, Art. 6 DSGVO, Par. 26 BDSG, Par. 22 BDSG
    """

    # PII-Kategorien gemäß DSGVO
    PII_CATEGORIES: Dict[str, List[str]] = {
        "identitaet": ["name", "geburtsdatum", "personalausweisnummer", "passnummer"],
        "kontakt": ["adresse", "telefon", "email", "fax"],
        "finanzen": ["iban", "bic", "kontonummer", "kreditkarte", "betrag"],
        "biometrie": ["unterschrift", "foto", "gesicht", "fingerabdruck"],
        "gesundheit": ["diagnose", "versicherungsnummer", "arzt", "krankenhaus"],
        "arbeit": ["personalnummer", "gehalt", "arbeitgeber", "position"],
        "steuern": ["steuernummer", "steuer_id", "finanzamt", "aktenzeichen"],
    }

    # Prompts für verschiedene Privacy Modes
    MODE_PROMPTS: Dict[PrivacyMode, str] = {
        PrivacyMode.STRICT: """Du bist ein DSGVO-Auditor mit HÖCHSTER Sicherheitsstufe.
Schwärze ALLE personenbezogenen Daten ohne Ausnahme:
- Alle Namen (auch Firmennamen wenn sie Personen identifizieren)
- Alle Adressen (auch Teiladressen)
- Alle Nummern (IBAN, Telefon, Steuer-ID, Kundennummer, etc.)
- Alle Unterschriften und handschriftlichen Notizen
- Alle Fotos und Gesichter
- Alle Datumsangaben die Personen identifizieren können
- Alle E-Mail-Adressen und URLs mit Personenbezug
REGEL: Im Zweifel IMMER schwärzen. Datenschutz hat Priorität.""",

        PrivacyMode.BALANCED: """Du bist ein DSGVO-Auditor mit STANDARD Sicherheitsstufe.
Schwärze die folgenden personenbezogenen Daten:
- Namen natürlicher Personen
- Adressen (Straße, PLZ, Ort)
- Bankdaten (IBAN, BIC, Kontonummern)
- Kontaktdaten (Telefon, E-Mail)
- Geburtsdaten
- Unterschriften
REGEL: Firmen-Stammdaten (HRB, USt-ID) können bleiben, sofern keine direkte Personenidentifikation möglich.""",

        PrivacyMode.LOOSE: """Du bist ein DSGVO-Auditor mit MINIMALER Sicherheitsstufe.
Finde NUR die kritischsten Finanzdaten:
- IBAN und BIC (Bankverbindungen)
- Kreditkartennummern
- Steuer-IDs und Steuernummern
- Sozialversicherungsnummern
IGNORIERE: Namen, Adressen, Telefonnummern, E-Mails, Daten
REGEL: Nur Finanzdaten und amtliche Nummern melden.""",
    }

    # Dokumenttyp-spezifische Hinweise
    DOCUMENT_HINTS: Dict[DocumentType, str] = {
        DocumentType.INVOICE: """RECHNUNG - Typische PIIs:
- Kundennummer, Rechnungsnummer (können zur Identifikation führen)
- IBAN, BIC, Bankname
- Empfänger-Adresse, Absender-Adresse
- Beträge (bei Gehaltsabrechnungen kritisch)
- Steuernummern (USt-ID, St-Nr)""",

        DocumentType.CONTRACT: """VERTRAG - Typische PIIs:
- Namen der Vertragsparteien
- Adressen beider Parteien
- Geburtsdaten
- Unterschriften (IMMER schwärzen)
- Bankverbindungen für Zahlungen
- Personalausweisnummern (bei Identitätsprüfung)""",

        DocumentType.ID_CARD: """AUSWEIS/PASS - ALLE FELDER SIND KRITISCH:
- Name, Vorname
- Geburtsdatum, Geburtsort
- Ausweisnummer
- Ablaufdatum
- Nationalität
- Foto (IMMER schwärzen)
- Unterschrift
- MRZ (maschinenlesbare Zone)""",

        DocumentType.TAX_NOTICE: """STEUERBESCHEID - Typische PIIs:
- Steuernummer, Steuer-ID
- Name und Adresse des Steuerpflichtigen
- Bankverbindung für Erstattung/Nachzahlung
- Finanzamt-Aktenzeichen
- Beträge (Einkommen, Steuerschuld)
- Veranlagungszeitraum mit Personenbezug""",

        DocumentType.MEDICAL: """ARZTBRIEF/MEDIZINISCH - BESONDERS SENSIBEL (Art. 9 DSGVO):
- Patientenname, Geburtsdatum
- Versicherungsnummer (Krankenversicherung)
- Diagnosen und Befunde
- Arztname und Praxisadresse
- Behandlungsdaten
- Medikation""",

        DocumentType.GENERAL: """ALLGEMEINES DOKUMENT:
Analysiere das Dokument und identifiziere alle personenbezogenen Daten gemäß DSGVO Art. 4.""",
    }

    @classmethod
    def get_system_prompt(cls, mode: PrivacyMode = PrivacyMode.BALANCED) -> str:
        """Generiert den System-Prompt basierend auf dem Privacy Mode"""
        return cls.MODE_PROMPTS.get(mode, cls.MODE_PROMPTS[PrivacyMode.BALANCED])

    @classmethod
    def get_document_hint(cls, doc_type: DocumentType = DocumentType.GENERAL) -> str:
        """Gibt dokumenttyp-spezifische Hinweise zurück"""
        return cls.DOCUMENT_HINTS.get(doc_type, cls.DOCUMENT_HINTS[DocumentType.GENERAL])

    @classmethod
    def build_redaction_prompt(
        cls,
        mode: PrivacyMode = PrivacyMode.BALANCED,
        doc_type: Optional[DocumentType] = None,
        custom_rules: Optional[List[str]] = None
    ) -> str:
        """
        Baut den vollständigen Redaktions-Prompt zusammen.

        Args:
            mode: Sicherheitsstufe (strict, balanced, loose)
            doc_type: Optional - Dokumenttyp für spezifische Hinweise
            custom_rules: Optional - Zusätzliche benutzerdefinierte Regeln

        Returns:
            Vollständiger Prompt für die PII-Erkennung
        """
        parts = [cls.get_system_prompt(mode)]

        if doc_type:
            parts.append(f"\nDOKUMENTTYP-HINWEISE:\n{cls.get_document_hint(doc_type)}")

        if custom_rules:
            parts.append(f"\nZUSÄTZLICHE REGELN:\n" + "\n".join(f"- {rule}" for rule in custom_rules))

        parts.append("""
Analysiere das Dokument und liste ALLE sensiblen Daten auf.

OUTPUT-FORMAT (NUR JSON-Array, keine Erklärungen davor oder danach):
[
  {"label": "KATEGORIE", "text": "exakter_text_aus_dokument"}
]

Verwende diese Kategorien: NAME, ADRESSE, IBAN, TELEFON, EMAIL, DATUM, STEUERNR, UNTERSCHRIFT, BETRAG, KUNDENNR, SONSTIGES

WICHTIG: Gib NUR Text zurück, der TATSÄCHLICH im Dokument sichtbar ist! Erfinde KEINE Beispieldaten!

Gib NUR das JSON-Array zurück.""")

        return "\n\n".join(parts)

    @classmethod
    def get_all_pii_labels(cls) -> List[str]:
        """Gibt alle PII-Kategorien als flache Liste zurück"""
        labels = []
        for category_items in cls.PII_CATEGORIES.values():
            labels.extend(category_items)
        return labels
