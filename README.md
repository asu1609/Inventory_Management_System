**Inventory Management Web Application**

**Overview**

This Flask-based web application is designed to efficiently manage the inventory of products across different locations or warehouses. It provides a user-friendly interface to perform operations related to products, locations, and product movements. The primary goal is to help businesses keep track of their inventory, including product additions, removals, and balance quantities in each location.

**Features**

- Database Tables

  - Product Table
    - Columns:
       - product_id (Primary Key)
  - Location Table
    - Columns:
      - location_id (Primary Key)
  - ProductMovement Table
    - Columns:
      - movement_id (Primary Key)
      - timestamp
      - from_location
      - to_location
      - product_id
      - qty
- Views
  
  - Product Operations
    - Add, edit, and view product details.
  - Location Operations
    - Add, edit, and view location details.
  - Product Movement Operations
    - Add, edit, and view product movement details.
- Reports

  - Balance Quantity Report

    Provides the balance quantity of each product in each location.

    
**Installation**
1. Clone the Repository: git clone https://github.com/asu1609/inventory_management_system.git
2. cd inventory_management_system
3. Create a Virtual Environment (Optional but Recommended)
   
   python -m venv venv
   
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
5. Install Dependencies

   pip install -r requirements.txt
6. Initialize the Database
7. Run the Application

   flask run
8. Access the Application
   
   Open your web browser and go to http://localhost:5000

**Usage**
- Product Operations

  Navigate to the "Product" section to add, edit, or view product details.
- Location Operations

  Navigate to the "Location" section to add, edit, or view location details.
- Product Movement Operations

  Navigate to the "Product Movement" section to add, edit, or view product movement details.
- Balance Quantity Report

  Access the "Reports" section to view the balance quantity report for each product in each location.
