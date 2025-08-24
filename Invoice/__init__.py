"""
Invoice Generator Package
-------------------------
Modules:
- data_generator: Functions to generate fake customer order datasets
- pdf_invoice: PDFInvoice class for creating invoices
- utils: Helper functions like save_to_csv and load_dataset
"""

from .data_generator import generate_dataset
from .pdf_invoice import PDFInvoice
from .utils import save_to_csv, load_dataset

__all__ = [
    "generate_dataset",
    "PDFInvoice",
    "save_to_csv",
    "load_dataset"
]
