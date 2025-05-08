from fpdf import FPDF
from datetime import datetime
from fpdf.enums import XPos, YPos  # Import position enums

class PDFInvoice(FPDF):
    def set_margins(self, left=15, top=15, right=15):
        self.set_left_margin(left)
        self.set_top_margin(top)
        self.set_right_margin(right)
        self.set_auto_page_break(auto=True, margin=top)

    def header(self):
        self.set_font("Times", 'B', 16)
        self.cell(100, 10, "Mizer Companition", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_font("Times", 'B', 14)
        self.cell(0, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        
        self.set_font("Times", '', 10)
        self.cell(100, 6, "Creative Business Idea", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(0, 6, f"Invoice Number: INV-{datetime.today().strftime('%Y%m%d')}", 
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        self.cell(100, 6, "", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(0, 6, f"Date: {datetime.today().strftime('%B %d, %Y')}", 
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        self.ln()

    def footer(self):
        self.set_y(-35)
        self.set_font("Times", 'I', 9)
        self.multi_cell(0, 6, "Terms & Conditions:\nPayment is due within 15 days. Late payment may be subject to additional fees.\nThank you for your business!")

    def add_invoice_info(self, to_name, from_name):
        page_width = self.w - self.l_margin - self.r_margin
        left_width = page_width * 0.72
        right_width = page_width * 0.72
        
        self.set_font("Times", 'B', 12)
        self.cell(left_width, 8, "Invoice To:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(right_width, 8, "Invoice From:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_font("Times", '', 10)
        self.cell(left_width, 6, to_name, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(right_width, 6, from_name, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.cell(left_width, 6, "Managing Director, Company Ltd", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(right_width, 6, "Managing Director, Company Ltd", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.cell(left_width, 6, "Phone: +123 4567 8910", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(right_width, 6, "Phone: +123 4567 8910", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.cell(left_width, 6, f"Email: {to_name.lower().strip().replace(' ', '')}@gmail.com", 
                 new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(right_width, 6, f"Email: {from_name.lower().strip().replace(' ', '')}@gmail.com", 
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.ln(10)

    def add_table(self, df):
        page_width = 180
        headers = ["No.", "Product Description", "Unit Price", "Qty", "Total"]
        proportions = [0.07, 0.47, 0.15, 0.10, 0.21]
        widths = [round(page_width * p) for p in proportions]
    
        row_colors = [(245, 245, 245), (255, 255, 255)]
    
        # Header row
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255)
        self.set_font("helvetica", 'B', 10)  # Using core font instead of Arial
        for i, header in enumerate(headers):
            self.cell(widths[i], 8, header, border=0, align='C', fill=True)
        self.ln()
    
        # Body rows
        self.set_font("helvetica", '', 10)
        self.set_text_color(0)
        total_sum = 0
    
        for index, row in enumerate(df):
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

        # Left: Payment Details
        self.set_font("Times", 'B', 11)
        self.cell(90, 8, "Payment Details:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Times", '', 10)
        self.set_xy(x_left, y_start + 8)
        self.multi_cell(90, 6, "Account Name: John Doe\nAccount Number: 1234 5678 910\nBank: XYZ Bank, Main Branch")

        self.ln(8)
        self.cell(90, 6, "Authorized Signature:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)
        self.line(self.get_x(), self.get_y(), self.get_x() + 50, self.get_y())

        # Right: Summary
        tax = subtotal * tax_rate
        total = subtotal + tax - discount

        self.set_xy(120, y_start)
        self.set_font("Times", 'B', 10)

        label_width = 30
        value_width = 30

        rows = [
            ("Subtotal:", subtotal),
            (f"Tax ({int(tax_rate*100)}%):", tax),
            ("Discount:", discount),
        ]

        for label, value in rows:
            self.set_x(138)
            self.cell(label_width, 8, label, border=0)
            self.cell(value_width, 8, f"${value:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Total
        self.set_x(138)
        self.cell(label_width, 8, "Total:", border=0)
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255)
        self.cell(value_width, 8, f"${total:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.set_text_color(0)

