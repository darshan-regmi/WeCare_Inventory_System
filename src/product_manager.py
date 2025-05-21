import os

def load_products(file_path: str):
    """
    Loads products from a file or creates a new file if it doesn't exist.

    This function reads product data from a CSV-formatted file where each line
    represents a product with comma-separated values. The expected format is:
    name,brand,quantity,cost_price,country

    Args:
        file_path (str): The path to the file containing the products

    Returns:
        list: A list of dictionaries, each representing a product with keys:
              id, name, brand, quantity, cost_price, country
    """
    products = []
    
    try:
        # Create the file if it doesn't exist
        if not os.path.exists(file_path):
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
                
            with open(file_path, "w") as file:
                # Write empty file
                pass
            print(f"Created new product file at {file_path}")
            return products
            
        # Read products from file
        print(f"Reading products from {file_path}...")
        with open(file_path, "r") as file:
            line_number = 0
            valid_products = 0
            invalid_lines = 0
            
            for line in file:
                line_number += 1
                if not line.strip():
                    continue  # Skip empty lines
                    
                parts = line.strip().split(",")
                if len(parts) < 5:
                    print(f"\033[93mWarning: Invalid product format on line {line_number}: {line.strip()}\033[0m")
                    invalid_lines += 1
                    continue
                    
                try:
                    products.append({
                        "name": parts[0].strip(),
                        "brand": parts[1].strip(),
                        "quantity": int(parts[2].strip()),
                        "cost_price": float(parts[3].strip()),
                        "country": parts[4].strip()
                    })
                    valid_products += 1
                except (ValueError, IndexError) as e:
                    print(f"\033[91mError parsing product on line {line_number}: {line.strip()} - {e}\033[0m")
                    invalid_lines += 1
            
            # Summary of loading process
            if invalid_lines > 0:
                print(f"Loaded {valid_products} products successfully. Found {invalid_lines} invalid entries.")
            else:
                print(f"Loaded {valid_products} products successfully.")
                    
    except FileNotFoundError:
        print(f"\033[91mProduct file not found: {file_path}\033[0m")
    except Exception as e:
        print(f"\033[91mAn error occurred while loading products: {e}\033[0m")
    
    # Assign IDs to products (1-based indexing)
    for i, product in enumerate(products, 1):
        product["id"] = i
        
    return products

def update_product_file(products: list) -> None:
    """
    Updates the product file with the given products.

    This function writes all products to the data file in CSV format.
    Each product is written as a single line with comma-separated values.

    Args:
        products (list): A list of dictionaries, each representing a product
        
    Returns:
        None
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname("data/products.txt")
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        
        # Count products being saved    
        product_count = len(products)
        
        # Write products to file
        with open("data/products.txt", "w") as file:
            for product in products:
                file.write(
                    f"{product['name']},{product['brand']},{product['quantity']},{product['cost_price']},{product['country']}\n"
                )
        
        # Success message
        print(f"\033[92mProduct file updated successfully. Saved {product_count} products.\033[0m")
    except Exception as e:
        print(f"\033[91mAn error occurred while updating product file: {e}\033[0m")

def edit_product_information(products: list) -> None:
    """
    Edit existing product information or add new products to the inventory.
    
    This function provides a submenu for editing existing products or adding
    new products to the inventory. Changes are saved to the product file.
    
    Args:
        products (list): A list of dictionaries, each representing a product
        
    Returns:
        None
    """
    while True:
        # Display submenu header
        print("\n" + "="*80)
        print(" "*30 + "UPDATE PRODUCT INFORMATION" + " "*30)
        print("="*80)
        
        # Display menu options
        print("\n  1. Edit Existing Product  - Modify details of products in inventory")
        print("  2. Add New Product      - Add a completely new product to inventory")
        print("  3. Return to Main Menu  - Go back to main menu")
        
        try:
            # Get user choice
            choice = int(input("\nEnter your choice (1-3): "))
            
            # Process user choice
            if choice == 1:
                edit_existing_product(products)
            elif choice == 2:
                add_new_product(products)
            elif choice == 3:
                break
            else:
                print("\033[91mInvalid choice. Please enter a number between 1 and 3.\033[0m")
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number.\033[0m")
    
    # Save changes to file
    update_product_file(products)

def edit_existing_product(products: list) -> None:
    """
    Edit an existing product's information.
    
    This function displays all products and allows the user to select one to edit.
    The user can then modify specific attributes of the selected product.
    
    Args:
        products (list): A list of dictionaries, each representing a product
        
    Returns:
        None
    """
    # Check if there are products to edit
    if not products:
        print("\n" + "="*80)
        print(" "*30 + "EDIT PRODUCT" + " "*30)
        print("="*80)
        print("\n\033[93mNo products available to edit. Please add products first.\033[0m")
        return
    
    # Display current products with a numbered list
    print("\n" + "="*80)
    print(" "*30 + "CURRENT PRODUCTS" + " "*30)
    print("="*80)
    print(f"{'#':^5} | {'Product Name':^30} | {'Brand':^15} | {'Cost Price':^15} | {'Stock':^10}")
    print("-"*85)
    
    for idx, product in enumerate(products, 1):
        print(f"{idx:^5} | {product['name']:^30} | {product['brand']:^15} | ₹{product['cost_price']:^13.2f} | {product['quantity']:^10}")
    
    # Select product to edit
    while True:
        try:
            product_idx = int(input("\nEnter product number to edit (or 0 to cancel): "))
            if product_idx == 0:
                return
            if 1 <= product_idx <= len(products):
                break
            print(f"\033[91mError: Please enter a number between 1 and {len(products)}.\033[0m")
        except ValueError:
            print("\033[91mError: Invalid input. Please enter a valid number.\033[0m")
    
    # Get the selected product
    product = products[product_idx - 1]
    
    # Choose attribute to modify
    print("\n" + "="*40 + f" Editing {product['name']} " + "="*40)
    print("  1. Name        - Change product name")
    print("  2. Brand       - Change manufacturer/brand name")
    print("  3. Quantity    - Update stock quantity")
    print("  4. Cost Price  - Update purchase price")
    print("  5. Country     - Change country of origin")
    print("  6. Cancel      - Return without changes")
    
    while True:
        try:
            attr_choice = int(input("\nSelect attribute to modify (1-6): "))
            if 1 <= attr_choice <= 6:
                break
            print("\033[91mError: Please enter a number between 1 and 6.\033[0m")
        except ValueError:
            print("\033[91mError: Invalid input. Please enter a valid number.\033[0m")
    
    # Store original values for confirmation message
    old_values = {}
    
    # Modify the selected attribute
    if attr_choice == 1:
        old_values['name'] = product['name']
        new_value = input(f"Enter new name (current: {product['name']}): ").strip()
        if new_value:
            product['name'] = new_value
        else:
            print("\033[93mName unchanged - empty value provided.\033[0m")
            return
    elif attr_choice == 2:
        old_values['brand'] = product['brand']
        new_value = input(f"Enter new brand (current: {product['brand']}): ").strip()
        if new_value:
            product['brand'] = new_value
        else:
            print("\033[93mBrand unchanged - empty value provided.\033[0m")
            return
    elif attr_choice == 3:
        old_values['quantity'] = product['quantity']
        try:
            new_value = int(input(f"Enter new quantity (current: {product['quantity']}): "))
            if new_value >= 0:
                product['quantity'] = new_value
            else:
                print("\033[91mError: Quantity cannot be negative.\033[0m")
                return
        except ValueError:
            print("\033[91mError: Invalid input. Quantity must be a number.\033[0m")
            return
    elif attr_choice == 4:
        old_values['cost_price'] = product['cost_price']
        try:
            new_value = float(input(f"Enter new cost price (current: ₹{product['cost_price']:.2f}): "))
            if new_value >= 0:
                product['cost_price'] = new_value
            else:
                print("\033[91mError: Cost price cannot be negative.\033[0m")
                return
        except ValueError:
            print("\033[91mError: Invalid input. Cost price must be a number.\033[0m")
            return
    elif attr_choice == 5:
        old_values['country'] = product['country']
        new_value = input(f"Enter new country (current: {product['country']}): ").strip()
        if new_value:
            product['country'] = new_value
        else:
            print("\033[93mCountry unchanged - empty value provided.\033[0m")
            return
    elif attr_choice == 6:
        return
    
    # Show confirmation with before/after values
    print("\n" + "-"*80)
    if 'name' in old_values:
        print(f"Product name updated: '{old_values['name']}' → '{product['name']}'")
    elif 'brand' in old_values:
        print(f"Brand updated: '{old_values['brand']}' → '{product['brand']}'")
    elif 'quantity' in old_values:
        print(f"Quantity updated: {old_values['quantity']} → {product['quantity']}")
    elif 'cost_price' in old_values:
        print(f"Cost price updated: ₹{old_values['cost_price']:.2f} → ₹{product['cost_price']:.2f}")
    elif 'country' in old_values:
        print(f"Country updated: '{old_values['country']}' → '{product['country']}'")
    print("-"*80)
    
    print(f"\n\033[92mProduct '{product['name']}' updated successfully.\033[0m")

def add_new_product(products: list) -> None:
    """
    Add a new product to the inventory.
    
    This function collects information about a new product and adds it to the inventory.
    It validates all inputs to ensure data integrity.
    
    Args:
        products (list): A list of dictionaries, each representing a product
        
    Returns:
        None
    """
    print("\n" + "="*80)
    print(" "*30 + "ADD NEW PRODUCT" + " "*30)
    print("="*80)
    
    # Get product details with validation
    while True:
        name = input("\nEnter product name: ").strip()
        if not name:
            print("\033[91mError: Product name cannot be empty.\033[0m")
            continue
            
        # Check if product already exists
        if any(p["name"].lower() == name.lower() for p in products):
            print(f"\033[93mProduct '{name}' already exists. Please use edit option instead.\033[0m")
            continue
        
        break
    
    # Get brand with default value
    brand = input("Enter brand name: ").strip() or "Generic"
    if brand == "Generic":
        print("\033[93mUsing default brand: 'Generic'\033[0m")
    
    # Get quantity with validation
    while True:
        try:
            quantity = int(input("Enter initial quantity: "))
            if quantity < 0:
                print("\033[91mError: Quantity cannot be negative.\033[0m")
                continue
            break
        except ValueError:
            print("\033[91mError: Invalid input. Please enter a valid quantity.\033[0m")
    
    # Get cost price with validation
    while True:
        try:
            cost_price = float(input("Enter cost price: "))
            if cost_price < 0:
                print("\033[91mError: Cost price cannot be negative.\033[0m")
                continue
            break
        except ValueError:
            print("\033[91mError: Invalid input. Please enter a valid cost price.\033[0m")
    
    # Get country with default value
    country = input("Enter country of origin: ").strip() or "Unknown"
    if country == "":
        country = "Unknown"
        print("\033[93mUsing default country: 'Unknown'\033[0m")
    
    # Create and add new product
    new_product = {
        "name": name,
        "brand": brand,
        "quantity": quantity,
        "cost_price": cost_price,
        "country": country
    }
    
    # Assign ID to new product (highest ID + 1)
    max_id = 0
    for product in products:
        if product.get("id", 0) > max_id:
            max_id = product["id"]
    new_product["id"] = max_id + 1
    
    products.append(new_product)
    
    # Display product summary
    print("\n" + "-"*80)
    print("PRODUCT ADDED SUCCESSFULLY:")
    print(f"  ID:         {new_product['id']}")
    print(f"  Name:       {name}")
    print(f"  Brand:      {brand}")
    print(f"  Quantity:   {quantity}")
    print(f"  Cost Price: ₹{cost_price:.2f}")
    print("-"*80)
    
    print(f"\n\033[92mNew product '{name}' added successfully.\033[0m")

