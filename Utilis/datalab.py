from typing import List, Dict, Optional
from faker import Faker
import pandas as pd
import random

fake = Faker()

class DatasetGenerator:
    def __init__(self):
        self.products = [
            'Web Development', 'Maintenance Plan', 'SSL Certificate',
            'Brand Strategy Consultation', 'Logo Design', 
            'IT Infrastructure Setup', 'On-Site Support', 'Training Session'
        ]
        
        self.unit_prices = {
            'Web Development': 1200, 
            'Maintenance Plan': 300,
            'SSL Certificate': 75, 
            'Brand Strategy Consultation': 950,
            'Logo Design': 600, 
            'IT Infrastructure Setup': 2000,
            'On-Site Support': 500, 
            'Training Session': 250  
        }
        
        self.default_tax_rate = 0.1  # 10% tax
        
    def _generate_customer_info(self) -> Dict:
        name = fake.name()
        return {
            'name': name,
            'email': f"{name.replace(' ', '').lower()}@gmail.com",
            'phone': fake.phone_number(),
            'address': fake.address().replace('\n', ', ')
        }
    
    def _generate_order_items(self, customer_name: str, num_items: int) -> List[Dict]:
        items = []
        cart_id = f"INV-{random.randint(100000, 999999)}"
        
        for _ in range(num_items):
            product = random.choice(self.products)
            quantity = random.randint(1, 3)
            unit_price = self.unit_prices[product]
            discount = round(random.uniform(0, 15), 2)  # Discount between 0% and 15%
            
            items.append({
                'cart_id': cart_id,
                'product_description': product,
                'quantity': quantity,
                'unit_price': unit_price,
                'tax_rate': self.default_tax_rate,
                'discount': discount
            })
        
        return items
    
    def generate_dataset(self, number_of_customers: int = 10, min_items: int = 1, max_items: int = 5) -> pd.DataFrame:
        data = []
        for _ in range(number_of_customers):
            customer = self._generate_customer_info()
            order_items = self._generate_order_items(
                customer['name'],
                random.randint(min_items, max_items)
            )
            
            for item in order_items:
                record = {
                    'customer_name': customer['name'],
                    'customer_email': customer['email'],
                    'customer_phone': customer['phone'],
                    'customer_address': customer['address'],
                    **item
                }
                data.append(record)
        
        return pd.DataFrame(data)
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = "orders.csv") -> None:
        df.to_csv(filename, index=False)
        print(f"Dataset saved to {filename}")


def main():
    # Initialize the generator
    generator = DatasetGenerator()
    
    # Generate dataset
    df = generator.generate_dataset(number_of_customers=10, min_items=1, max_items=5)
    
    # Display the dataset
    #print("Generated Dataset:")
    display(df)
    
    # Save to CSV
    generator.save_to_csv(df, "orders.csv")

if __name__ == "__main__":
    main()