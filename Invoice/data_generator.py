from typing import List, Dict
from faker import Faker
import random
import pandas as pd

fake = Faker()

PRODUCTS = [
    'Web Development', 'Maintenance Plan', 'SSL Certificate',
    'Brand Strategy Consultation', 'Logo Design', 
    'IT Infrastructure Setup', 'On-Site Support', 'Training Session'
]

UNIT_PRICES = {
    'Web Development': 1200, 
    'Maintenance Plan': 300,
    'SSL Certificate': 75, 
    'Brand Strategy Consultation': 950,
    'Logo Design': 600, 
    'IT Infrastructure Setup': 2000,
    'On-Site Support': 500, 
    'Training Session': 250  
}

DEFAULT_TAX_RATE = 0.1  # 10% tax

def generate_customer_info() -> Dict:
    name = fake.name()
    return {
        'name': name,
        'email': f"{name.replace(' ', '').lower()}@gmail.com",
        'phone': fake.phone_number(),
        'address': fake.address().replace('\n', ', ')
    }

def generate_order_items(num_items: int) -> List[Dict]:
    items = []
    cart_id = f"INV-{random.randint(100000, 999999)}"
    
    for _ in range(num_items):
        product = random.choice(PRODUCTS)
        quantity = random.randint(1, 3)
        unit_price = UNIT_PRICES[product]
        discount = round(random.uniform(0, 15), 2)
        items.append({
            'cart_id': cart_id,
            'description': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'tax_rate': DEFAULT_TAX_RATE,
            'discount': discount
        })
    return items

def generate_dataset(num_customers=10, min_items=1, max_items=5) -> pd.DataFrame:
    data = []
    for _ in range(num_customers):
        customer = generate_customer_info()
        items = generate_order_items(random.randint(min_items, max_items))
        for item in items:
            record = {
                'customer_name': customer['name'],
                'customer_email': customer['email'],
                'customer_phone': customer['phone'],
                'customer_address': customer['address'],
                **item
            }
            data.append(record)
    return pd.DataFrame(data)
