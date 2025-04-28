from datetime import datetime
from src.product_manager import update_product_file

def restock_products(products):
    print("\nRestock Products")
    print("----------------")
    while True:
        product_name = input("Enter product name to restock (or 'done' to finish): ")
        if product_name == 'done':
            break
        
        product = next((p for p in products if p["name"].lower() == product_name.lower()), None)
        if not product:
            print("Product not found. Please try again.")
            continue
        
        while True:
            try:
                quantity = int(input(f"Enter quantity for {product_name}: "))
                if quantity <= 0:
                    print("Quantity must be a positive integer.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid quantity.")
        
        while True:
            try:
                cost_price = float(input(f"Enter cost price for {product_name}: "))
                if cost_price < 0:
                    print("Cost price cannot be negative.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid cost price.") 
        
        product["quantity"] += quantity
        product["cost_price"] = cost_price
        
        generate_restock_invoice(product, quantity, cost_price)

    update_product_file(products)

def generate_restock_invoice(product, quantity, cost_price):
    invoice_name = f"data/restock_invoices/Restock_Invoice_{product['name']}_{get_current_date()}.txt"
    with open(invoice_name, "w") as invoice:
        invoice.write(f"{'Restock Invoice':^40}\n")
        invoice.write(f"{'Product':<20}: {product['name']}\n")
        invoice.write(f"{'Brand':<20}: {product['brand']}\n")
        invoice.write(f"{'Quantity Restocked':<20}: {quantity}\n")
        invoice.write(f"{'Cost Price':<20}: ₹{cost_price:.2f}\n")
        invoice.write(f"{'Date':<20}: {get_current_date()}\n")
        invoice.write(f"{'Total Amount':<20}: ₹{cost_price * quantity:.2f}\n")
        invoice.write(f"{'-------------------------':<40}\n")
        invoice.write(f"{'Thank you for restocking with us.':^40}\n")

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")