import os
import sys
from src.product_manager import load_products, edit_product_information
from src.sale_manager import process_sale
from src.restock_manager import restock_products

def display_products(products):
    """
    Display all available products in a formatted table.
    
    Args:
        products (list): List of product dictionaries containing product information
                        Each dictionary should have keys: name, brand, cost_price, quantity, country
    
    Returns:
        None
    """
    # Define markup for selling price calculation
    MARKUP_MULTIPLIER = 3

    # Handle empty inventory case
    if not products:
        print("\n" + "="*80)
        print(" "*30 + "INVENTORY STATUS" + " "*30)
        print("="*80)
        print("\nNo products available in inventory. Please restock products.")
        return
    
    # Display header    
    print("\n" + "="*80)
    print(" "*30 + "AVAILABLE PRODUCTS" + " "*30)
    print("="*80)
    
    # Display column headers
    print(f"{'ID':^5} | {'Product Name':^30} | {'Brand':^15} | {'Selling Price':^15} | {'Stock':^10} | {'Country':^15}")
    print("-"*105)
    
    # Display each product with formatted values
    for product in products:
        selling_price = product["cost_price"] * MARKUP_MULTIPLIER
        if product["quantity"] <= 5:
            quantity_display = f"!!! {product['quantity']} !!!"
        else:
            quantity_display = str(product['quantity'])
            
        print(f"{product['id']:^5} | {product['name']:^30} | {product['brand']:^15} | ₹{selling_price:^13.2f} | {quantity_display:^10} | {product['country']:^15}")
    
    print("-"*95)
    print(f"{'Total Products:':^30} {len(products):^5}")
    print("\n" + "="*95)

def display_menu():
    """
    Display the main menu of the WeCare Inventory System.
    
    This function clears the screen and displays a formatted menu with options
    for the user to interact with the system.
    
    Returns:
        None
    """
    # Clear screen for better user experience
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Display header banner
    print("\n" + "*"*80)
    print("*" + " "*78 + "*")
    print("*" + "WELCOME TO WECARE".center(78) + "*")
    print("*" + "Your Complete Skincare Inventory Solution".center(78) + "*")
    print("*" + " "*78 + "*")
    print("*"*80)
    
    # Display menu options
    print("\n" + "="*40 + " Main Menu " + "="*40 + "\n")
    print("  1. View Products        - Display all products in inventory")
    print("  2. Process Sale        - Record a customer purchase")
    print("  3. Restock Products    - Add inventory to existing products")
    print("  4. Update Information  - Edit product details or add new products")
    print("  5. Exit                - Close the application")
    print("\n" + "="*80 + "\n")

def get_valid_choice(prompt, valid_range):
    """
    Get a valid integer choice from the user within the specified range.
    
    This function repeatedly prompts the user until they enter a valid integer
    within the specified range.
    
    Args:
        prompt (str): The prompt to display to the user
        valid_range (range): The range of valid choices (e.g., range(1, 6) for choices 1-5)
        
    Returns:
        int: The validated user choice
    """
    while True:
        try:
            # Get user input and convert to integer
            choice = int(input(prompt))
            
            # Validate the choice is within the acceptable range
            if choice in valid_range:
                return choice
                
            # Display error message for out-of-range values
            print(f"\033[91mError: Please enter a number between {valid_range.start} and {valid_range.stop-1}.\033[0m")
        except ValueError:
            # Handle non-integer inputs
            print("\033[91mError: Please enter a valid number.\033[0m")

def main():
    """
    Main function to run the WeCare Inventory System.
    
    This function initializes the system, loads product data, and handles the main
    application loop. It also includes error handling for graceful exits.
    
    Returns:
        None
    """
    # Ensure required directories exist
    os.makedirs("data/sales_invoices", exist_ok=True)
    os.makedirs("data/restock_invoices", exist_ok=True)
    
    try:
        # Load product data from file
        products = load_products("data/products.txt")        
        # Main application loop
        while True:
            display_menu()
            choice = get_valid_choice("Enter your choice (1-5): ", range(1, 6))
            
            if choice == 1:
                # Display available products
                display_products(products)
                input("\nPress Enter to return to main menu...")
                
            elif choice == 2:
                # Process sale
                print("\n" + "="*80)
                print(" "*30 + "PROCESS SALE" + " "*30)
                print("="*80)
                
                while True:
                    customer_name = input("\nEnter customer name: ").strip()

                    if customer_name == "":
                        print("\033[91mError: Customer name cannot be empty.\033[0m")
                    elif any(char.isdigit() for char in customer_name):
                        print("\033[91mError: Customer name cannot contain numbers.\033[0m")
                    elif not all(c.isalpha() or c.isspace() for c in customer_name):
                        print("\033[91mError: Please enter a valid customer name (letters and spaces only).\033[0m")
                    else:
                        break
                
                process_sale(products, customer_name)
                input("\nPress Enter to return to main menu...")
                
            elif choice == 3:
                # Restock products
                restock_products(products)
                input("\nPress Enter to return to main menu...")
                
            elif choice == 4:
                # Update product information
                edit_product_information(products)
                input("\nPress Enter to return to main menu...")
                
            elif choice == 5:
                print("\n" + "*"*80)
                print("*" + " "*78 + "*")
                print("*" + "Thank you for using WeCare!".center(78) + "*")
                print("*" + "Goodbye!".center(78) + "*")
                print("*" + " "*78 + "*")
                print("*"*80)
                sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Saving data and exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91mAn unexpected error occurred: {e}\033[0m")
        print("The system will now exit. Please restart the application.")
        sys.exit(1)

if __name__ == "__main__":
    main()