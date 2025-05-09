from Invoice.Invoicepdf import PDFInvoice
from Utilis.logger import log_success
from datetime import datetime
import pandas as pd
import os

# Load orders dataset
df = pd.read_csv("Datasets/orders.csv")

# Group data by cart_id  as Its Unique Id (each cart_id = one invoice)
for cart_id, group in df.groupby("cart_id"):
    customer = group.iloc[0]

    # Prepare recipient (customer) information
    to_info = [
        customer["customer_name"],
        f"Phone: {customer['customer_phone']}",
        f"Email: {customer['customer_email']}",
        f"Addres: {customer['customer_address']}"
    ]

    # Static sender (company) information
    from_info = [
        "Jane Doe",
        "Managing Director, Company Ltd",
        "Phone: +123 4567 8910",
        "Email: janedoe@gmail.com"
    ]

    # Prepare list of purchased items
    items = []
    for _, row in group.iterrows():
        items.append({
            "description": row["product_description"],
            "unit_price": float(row["unit_price"]),
            "quantity": int(row["quantity"])
        })

    # Get tax rate and total discount
    tax_rate = float(customer["tax_rate"])
    discount = float(group["discount"].sum())

    # Create PDF invoice
    pdf = PDFInvoice(
        company_name="Mizer Companition",
        tagline="Creative Business Idea",
        invoice_number=cart_id,
        invoice_date=datetime.today().strftime('%B %d, %Y'),
        terms="Payment due in 30 days.\nNo refunds after 7 days.",
        payment_info="Account: Mizer Inc\nBank: GlobalBank\nIBAN: GB00 1234 5678 9012"
    )

    # Build the invoice layout
    pdf.set_margins()
    pdf.add_page()
    pdf.add_invoice_info(to_info=to_info, from_info=from_info)
    subtotal = pdf.add_table(items)
    pdf.add_summary_section(subtotal=subtotal, tax_rate=tax_rate, discount=discount)

    # Save the invoice as PDF
    os.makedirs("Outputs", exist_ok=True)
    pdf.output(f"Outputs/{cart_id}.pdf")

    # Log success
    log_success(cart_id)