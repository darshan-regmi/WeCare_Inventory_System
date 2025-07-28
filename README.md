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
	+ pandas (optional for structured data handling)

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

```
WeCare_Inventory_System/
│
├── data/
│   ├── products.txt              # Store product data (name, brand, stock, cost, etc.)
│
├── invoices/                     # Folder for storing generated invoices (sales and restocking)
│
├── main.py                       # Main program file for running the system
├── requirements.txt              # List of dependencies for the project
├── README.md                     # Project documentation
└── LICENSE                       # Project license file
```

---

## Contributing

We welcome contributions to improve the project! To contribute:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name for your changes.
3. Make your changes and commit them with a detailed commit message.
4. Push your changes and open a pull request with a description of the changes.

All contributions must adhere to the code of conduct and project standards.

---

## License

This project is licensed under the MIT License. See LICENSE for more details.

---

## Acknowledgements

* Python: Programming language used for building the application.
* VS Code: Text editor used during development.
* GitHub: Platform for version control and collaboration.

---

## Conclusion

This Beauty and Skin Care Shop Management System simplifies inventory management and transaction processing by automating tasks like stock updates, sales processing, and invoice generation. The program provides an efficient way for the shop to track product sales, manage stock levels, and generate accurate reports for both sales and restocking. It also follows the “Buy 3, Get 1 Free” policy, ensuring that the shop’s marketing offer is applied seamlessly during sales transactions.

By using this application, WeCare can enhance their store management, improve operational efficiency, and provide a better experience for both customers and administrators.

### Key Changes/Improvements:

1. **Features** section describes all core functionalities of the system.
2. **Installation** section includes the steps to clone and run the application.
3. **File Structure** provides a quick view of the organization of files in the project.
4. **Contributing** section gives guidelines on how to contribute.
5. **License** section specifies that the project is under the MIT License.
6. **Conclusion** summarizes the impact of the project and how it benefits the store.

This should give users all the information they need to set up, run, and contribute to your project.
