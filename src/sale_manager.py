from datetime import datetime
import os
from src.product_manager import update_product_file

def process_sale(products, customer_name):
    """
    Process a sale transaction for a customer.
    
    This function handles the entire sales process including:
    - Displaying available products
    - Adding products to the cart
    - Calculating totals and discounts
    - Generating invoices
    - Updating inventory
    
    Args:
        products (list): List of product dictionaries with inventory information
        customer_name (str): Name of the customer making the purchase
        
    Returns:
        None
    """
    # Initialize sale variables
    total_amount = 0
    sale_details = []
    MARKUP_MULTIPLIER = 3

    # Display welcome message and header
    print(f"\n" + "="*80)
    print(f"Welcome, {customer_name}!")
    print("="*80)
    print("Available Products:")
    print(f"{'ID':^5} | {'Product Name':^30} | {'Brand':^15} | {'Price':^10} | {'Available':^10}")
    print("-"*80)
    
    # Filter and display available products with stock > 0
    in_stock_products = [p for p in products if p["quantity"] > 0]
    if not in_stock_products:
        print("\n\033[93mSorry, no products are currently in stock.\033[0m")
        return
        
    # Display available products
    for product in in_stock_products:
        selling_price = product["cost_price"] * MARKUP_MULTIPLIER
        print(f"{product['id']:^5} | {product['name']:^30} | {product['brand']:^15} | ₹{selling_price:^8.2f} | {product['quantity']:^10}")
    print("-"*80)
    
    # Product selection loop
    while True:
        product_input = input("\nEnter product ID or name to buy (or 'done' to finish): ")
        
        # Check if user is done shopping
        if product_input.lower() == 'done':
            if not sale_details:
                print("\033[93mNo items added to cart. Sale cancelled.\033[0m")
                return
            break
        
        # Find the product in inventory
        product = None
        if product_input.isdigit():
            # Search by ID
            product_id = int(product_input)
            product = next((p for p in products if p.get("id") == product_id), None)
        else:
            # Search by name
            product = next((p for p in products if p["name"].lower() == product_input.lower()), None)
            
        if not product:
            print("\033[91mProduct not found. Please try again.\033[0m")
            continue
            
        # Check if product is in stock
        if product["quantity"] <= 0:
            print(f"\033[91mSorry, {product['name']} is out of stock.\033[0m")
            continue
        
        # Get quantity from user
        valid_quantity = False
        while not valid_quantity:
            try:
                quantity = int(input(f"Enter quantity for {product['name']} (max {product['quantity']}): "))
                
                # Validate quantity
                if quantity <= 0:
                    print("\033[91mError: Quantity must be a positive number.\033[0m")
                    continue
                    
                free_quantity = quantity // 3
                total_quantity = quantity + free_quantity
                
                if total_quantity > product["quantity"]:
                    print(f"\033[91mError: Only {product['quantity']} units of {product['name']} available.\033[0m")
                    continue
                
                valid_quantity = True
                if quantity > total_quantity:
                    print("\033[91mError: Quantity exceeds available stock.\033[0m")
                    continue
                
            except ValueError:
                print("\033[91mError: Please enter a valid number.\033[0m")
        
        # Apply promotions and calculate totals
        selling_price = product["cost_price"] * MARKUP_MULTIPLIER
        item_total = selling_price * quantity 
        total_amount += item_total

        # Add to sale details
        sale_details.append({
            "product_name": product["name"],
            "brand": product["brand"],
            "quantity_sold": quantity,
            "free_quantity": free_quantity,
            "unit_price": selling_price,
            "item_total": item_total
        })
        
        # Confirm item added
        if free_quantity > 0:
            print(f"\033[92mAdded {quantity} {product['name']} to cart + {free_quantity} FREE!\033[0m")
            print(f"Item total: ₹{item_total:.2f}")
        else:
            print(f"\033[92mAdded {quantity} {product['name']} to cart.\033[0m")
            print(f"Item total: ₹{item_total:.2f}")
    
    # Display sale summary
    print("\n" + "="*80)
    print(" "*30 + "SALE SUMMARY" + " "*30)
    print("="*80)
    print(f"{'Product':<25}{'Brand':<15}{'Qty':<5}{'Free':<5}{'Unit Price':<15}{'Total':<10}")
    print("-"*80)
    
    # Show each item in the cart
    for sale in sale_details:
        print(f"{sale['product_name']:<25}{sale['brand']:<15}{sale['quantity_sold']:<5}{sale['free_quantity']:<5}₹{sale['unit_price']:<13.2f}₹{sale['item_total']:<8.2f}")
    
    # Show total and apply discounts
    print("-"*80)
    print(f"{'Total Amount:':<65}₹{total_amount:.2f}")
    
    # Apply discount for purchases over ₹1000 (5% discount)
    discount = 0
    if total_amount >= 1000:
        discount = total_amount * 0.05
        print(f"{'Discount (5%):':<65}₹{discount:.2f}")
        print(f"{'Final Amount:':<65}\033[92m₹{total_amount - discount:.2f}\033[0m")
    print("="*80)
    
    # Confirm sale with user
    while True:
        confirm = input("\nConfirm sale? (yes/no): ")
        if confirm.lower() in ['yes', 'y', 'no', 'n']:
            break
        print("\033[91mPlease enter 'yes' or 'no'.\033[0m")
    
    # Process confirmed sale
    if confirm.lower() in ['yes', 'y']:
        # Update product quantities in inventory
        for sale in sale_details:
            product = next((p for p in products if p["name"] == sale["product_name"]), None)
            if product:
                product["quantity"] -= (sale["quantity_sold"] + sale["free_quantity"])
        
        # Generate invoice and update inventory file
        invoice_path = generate_invoice(customer_name, sale_details, total_amount, discount)
        update_product_file(products)
        
        # Confirm completion
        print("\n" + "-"*80)
        print("\033[92mSale completed successfully!\033[0m")
        print(f"Invoice generated at: {invoice_path}")
        print("-"*80)
    else:
        print("\033[93mSale cancelled. No changes made to inventory.\033[0m")

def generate_invoice(customer_name, sale_details, total_amount, discount=0):
    """
    Generate an invoice for a completed sale.
    
    This function creates a formatted text invoice with all sale details,
    including products purchased, quantities, prices, and any discounts applied.
    The invoice is saved to a file in the sales_invoices directory.
    
    Args:
        customer_name (str): Name of the customer making the purchase
        sale_details (list): List of dictionaries containing sale details
        total_amount (float): Total amount of the sale before discount
        discount (float, optional): Discount amount applied to the sale
        
    Returns:
        str: Path to the generated invoice file
    """
    # Ensure directory exists for saving invoices
    os.makedirs("data/sales_invoices", exist_ok=True)
    
    # Generate a unique invoice filename with customer name and timestamp
    invoice_name = f"data/sales_invoices/Invoice_{customer_name}_{get_current_date_for_filename()}.txt"
    
    # Create and write the invoice content
    with open(invoice_name, "w") as invoice:
        # Header section
        invoice.write("="*80 + "\n")
        invoice.write(" "*30 + "WECARE" + " "*30 + "\n")
        invoice.write(" "*25 + "Your Complete Skincare Solution" + " "*25 + "\n")
        invoice.write("="*80 + "\n\n")
        
        # Invoice details section
        invoice.write(f"{'Invoice Date:':<20}{get_current_date()}\n")
        invoice.write(f"{'Invoice Number:':<20}INV-{get_current_date_for_filename()}\n")
        invoice.write(f"{'Customer Name:':<20}{customer_name}\n\n")
        
        # Items section
        invoice.write("="*80 + "\n")
        invoice.write(f"{'Product':<25}{'Brand':<15}{'Qty':<5}{'Free':<5}{'Unit Price':<15}{'Total':<10}\n")
        invoice.write("-"*80 + "\n")
        
        # List each item purchased
        for sale in sale_details:
            invoice.write(f"{sale['product_name']:<25}{sale['brand']:<15}{sale['quantity_sold']:<5}{sale['free_quantity']:<5}₹{sale['unit_price']:<13.2f}₹{sale['item_total']:<8.2f}\n")
        
        # Totals section
        invoice.write("-"*80 + "\n")
        invoice.write(f"{'Subtotal:':<65}₹{total_amount:.2f}\n")
        
        # Apply discount if applicable
        if discount > 0:
            invoice.write(f"{'Discount (5%):':<65}₹{discount:.2f}\n")
            invoice.write(f"{'Final Amount:':<65}₹{total_amount - discount:.2f}\n")
        
        # Footer section
        invoice.write("="*80 + "\n\n")
        invoice.write(" "*20 + "Thank you for shopping with WeCare!" + " "*20 + "\n")
        invoice.write(" "*25 + "We Care Because You Matter" + " "*25 + "\n")
        invoice.write(" "*30 + "Visit us again soon!" + " "*30 + "\n")
    
    return invoice_name

def get_current_date():
    """
    Get the current date in YYYY-MM-DD format.
    
    This function returns the current date formatted as a string,
    suitable for display in invoices and reports.
    
    Returns:
        str: Current date string in YYYY-MM-DD format
    """
    return datetime.now().strftime("%Y-%m-%d")

def get_current_date_for_filename():
    """
    Get the current date and time for use in filenames.
    
    This function returns the current date and time formatted as a string,
    suitable for creating unique filenames. The format includes seconds
    to ensure uniqueness even for multiple files created in quick succession.
    
    Returns:
        str: Current date and time string in YYYY-MM-DD_HH-MM-SS format
    """
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")