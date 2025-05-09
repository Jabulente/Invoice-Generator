from fpdf import FPDF
from datetime import datetime
from fpdf.enums import XPos, YPos


class PDFInvoice(FPDF):
    def __init__(self, company_name="Your Company", tagline="Business Tagline", **kwargs):
        super().__init__()
        self.company_name = company_name
        self.tagline = tagline
        self.invoice_number = kwargs.get("invoice_number", f"INV-{datetime.today().strftime('%Y%m%d')}")
        self.invoice_date = kwargs.get("invoice_date", datetime.today().strftime('%B %d, %Y'))
        self.terms = kwargs.get("terms", "Payment is due within 15 days. Late payment may be subject to additional fees.\nThank you for your business!")
        self.payment_info = kwargs.get("payment_info", "Account Name: John Doe\nAccount Number: 1234 5678 910\nBank: XYZ Bank, Main Branch")

    def set_margins(self, left=15, top=0, right=15):
        self.set_left_margin(left)
        self.set_top_margin(top)
        self.set_right_margin(right)
        self.set_auto_page_break(auto=True, margin=top)
        
    def draw_colored_bar(self, height=15):
        self.set_fill_color(0, 102, 204)
        self.rect(self.l_margin, self.get_y(), self.w - self.l_margin - self.r_margin, height, style='F')
            
    def header(self):
        # Full page width (ignores margins)
        full_width = self.w
        header_height = 29
    
        # Draw rectangle from edge to edge
        self.set_fill_color(0, 102, 204)
        self.rect(x=0, y=0, w=full_width, h=header_height, style='F')  # Full-width filled rectangle
    
        # Set text color and font
        self.set_text_color(255, 255, 255)
        self.set_font("Times", 'B', 16)
    
        # Set Y slightly down from top
        self.set_y(6)
        self.set_x(self.l_margin)
        self.cell(100, 10, self.company_name, new_x=XPos.RIGHT, new_y=YPos.TOP, fill=True)
    
        self.set_font("Times", 'B', 14)
        self.set_x(self.w - self.r_margin - 50)
        self.cell(50, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
    
        # Second row: tagline and invoice number
        self.set_y(15)
        self.set_x(self.l_margin)
        self.set_font("Times", '', 10)
        self.cell(100, 6, self.tagline, new_x=XPos.RIGHT, new_y=YPos.TOP)
    
        self.set_x(self.w - self.r_margin - 60)
        self.cell(60, 6, f"Invoice Number: {self.invoice_number}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
    
        # Third row: invoice date
        self.set_y(21)
        self.set_x(self.w - self.r_margin - 60)
        self.cell(60, 6, f"Date: {self.invoice_date}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
    
        # Reset to margin-based positioning for body
        self.set_y(30)
        self.set_text_color(0, 0, 0)




    def footer(self):
        self.set_y(-35)
        self.set_font("Times", 'I', 9)
        self.multi_cell(0, 6, f"Terms & Conditions:\n{self.terms}")

    def add_invoice_info(self, to_info, from_info):
        page_width = self.w - self.l_margin - self.r_margin
        #col_width = page_width / 2  # Equal width for both columns
        col_width = page_width*0.73
        line_height = 6
        title_height = 12
    
        # Capture current y position to align rows properly
        start_y = self.get_y()
    
        # Titles
        self.set_font("Times", 'B', 12)
        self.set_xy(self.l_margin, start_y)
        self.cell(col_width, title_height, "Invoice To:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_xy(self.l_margin + col_width, start_y)
        self.cell(col_width, title_height, "Invoice From:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
        # Info lines
        self.set_font("Times", '', 10)
        max_lines = max(len(to_info), len(from_info))
    
        for i in range(max_lines):
            left_line = to_info[i] if i < len(to_info) else ""
            right_line = from_info[i] if i < len(from_info) else ""
    
            y = start_y + title_height + i * line_height
            self.set_xy(self.l_margin, y)
            self.cell(col_width, line_height, left_line, new_x=XPos.RIGHT, new_y=YPos.TOP)
    
            self.set_xy(self.l_margin + col_width, y)
            self.cell(col_width, line_height, right_line, new_x=XPos.RIGHT, new_y=YPos.TOP)
    
        self.set_y(start_y + title_height + max_lines * line_height + 5)


    def add_table(self, items):
        page_width = 180
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
            fill_color = row_colors[index % 2]
            self.set_fill_color(*fill_color)

            description = row['description']
            unit_price = float(row['unit_price'])
            quantity = int(row['quantity'])
            total = unit_price * quantity
            total_sum += total

            line_data = [str(index + 1), description, f"${unit_price:.2f}", str(quantity), f"${total:.2f}"]
            for i, item in enumerate(line_data):
                self.cell(widths[i], 8, item, border=0, align='C', fill=True)
            self.ln()

        return total_sum

    def add_summary_section(self, subtotal, tax_rate=0.10, discount=0.0):
        self.ln(10)
        x_left = self.get_x()
        y_start = self.get_y()

        self.set_font("Times", 'B', 11)
        self.cell(90, 8, "Payment Details:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Times", '', 10)
        self.set_xy(x_left, y_start + 8)
        self.multi_cell(90, 6, self.payment_info)

        self.ln(8)
        self.cell(90, 6, "Authorized Signature:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)
        self.line(self.get_x(), self.get_y(), self.get_x() + 50, self.get_y())

        tax = subtotal * tax_rate
        total = subtotal + tax - discount

        self.set_xy(120, y_start)
        self.set_font("Times", 'B', 10)
        label_width = 30
        value_width = 30

        rows = [
            ("Subtotal:", subtotal),
            (f"Tax ({int(tax_rate * 100)}%):", tax),
            ("Discount:", discount),
        ]

        for label, value in rows:
            self.set_x(138)
            self.cell(label_width, 8, label, border=0)
            self.cell(value_width, 8, f"${value:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_x(138)
        self.cell(label_width, 8, "Total:", border=0)
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255)
        self.cell(value_width, 8, f"${total:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.set_text_color(0)