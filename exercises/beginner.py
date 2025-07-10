"""
Beginner MySQL Exercises
Complete these exercises to practice basic MySQL operations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class BeginnerExercises:
    """Beginner level MySQL exercises."""
    
    def __init__(self):
        self.db = None
    
    def setup(self):
        """Setup database connection."""
        self.db = MySQLConnection()
        self.db.connect()
    
    def cleanup(self):
        """Clean up database connection."""
        if self.db:
            self.db.disconnect()
    
    def exercise_1_basic_select(self):
        """
        Exercise 1: Basic SELECT queries
        
        Tasks:
        1. Select all customers from New York
        2. Select products with price > $100
        3. Count total number of orders
        """
        print("=== Exercise 1: Basic SELECT ===")
        
        # TODO: Write query to select all customers from New York
        print("\n1. Customers from New York:")
        ny_customers_query = """
        -- Write your query here
        SELECT first_name, last_name, email 
        FROM customers 
        WHERE state = 'NY'
        """
        
        try:
            customers = self.db.execute_query(ny_customers_query)
            if customers:
                for customer in customers:
                    print(f"   {customer['first_name']} {customer['last_name']} - {customer['email']}")
            else:
                print("   No customers found or query error")
        except Exception as e:
            print(f"   Error: {e}")
        
        # TODO: Write query to select products with price > $100
        print("\n2. Products with price > $100:")
        expensive_products_query = """
        -- Write your query here
        SELECT product_name, price 
        FROM products 
        WHERE price > 100 
        ORDER BY price DESC
        """
        
        try:
            products = self.db.execute_query(expensive_products_query)
            if products:
                for product in products:
                    print(f"   {product['product_name']}: ${product['price']}")
            else:
                print("   No products found or query error")
        except Exception as e:
            print(f"   Error: {e}")
        
        # TODO: Count total number of orders
        print("\n3. Total number of orders:")
        count_orders_query = """
        -- Write your query here
        SELECT COUNT(*) as total_orders 
        FROM orders
        """
        
        try:
            result = self.db.execute_query(count_orders_query)
            if result:
                print(f"   Total orders: {result[0]['total_orders']}")
            else:
                print("   Query error")
        except Exception as e:
            print(f"   Error: {e}")
    
    def exercise_2_insert_update(self):
        """
        Exercise 2: INSERT and UPDATE operations
        
        Tasks:
        1. Insert a new category
        2. Insert a new product in that category
        3. Update the product price
        """
        print("\n=== Exercise 2: INSERT and UPDATE ===")
        
        # TODO: Insert a new category
        print("\n1. Inserting new category 'Toys':")
        insert_category_query = """
        INSERT INTO categories (category_name, description)
        VALUES (%s, %s)
        """
        
        try:
            rows_affected = self.db.execute_update(
                insert_category_query, 
                ('Toys', 'Toys and games for all ages')
            )
            print(f"   Inserted {rows_affected} category")
        except Exception as e:
            print(f"   Error: {e}")
        
        # TODO: Insert a new product
        print("\n2. Inserting new product:")
        # First get the category_id for 'Toys'
        get_category_query = "SELECT category_id FROM categories WHERE category_name = 'Toys'"
        category_result = self.db.execute_query(get_category_query)
        
        if category_result:
            category_id = category_result[0]['category_id']
            
            insert_product_query = """
            INSERT INTO products (product_name, description, category_id, price, stock_quantity, sku)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            try:
                rows_affected = self.db.execute_update(
                    insert_product_query,
                    ('LEGO Building Set', 'Creative building blocks set', category_id, 49.99, 25, 'TOY-001')
                )
                print(f"   Inserted {rows_affected} product")
            except Exception as e:
                print(f"   Error: {e}")
        
        # TODO: Update product price
        print("\n3. Updating product price:")
        update_price_query = """
        UPDATE products 
        SET price = %s 
        WHERE sku = %s
        """
        
        try:
            rows_affected = self.db.execute_update(update_price_query, (44.99, 'TOY-001'))
            print(f"   Updated {rows_affected} product price")
        except Exception as e:
            print(f"   Error: {e}")
    
    def exercise_3_joins(self):
        """
        Exercise 3: JOIN operations
        
        Tasks:
        1. List all products with their category names
        2. Show customers and their order count
        3. Display order details with customer and product information
        """
        print("\n=== Exercise 3: JOINs ===")
        
        # TODO: Products with category names
        print("\n1. Products with category names:")
        products_categories_query = """
        SELECT p.product_name, c.category_name, p.price
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        ORDER BY c.category_name, p.product_name
        LIMIT 10
        """
        
        try:
            results = self.db.execute_query(products_categories_query)
            if results:
                for row in results:
                    print(f"   {row['product_name']} ({row['category_name']}) - ${row['price']}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # TODO: Customers with order count
        print("\n2. Customers with order count:")
        customers_orders_query = """
        SELECT 
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            COUNT(o.order_id) as order_count,
            COALESCE(SUM(o.total_amount), 0) as total_spent
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        ORDER BY order_count DESC
        """
        
        try:
            results = self.db.execute_query(customers_orders_query)
            if results:
                for row in results:
                    print(f"   {row['customer_name']}: {row['order_count']} orders, ${row['total_spent']:.2f} spent")
        except Exception as e:
            print(f"   Error: {e}")
    
    def exercise_4_aggregation(self):
        """
        Exercise 4: Aggregation and grouping
        
        Tasks:
        1. Calculate average order value by month
        2. Find top 5 best-selling products
        3. Show category sales summary
        """
        print("\n=== Exercise 4: Aggregation ===")
        
        # TODO: Average order value by month
        print("\n1. Average order value by month:")
        monthly_avg_query = """
        SELECT 
            YEAR(order_date) as year,
            MONTH(order_date) as month,
            COUNT(*) as order_count,
            AVG(total_amount) as avg_order_value
        FROM orders
        GROUP BY YEAR(order_date), MONTH(order_date)
        ORDER BY year, month
        """
        
        try:
            results = self.db.execute_query(monthly_avg_query)
            if results:
                for row in results:
                    print(f"   {row['year']}-{row['month']:02d}: {row['order_count']} orders, avg ${row['avg_order_value']:.2f}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # TODO: Top 5 best-selling products
        print("\n2. Top 5 best-selling products:")
        bestsellers_query = """
        SELECT 
            p.product_name,
            SUM(oi.quantity) as total_sold,
            SUM(oi.total_price) as total_revenue
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_sold DESC
        LIMIT 5
        """
        
        try:
            results = self.db.execute_query(bestsellers_query)
            if results:
                for row in results:
                    print(f"   {row['product_name']}: {row['total_sold']} sold, ${row['total_revenue']:.2f} revenue")
        except Exception as e:
            print(f"   Error: {e}")


def main():
    """Run beginner exercises."""
    print("MySQL Beginner Exercises")
    print("=" * 30)
    
    exercises = BeginnerExercises()
    
    try:
        exercises.setup()
        
        exercises.exercise_1_basic_select()
        exercises.exercise_2_insert_update()
        exercises.exercise_3_joins()
        exercises.exercise_4_aggregation()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. MySQL server running")
        print("2. Database and tables created")
        print("3. Sample data loaded")
        print("4. .env file configured")
        
    finally:
        exercises.cleanup()


if __name__ == "__main__":
    main()
