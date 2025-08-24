import os
from data_generator import generate_dataset
from utils import save_to_csv
from pdf_invoice import PDFInvoice

# Generate dataset
df = generate_dataset(num_customers=5, min_items=1, max_items=4)
os.makedirs("outputs", exist_ok=True)
csv_path = "outputs/orders.csv"
save_to_csv(df, csv_path)

# Generate invoices
for cart_id, group in df.groupby('cart_id'):
    pdf = PDFInvoice(invoice_number=cart_id)
    pdf.add_page()
    
    customer = group.iloc[0]
    to_info = [
        customer['customer_name'],
        customer['customer_email'],
        customer['customer_phone'],
        customer['customer_address']
    ]
    from_info = ["Your Company", "support@company.com", "123-456-7890", "123 Business St, City"]
    pdf.add_invoice_info(to_info, from_info)
    
    items = group.to_dict('records')
    subtotal = pdf.add_table(items)
    pdf.add_summary_section(subtotal)
    
    pdf_path = f"outputs/{cart_id}.pdf"
    pdf.output(pdf_path)
    print(f"Invoice saved: {pdf_path}")
