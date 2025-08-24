from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime

class PDFInvoice(FPDF):
    def __init__(self, company_name="Vertex", tagline="Where Quality Meets Affordability", **kwargs):
        super().__init__()
        self.company_name = company_name
        self.tagline = tagline
        self.invoice_number = kwargs.get("invoice_number", f"INV-{datetime.today().strftime('%Y%m%d')}")
        self.invoice_date = kwargs.get("invoice_date", datetime.today().strftime('%B %d, %Y'))
        self.terms = kwargs.get("terms", "Payment due within 15 days. Late fees may apply.")
        self.payment_info = kwargs.get("payment_info", "Account Name: John Doe\nAccount Number: 1234 5678 910\nBank: XYZ Bank")

    def header(self):
        self.set_fill_color(0, 102, 204)
        self.rect(0, 0, self.w, 29, style='F')
        self.set_text_color(255)
        self.set_font("Times", 'B', 16)
        self.set_y(6)
        self.set_x(self.l_margin)
        self.cell(100, 10, self.company_name)
        self.set_font("Times", 'B', 14)
        self.set_x(self.w - self.r_margin - 50)
        self.cell(50, 10, "INVOICE", align='R')
        self.set_font("Times", '', 10)
        self.set_y(15)
        self.set_x(self.l_margin)
        self.cell(100, 6, self.tagline)
        self.set_x(self.w - self.r_margin - 60)
        self.cell(60, 6, f"Invoice #: {self.invoice_number}", align='R')
        self.set_y(21)
        self.set_x(self.w - self.r_margin - 60)
        self.cell(60, 6, f"Date: {self.invoice_date}", align='R')
        self.set_text_color(0)
        self.set_y(30)

    def footer(self):
        self.set_y(-35)
        self.set_font("Times", 'I', 9)
        self.multi_cell(0, 6, f"Terms & Conditions:\n{self.terms}")

    def add_invoice_info(self, to_info, from_info):
        page_width = self.w - self.l_margin - self.r_margin
        col_width = page_width * 0.7
        line_height = 6
        title_height = 12
        start_y = self.get_y()
        self.set_font("Times", 'B', 12)
        self.set_xy(self.l_margin, start_y)
        self.cell(col_width, title_height, "Invoice To:")
        self.set_xy(self.l_margin + col_width, start_y)
        self.cell(col_width, title_height, "Invoice From:")
        self.set_font("Times", '', 10)
        max_lines = max(len(to_info), len(from_info))
        
        for i in range(max_lines):
            y = start_y + title_height + i * line_height
            self.set_xy(self.l_margin, y)
            self.cell(col_width, line_height, to_info[i] if i < len(to_info) else "")
            self.set_xy(self.l_margin + col_width, y)
            self.cell(col_width, line_height, from_info[i] if i < len(from_info) else "")
        self.set_y(start_y + title_height + max_lines * line_height + 5)

    def add_table(self, items):
        page_width = 190
        headers = ["No.", "Product Description", "Unit Price", "Qty", "Total"]
        proportions = [0.07, 0.47, 0.15, 0.10, 0.21]
        widths = [round(page_width * p) for p in proportions]
        row_colors = [(245, 245, 245), (255, 255, 255)]
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255)
        self.set_font("helvetica", 'B', 10)
        for i, header in enumerate(headers):
            self.cell(widths[i], 8, header, border=0, align='C', fill=True)
        self.ln()
        self.set_font("helvetica", '', 10)
        self.set_text_color(0)
        total_sum = 0
        for index, row in enumerate(items):
            self.set_fill_color(*row_colors[index % 2])
            unit_price = float(row['unit_price'])
            quantity = int(row['quantity'])
            total = unit_price * quantity
            total_sum += total
            line_data = [str(index + 1), row['description'], f"${unit_price:.2f}", str(quantity), f"${total:.2f}"]
            for i, item in enumerate(line_data):
                self.cell(widths[i], 8, item, border=0, align='C', fill=True)
            self.ln()
        return total_sum

    def add_summary_section(self, subtotal, tax_rate=0.10, discount=0.0):
        self.ln(10)
        x_left = self.get_x()
        y_start = self.get_y()
        self.set_font("Times", 'B', 11)
        self.cell(90, 8, "Payment Details:")
        self.set_font("Times", '', 10)
        self.set_xy(x_left, y_start + 8)
        self.multi_cell(90, 6, self.payment_info)
        self.ln(8)
        self.cell(90, 6, "Authorized Signature:")
        self.ln(5)
        self.line(self.get_x(), self.get_y(), self.get_x() + 50, self.get_y())
        tax = subtotal * tax_rate
        total = subtotal + tax - discount
        self.set_xy(120, y_start)
        self.set_font("Times", 'B', 10)
        rows = [("Subtotal:", subtotal), (f"Tax ({int(tax_rate * 100)}%):", tax), ("Discount:", discount)]
        for label, value in rows:
            self.set_x(138)
            self.cell(30, 8, label)
            self.cell(30, 8, f"${value:.2f}")
            self.ln()
        self.set_x(138)
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255)
        self.set_font("Times", 'B', 10)
        self.cell(30, 8, "Total:", border=0, fill=True, align='C')
        self.cell(30, 8, f"${total:.2f}", border=0, fill=True, align='C')
        self.set_text_color(0)
        
