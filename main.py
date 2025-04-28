from src.product_manager import load_products, update_product_file
from src.sale_manager import process_sale
from src.restock_manager import restock_products

def display_products(products):
    print("\n" + "="*40 + " Available Products " + "="*40 + "\n")
    print(f"{'Product Name':^30} | {'Brand':^10} | {'Selling Price':^15} | {'Stock':^10}")
    print("-"*80)
    for product in products:
        selling_price = product["cost_price"] * 2  # 200% markup
        print(f"{product['name']:^30} | {product['brand']:^10} | ₹{selling_price:^15} | {product['quantity']:^10}")
    print("\n" + "="*80 + "\n")

def display_menu():
    print("\n" + "="*40 + " Main Menu " + "="*40 + "\n")
    print("1. View Products")
    print("2. Process Sale")
    print("3. Restock Products")
    print("4. Update Product Information")
    print("5. Exit")
    print("\n" + "="*80 + "\n")

def main():
    products = load_products("data/products.txt")
    while True:
        display_menu()
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            # Display available products
            display_products(products)
        elif choice == 2:
            customer_name = input("Enter customer name: ")
            process_sale(products, customer_name)
        elif choice == 3:
            restock_products(products)
        elif choice == 4:
            update_product_file(products)
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()