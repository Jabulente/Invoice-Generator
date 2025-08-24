import os
from pdf_invoice import PDFInvoice
from data_generator import generate_dataset
from utils import save_to_csv, log_success

if __name__ == "__main__":
    df = generate_dataset(num_customers=5, min_items=1, max_items=5)
    os.makedirs("datasets", exist_ok=True)
    filepath = "datasets/orders.csv"
    df.to_csv(filepath, index=False)
    print(df)

if __name__ == "__main__":
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
        
        from_info = ["Vertex", "support@vertexstore.com", "+255 123 456 789",  "123 Commerce Street, Arusha, Tanzania"]
    
        pdf.add_invoice_info(to_info, from_info)
        
        items = group.to_dict('records')
        subtotal = pdf.add_table(items)
        pdf.add_summary_section(subtotal)
        
        pdf_path = f"outputs/{cart_id}.pdf"
        pdf.output(pdf_path)
        log_success(pdf_path)
