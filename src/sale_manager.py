from datetime import datetime
from src.product_manager import update_product_file

def process_sale(products, customer_name):
    total_amount = 0
    sale_details = []

    print(f"Welcome, {customer_name}!")
    while True:
        product_name = input("Enter product name to buy (or 'done' to finish): ")
        if product_name == 'done':
            break
        
        product = next((p for p in products if p["name"].lower() == product_name.lower()), None)
        if not product:
            print("Product not found. Please try again.")
            continue
        
        quantity = int(input(f"Enter quantity for {product_name}: "))
        if quantity > product["quantity"]:
            print("Not enough stock available.")
            continue
        
        free_quantity = quantity // 3
        total_quantity = quantity + free_quantity
        selling_price = product["cost_price"] * 2  # 200% markup
        total_amount += selling_price * quantity  # Total amount for this sale

        sale_details.append({
            "product_name": product["name"],
            "brand": product["brand"],
            "quantity_sold": quantity,
            "free_quantity": free_quantity
        })
        
        product["quantity"] -= total_quantity
    
    print("\nSale Summary:")
    for sale in sale_details:
        print(f"{sale['product_name']} - {sale['brand']}, Quantity: {sale['quantity_sold']} (Free: {sale['free_quantity']})")
    print(f"\nTotal Amount: ₹{total_amount}")
    
    confirm = input("\nConfirm sale? (yes/no): ")
    if confirm.lower() == 'yes':
        generate_invoice(customer_name, sale_details, total_amount)
        update_product_file(products)
        print("Sale confirmed and invoice generated.")
    else:
        print("Sale cancelled.")

def generate_invoice(customer_name, sale_details, total_amount):
    invoice_name = f"data/sales_invoices/Invoice_{customer_name}_{get_current_date_for_filename()}.txt"
    with open(invoice_name, "w") as invoice:
        invoice.write(f"{'Customer Name:':<20}{customer_name}\n")
        invoice.write(f"{'Date:':<20}{get_current_date()}\n")
        invoice.write(f"{'Total Amount:':<20}₹{total_amount}\n\n")
        
        # Proper formatting for product details in the invoice
        invoice.write(f"{'Product':<20}{'Brand':<20}{'Quantity':<10}{'Free':<5}\n")
        for sale in sale_details:
            invoice.write(f"{sale['product_name']:<20}{sale['brand']:<20}{sale['quantity_sold']:<10}{sale['free_quantity']:<5}\n")

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_current_date_for_filename():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Adding time to make the filename unique