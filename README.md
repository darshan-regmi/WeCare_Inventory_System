# WeCare Inventory System

## Overview

This project is a Python-based application designed to manage sales, stock, and restocking of beauty and skincare products in a store. It implements a "Buy 3, Get 1 Free" policy, updates stock in real-time, and generates invoices for both sales and restocking transactions. The system allows administrators to manage inventory, process transactions, and generate VAT invoices for sales and restocking.

### Features

* **View Available Products**: List all the products with their details such as name, brand, price, and stock.
* **Process Customer Sales**: Apply the "Buy 3, Get 1 Free" policy, update stock, and calculate the total cost of the transaction.
* **Restock Products**: Add new stock to the inventory, update prices and quantities, and generate a restocking invoice.
* **Generate Sales and Restocking Invoices**: Create invoice files for both sales and restocking transactions, including the product details, quantities, prices, and totals.
* **Modular Design**: The program is structured to allow for easy extension and future improvements, such as adding new features or integrating with other systems.
* **User-Friendly Interface**: The application features a simple and intuitive interface, making it easy for administrators to navigate and use the system.
* **Data Security**: The system ensures the security and integrity of data by implementing proper data validation and error handling mechanisms.

---

## Installation

### Prerequisites

* Python 3.8 or higher
* pip 20.0 or higher
* Required dependencies listed in requirements.txt:
  * pandas (optional for structured data handling)

### Steps to Install

1. Clone the repository using the following command:

   ```bash
   git clone https://github.com/darshan-regmi/WeCare_Inventory_System.git
   ```

2. Go to the project directory:

   ```bash
   cd WeCare_Inventory_System
   ```

3. Run the application:

   ```bash
   python main.py
   ```

---

## Usage

### Main Menu

After running the application, you will be presented with a main menu. The options in the main menu are:

* **View Available Products**: Displays the list of all products, their prices (based on a 200% markup), and stock.
* **Process Sale**: Enter customer details and process sales, where the system will apply the “Buy 3, Get 1 Free” offer.
* **Restock Products**: Add more products to the stock and update their details.
* **Generate Invoice**: After processing a sale or restocking, an invoice will be generated in .txt format with all relevant details.
* **Exit**: Close the application when done.

---

## File Structure

```bash
WeCare_Inventory_System/
│
├── data
│   └── products.txt
├── main.py
├── README.md
└── src
   ├── product_manager.py
   ├── restock_manager.py
   └── sale_manager.py
```

---

## Project Context

Built as a coursework project for Fundamentals of Computing, demonstrating modular Python design, file-based data persistence, and terminal UI patterns.

---

## License

MIT
