"""
Basic MySQL operations examples.
This module demonstrates basic CRUD operations using Python and MySQL.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


def create_operations():
    """Demonstrate CREATE (INSERT) operations."""
    print("=== CREATE Operations ===")
    
    with MySQLConnection() as db:
        # Insert a new customer
        insert_customer_query = """
        INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        customer_data = (
            'Alice', 'Cooper', 'alice.cooper@email.com', '555-0109',
            '999 Rock St', 'Detroit', 'MI', '48201'
        )
        
        rows_affected = db.execute_update(insert_customer_query, customer_data)
        print(f"Inserted {rows_affected} customer(s)")
        
        # Insert multiple products
        insert_product_query = """
        INSERT INTO products (product_name, description, category_id, price, stock_quantity, sku)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        products_data = [
            ('Gaming Mouse', 'High-precision gaming mouse', 1, 79.99, 50, 'ELEC-006'),
            ('Mechanical Keyboard', 'RGB mechanical keyboard', 1, 149.99, 30, 'ELEC-007'),
            ('Hoodie', 'Comfortable cotton hoodie', 2, 49.99, 100, 'CLOTH-006')
        ]
        
        rows_affected = db.execute_many(insert_product_query, products_data)
        print(f"Inserted {rows_affected} product(s)")


def read_operations():
    """Demonstrate READ (SELECT) operations."""
    print("\n=== READ Operations ===")
    
    with MySQLConnection() as db:
        # Simple SELECT
        print("1. All categories:")
        categories = db.execute_query("SELECT * FROM categories")
        if categories:
            for category in categories:
                print(f"   {category['category_id']}: {category['category_name']}")
        else:
            print("   No categories found or connection error")
        
        # SELECT with WHERE clause
        print("\n2. Electronics products:")
        electronics_query = """
        SELECT p.product_name, p.price, p.stock_quantity
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE c.category_name = %s
        ORDER BY p.price DESC
        """
        
        electronics = db.execute_query(electronics_query, ('Electronics',))
        if electronics:
            for product in electronics:
                print(f"   {product['product_name']}: ${product['price']} (Stock: {product['stock_quantity']})")
        else:
            print("   No electronics products found or connection error")
        
        # SELECT with aggregation
        print("\n3. Order statistics:")
        stats_query = """
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value,
            MIN(total_amount) as min_order,
            MAX(total_amount) as max_order
        FROM orders
        """
        
        stats = db.execute_query(stats_query)
        if stats:
            stat = stats[0]
            print(f"   Total Orders: {stat['total_orders']}")
            print(f"   Total Revenue: ${stat['total_revenue']:.2f}")
            print(f"   Average Order Value: ${stat['avg_order_value']:.2f}")
            print(f"   Min Order: ${stat['min_order']:.2f}")
            print(f"   Max Order: ${stat['max_order']:.2f}")


def update_operations():
    """Demonstrate UPDATE operations."""
    print("\n=== UPDATE Operations ===")
    
    with MySQLConnection() as db:
        # Update single record
        print("1. Updating product price:")
        
        # First, show current price
        current_price_query = "SELECT product_name, price FROM products WHERE sku = %s"
        result = db.execute_query(current_price_query, ('ELEC-001',))
        if result:
            print(f"   Current price of {result[0]['product_name']}: ${result[0]['price']}")
        
        # Update price
        update_price_query = "UPDATE products SET price = %s WHERE sku = %s"
        rows_affected = db.execute_update(update_price_query, (749.99, 'ELEC-001'))
        print(f"   Updated {rows_affected} product(s)")
        
        # Show new price
        result = db.execute_query(current_price_query, ('ELEC-001',))
        if result:
            print(f"   New price of {result[0]['product_name']}: ${result[0]['price']}")
        
        # Update multiple records
        print("\n2. Updating stock quantities:")
        update_stock_query = """
        UPDATE products 
        SET stock_quantity = stock_quantity + %s 
        WHERE category_id = (SELECT category_id FROM categories WHERE category_name = %s)
        """
        
        rows_affected = db.execute_update(update_stock_query, (10, 'Electronics'))
        print(f"   Updated stock for {rows_affected} electronics product(s)")


def delete_operations():
    """Demonstrate DELETE operations."""
    print("\n=== DELETE Operations ===")
    
    with MySQLConnection() as db:
        # First, create a test record to delete
        insert_test_query = """
        INSERT INTO customers (first_name, last_name, email, phone)
        VALUES (%s, %s, %s, %s)
        """
        
        db.execute_update(insert_test_query, ('Test', 'User', 'test@delete.com', '000-0000'))
        print("Created test customer")
        
        # Delete the test record
        delete_query = "DELETE FROM customers WHERE email = %s"
        rows_affected = db.execute_update(delete_query, ('test@delete.com',))
        print(f"Deleted {rows_affected} test customer(s)")
        
        # Delete with condition
        print("\nDeleting out-of-stock products:")
        delete_stock_query = "DELETE FROM products WHERE stock_quantity = 0"
        rows_affected = db.execute_update(delete_stock_query)
        print(f"Deleted {rows_affected} out-of-stock product(s)")


def advanced_queries():
    """Demonstrate more advanced queries."""
    print("\n=== Advanced Queries ===")
    
    with MySQLConnection() as db:
        # JOIN query
        print("1. Customer orders with details:")
        join_query = """
        SELECT 
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            o.order_id,
            o.order_date,
            o.status,
            o.total_amount
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        ORDER BY o.order_date DESC
        LIMIT 5
        """
        
        orders = db.execute_query(join_query)
        if orders:
            for order in orders:
                print(f"   {order['customer_name']}: Order #{order['order_id']} - ${order['total_amount']} ({order['status']})")
        else:
            print("   No orders found or connection error")
        
        # Subquery
        print("\n2. Customers with orders above average:")
        subquery = """
        SELECT 
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            o.total_amount
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.total_amount > (SELECT AVG(total_amount) FROM orders)
        ORDER BY o.total_amount DESC
        """
        
        high_value_customers = db.execute_query(subquery)
        if high_value_customers:
            for customer in high_value_customers:
                print(f"   {customer['customer_name']}: ${customer['total_amount']}")
        else:
            print("   No high-value customers found or connection error")
        
        # Group by with having
        print("\n3. Product categories with total revenue:")
        group_query = """
        SELECT 
            c.category_name,
            COUNT(oi.order_item_id) as items_sold,
            SUM(oi.total_price) as category_revenue
        FROM categories c
        JOIN products p ON c.category_id = p.category_id
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY c.category_id, c.category_name
        HAVING category_revenue > 100
        ORDER BY category_revenue DESC
        """
        
        category_revenue = db.execute_query(group_query)
        if category_revenue:
            for category in category_revenue:
                print(f"   {category['category_name']}: {category['items_sold']} items, ${category['category_revenue']:.2f}")
        else:
            print("   No category revenue data found or connection error")


def main():
    """Main function to run all examples."""
    print("MySQL Basic Operations Examples")
    print("=" * 40)
    
    try:
        create_operations()
        read_operations()
        update_operations()
        delete_operations()
        advanced_queries()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. MySQL server running")
        print("2. Database 'practice_db' created")
        print("3. Tables created using schemas/create_tables.sql")
        print("4. Sample data inserted using schemas/sample_data.sql")
        print("5. Environment variables set in .env file")


if __name__ == "__main__":
    main()
