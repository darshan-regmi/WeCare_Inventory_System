def load_products(file_path: str) -> list:
    """
    Loads products from a file.

    Args:
    file_path (str): The path to the file containing the products.

    Returns:
    list: A list of dictionaries, each representing a product.
    """
    try:
        with open(file_path, "r") as file:
            products = [
                {
                    "name": line.strip().split(",")[0],
                    "brand": line.strip().split(",")[1],
                    "quantity": int(line.strip().split(",")[2]),
                    "cost_price": float(line.strip().split(",")[3]),
                    "country": line.strip().split(",")[4]
                }
                for line in file
            ]
    except FileNotFoundError:
        print("Product file not found.")
        products = []
    except Exception as e:
        print(f"An error occurred: {e}")
        products = []
    return products

def update_product_file(products: list) -> None:
    """
    Updates the product file with the given products.

    Args:
    products (list): A list of dictionaries, each representing a product.
    """
    try:
        with open("data/products.txt", "w") as file:
            for product in products:
                file.write(
                    f"{product['name']},{product['brand']},{product['quantity']},{product['cost_price']},{product['country']}\n"
                )
    except Exception as e:
        print(f"An error occurred: {e}")