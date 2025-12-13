"""
German-Privacy-Shield - DSGVO-konforme Dokument-Redaktion
Entwickelt von Keyvan (Keyvan.ai)
"""

from .client import GermanPrivacyShield, Redactor
from .knowledge_base import KnowledgeBase, PrivacyMode

__version__ = "0.1.0"
__author__ = "Keyvan Hardani"
__email__ = "info@keyvan.ai"

__all__ = [
    "GermanPrivacyShield",
    "Redactor",
    "KnowledgeBase",
    "PrivacyMode",
]
