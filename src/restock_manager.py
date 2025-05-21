from datetime import datetime
import os
from src.product_manager import update_product_file

def restock_products(products):
    """
    Handle the restocking of existing products or adding new products to inventory.
    
    This function provides a submenu for restocking operations, allowing users to
    either add stock to existing products or add completely new products to the inventory.
    
    Args:
        products (list): List of product dictionaries containing inventory information
        
    Returns:
        None
    """
    # Display header
    print("\n" + "="*80)
    print(" "*30 + "RESTOCK PRODUCTS" + " "*30)
    print("="*80)
    
    # Display menu options
    print("\n  1. Restock Existing Product  - Add inventory to products already in system")
    print("  2. Return to Main Menu     - Go back to main menu")
    
    # Get user choice with validation
    while True:
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if choice in [1, 2]:
                break
            print("\033[91mError: Please enter a number between 1 and 3.\033[0m")
        except ValueError:
            print("\033[91mError: Please enter a valid number.\033[0m")
    
    # Process user choice
    if choice == 1:
        restock_existing_product(products)
    elif choice == 2:
        return
    
    # Save changes to file
    update_product_file(products)

def restock_existing_product(products):
    """
    Restock an existing product in the inventory.
    
    This function allows users to add more stock to existing products and
    optionally update the cost price. It generates a restock invoice for
    record-keeping and updates the inventory.
    
    Args:
        products (list): List of product dictionaries containing inventory information
        
    Returns:
        None
    """
    # Check if there are products to restock
    if not products:
        print("\n" + "="*80)
        print(" "*30 + "RESTOCK PRODUCTS" + " "*30)
        print("="*80)
        print("\n\033[93mNo products available in inventory to restock. Please add products first.\033[0m")
        return
        
    # Display current inventory
    print("\n" + "="*80)
    print(" "*30 + "CURRENT INVENTORY" + " "*30)
    print("="*80)
    print(f"{'Product Name':^30} | {'Brand':^15} | {'Cost Price':^15} | {'Stock':^10}")
    print("-"*80)
    
    # Show each product with current stock and cost price
    for product in products:
        # Highlight low stock items
        if product['quantity'] <= 5:
            quantity_display = f"!!! {product['quantity']} !!!"
        else:
            quantity_display = str(product['quantity'])
            
        print(f"{product['name']:^30} | {product['brand']:^15} | ₹{product['cost_price']:^13.2f} | {quantity_display:^10}")
    
    print("-"*80)
    
    # Initialize restock process variables
    restock_details = []
    total_cost = 0
    
    # Product selection loop
    while True:
        product_name = input("\nEnter product name to restock (or 'done' to finish): ")
        
        # Check if user is done restocking
        if product_name.lower() == 'done':
            if not restock_details:
                print("\033[93mNo products restocked. Returning to menu.\033[0m")
                return
            break
        
        # Find the product in inventory
        product = next((p for p in products if p["name"].lower() == product_name.lower()), None)
        if not product:
            print("\033[91mProduct not found. Please try again or add as a new product.\033[0m")
            continue
        
        # Get restock quantity with validation
        while True:
            try:
                quantity = int(input(f"Enter quantity to add for {product_name}: "))
                if quantity <= 0:
                    print("\033[91mError: Quantity must be a positive integer.\033[0m")
                else:
                    break
            except ValueError:
                print("\033[91mError: Invalid input. Please enter a valid quantity.\033[0m")
        
        # Get new cost price with validation
        while True:
            try:
                cost_price = float(input(f"Enter new cost price for {product_name} (current: ₹{product['cost_price']:.2f}): "))
                if cost_price < 0:
                    print("\033[91mError: Cost price cannot be negative.\033[0m")
                else:
                    break
            except ValueError:
                print("\033[91mError: Invalid input. Please enter a valid cost price.\033[0m") 
        
        # Update product in inventory
        old_quantity = product["quantity"]
        old_cost_price = product["cost_price"]
        product["quantity"] += quantity
        product["cost_price"] = cost_price
        
        # Calculate costs
        item_cost = cost_price * quantity
        total_cost += item_cost
        
        # Add to restock details for invoice
        restock_details.append({
            "product_name": product["name"],
            "brand": product["brand"],
            "quantity": quantity,
            "cost_price": cost_price,
            "old_quantity": old_quantity,
            "old_cost_price": old_cost_price,
            "item_cost": item_cost
        })
        
        # Confirm restock action
        print(f"\033[92mAdded {quantity} units of {product_name} at ₹{cost_price:.2f} each.\033[0m")
        print(f"Item cost: ₹{item_cost:.2f}")
        print(f"New stock level: {old_quantity} + {quantity} = {product['quantity']}")
    
    # Display restock summary if items were restocked
    if restock_details:
        print("\n" + "="*80)
        print(" "*30 + "RESTOCK SUMMARY" + " "*30)
        print("="*80)
        print(f"{'Product':<25}{'Brand':<15}{'Quantity':<10}{'Cost Price':<15}{'Total':<15}")
        print("-"*80)
        
        # Display each restocked item
        for item in restock_details:
            print(f"{item['product_name']:<25}{item['brand']:<15}{item['quantity']:<10}₹{item['cost_price']:<13.2f}₹{item['item_cost']:<13.2f}")
        
        # Show total cost
        print("-"*80)
        print(f"{'Total Cost:':<50}\033[92m₹{total_cost:.2f}\033[0m")
        print("="*80)
        
        # Generate and save restock invoice
        invoice_path = generate_restock_invoice(restock_details, total_cost)
        
        # Confirm completion
        print("\n" + "-"*80)
        print("\033[92mRestock operation completed successfully!\033[0m")
        print(f"Restock invoice generated at: {invoice_path}")
        print("-"*80)

def generate_restock_invoice(restock_details, total_cost):
    """
    Generate an invoice for a restock operation.
    
    This function creates a formatted text invoice with all restock details,
    including products, quantities, cost prices, and total cost. The invoice
    is saved to a file in the restock_invoices directory.
    
    Args:
        restock_details (list): List of dictionaries containing restock details
        total_cost (float): Total cost of the restock operation
        
    Returns:
        str: Path to the generated invoice file
    """
    # Ensure directory exists for saving invoices
    os.makedirs("data/restock_invoices", exist_ok=True)
    
    # Use the first product for the invoice name and create a unique filename
    first_product = restock_details[0]["product_name"]
    timestamp = get_current_date_for_filename()
    invoice_name = f"data/restock_invoices/Restock_Invoice_{first_product}_{timestamp}.txt"
    
    # Create and write the invoice content
    with open(invoice_name, "w") as invoice:
        # Header section
        invoice.write("="*80 + "\n")
        invoice.write(" "*30 + "WECARE" + " "*30 + "\n")
        invoice.write(" "*25 + "RESTOCK INVOICE" + " "*25 + "\n")
        invoice.write("="*80 + "\n\n")
        
        # Invoice details section
        invoice.write(f"{'Date:':<20}{get_current_date()}\n")
        invoice.write(f"{'Invoice Number:':<20}RESTOCK-{timestamp}\n")
        invoice.write(f"{'Products Restocked:':<20}{len(restock_details)}\n\n")
        
        # Items section
        invoice.write("="*80 + "\n")
        invoice.write(f"{'Product':<25}{'Brand':<15}{'Quantity':<10}{'Cost Price':<15}{'Total':<15}\n")
        invoice.write("-"*80 + "\n")
        
        # List each restocked item
        for item in restock_details:
            invoice.write(f"{item['product_name']:<25}{item['brand']:<15}{item['quantity']:<10}₹{item['cost_price']:<13.2f}₹{item['item_cost']:<13.2f}\n")
        
        # Totals section
        invoice.write("-"*80 + "\n")
        invoice.write(f"{'Total Cost:':<65}₹{total_cost:.2f}\n")
        invoice.write("="*80 + "\n\n")
        
        # Footer section
        invoice.write(" "*25 + "Thank you for your business" + " "*25 + "\n")
        invoice.write(" "*20 + "WeCare - Your Healthcare Partner" + " "*20 + "\n")
    
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