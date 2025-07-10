"""
MySQL Practice Project - Data Generation Utilities
Generate larger datasets for performance testing and advanced scenarios.
"""

import datetime
import os
import random
import sys
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class DataGenerator:
    """Generate sample data for testing and demonstrations."""

    def __init__(self):
        self.db: Optional[MySQLConnection] = None

        # Sample data pools
        self.first_names = [
            "James",
            "Mary",
            "John",
            "Patricia",
            "Robert",
            "Jennifer",
            "Michael",
            "Linda",
            "William",
            "Elizabeth",
            "David",
            "Barbara",
            "Richard",
            "Susan",
            "Joseph",
            "Jessica",
            "Thomas",
            "Sarah",
            "Christopher",
            "Karen",
            "Charles",
            "Nancy",
            "Daniel",
            "Lisa",
            "Matthew",
            "Betty",
            "Anthony",
            "Helen",
            "Mark",
            "Sandra",
            "Donald",
            "Donna",
            "Steven",
            "Carol",
            "Paul",
            "Ruth",
            "Andrew",
            "Sharon",
            "Joshua",
            "Michelle",
        ]

        self.last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
            "Taylor",
            "Moore",
            "Jackson",
            "Martin",
            "Lee",
            "Perez",
            "Thompson",
            "White",
            "Harris",
            "Sanchez",
            "Clark",
            "Ramirez",
            "Lewis",
            "Robinson",
        ]

        self.cities = [
            "New York",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
            "Dallas",
            "San Jose",
            "Austin",
            "Jacksonville",
            "Fort Worth",
            "Columbus",
            "Indianapolis",
            "Charlotte",
            "San Francisco",
            "Seattle",
            "Denver",
            "Washington DC",
            "Boston",
            "El Paso",
            "Nashville",
            "Detroit",
            "Oklahoma City",
            "Portland",
            "Las Vegas",
            "Memphis",
            "Louisville",
            "Baltimore",
            "Milwaukee",
            "Albuquerque",
            "Tucson",
            "Fresno",
            "Sacramento",
        ]

        self.states = [
            "NY",
            "CA",
            "IL",
            "TX",
            "AZ",
            "PA",
            "FL",
            "OH",
            "IN",
            "NC",
            "WA",
            "CO",
            "MA",
            "TN",
            "MI",
            "OK",
            "OR",
            "NV",
            "KY",
            "MD",
            "WI",
            "NM",
            "LA",
            "MN",
        ]

        self.product_adjectives = [
            "Premium",
            "Deluxe",
            "Professional",
            "Advanced",
            "Smart",
            "Ultra",
            "Super",
            "Mega",
            "Pro",
            "Elite",
            "Ultimate",
            "Enhanced",
            "Digital",
            "Wireless",
            "Portable",
            "Compact",
            "Heavy-Duty",
            "Industrial",
            "Commercial",
            "Eco-Friendly",
        ]

        self.product_nouns = [
            "Widget",
            "Device",
            "Tool",
            "Gadget",
            "Accessory",
            "Kit",
            "Set",
            "Pack",
            "System",
            "Solution",
            "Equipment",
            "Apparatus",
            "Instrument",
            "Machine",
            "Component",
            "Module",
            "Unit",
            "Assembly",
            "Hardware",
            "Software",
        ]

    def setup(self) -> bool:
        """Setup database connection."""
        try:
            self.db = MySQLConnection()
            return self.db.connect()
        except Exception as e:
            print(f"Failed to setup database connection: {e}")
            return False

    def cleanup(self):
        """Clean up database connection."""
        if self.db:
            self.db.disconnect()

    def _check_connection(self) -> bool:
        """Check if database connection is available."""
        if not self.db:
            print("Error: No database connection")
            return False
        return True

    def generate_customers(self, count: int = 1000) -> int:
        """Generate random customer data."""
        if not self._check_connection():
            return 0
        assert self.db is not None

        print(f"Generating {count} customers...")

        customers_data = []
        for i in range(count):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@email.com"
            phone = f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
            address = f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar', 'Maple'])} {random.choice(['St', 'Ave', 'Dr', 'Ln', 'Blvd'])}"
            city = random.choice(self.cities)
            state = random.choice(self.states)
            zip_code = f"{random.randint(10000, 99999)}"

            customers_data.append(
                (first_name, last_name, email, phone, address, city, state, zip_code)
            )

        # Batch insert
        insert_query = """
        INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            rows_inserted = self.db.execute_batch_update(insert_query, customers_data)
            print(f"✅ Generated {rows_inserted} customers")
            return rows_inserted
        except Exception as e:
            print(f"❌ Error generating customers: {e}")
            return 0

    def generate_products(self, count: int = 500) -> int:
        """Generate random product data."""
        if not self._check_connection():
            return 0
        assert self.db is not None

        print(f"Generating {count} products...")

        # Get existing categories
        categories = self.db.execute_query(
            "SELECT category_id, category_name FROM categories"
        )
        if not categories:
            print("❌ No categories found. Please create categories first.")
            return 0

        products_data = []
        for i in range(count):
            category = random.choice(categories)
            adjective = random.choice(self.product_adjectives)
            noun = random.choice(self.product_nouns)
            product_name = f"{adjective} {noun}"
            description = f"High-quality {noun.lower()} for {category['category_name'].lower()} applications"
            price = round(random.uniform(9.99, 999.99), 2)
            stock_quantity = random.randint(0, 200)
            sku = (
                f"{category['category_name'][:4].upper()}-{random.randint(1000, 9999)}"
            )

            products_data.append(
                (
                    product_name,
                    description,
                    price,
                    stock_quantity,
                    sku,
                    category["category_id"],
                )
            )

        # Batch insert
        insert_query = """
        INSERT INTO products (product_name, description, price, stock_quantity, sku, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        try:
            rows_inserted = self.db.execute_batch_update(insert_query, products_data)
            print(f"✅ Generated {rows_inserted} products")
            return rows_inserted
        except Exception as e:
            print(f"❌ Error generating products: {e}")
            return 0

    def generate_orders(self, count: int = 2000) -> int:
        """Generate random order data with order items."""
        if not self._check_connection():
            return 0
        assert self.db is not None

        print(f"Generating {count} orders...")

        # Get existing customers and products
        customers = self.db.execute_query("SELECT customer_id FROM customers")
        products = self.db.execute_query(
            "SELECT product_id, price FROM products WHERE stock_quantity > 0"
        )

        if not customers or not products:
            print("❌ No customers or products found. Please generate them first.")
            return 0

        orders_generated = 0

        for i in range(count):
            customer = random.choice(customers)

            # Random order date within last 2 years
            start_date = datetime.datetime.now() - datetime.timedelta(days=730)
            end_date = datetime.datetime.now()
            random_date = start_date + datetime.timedelta(
                seconds=random.randint(0, int((end_date - start_date).total_seconds()))
            )

            status = random.choice(
                ["pending", "processing", "shipped", "delivered", "cancelled"]
            )

            # Create order
            order_query = """
            INSERT INTO orders (customer_id, order_date, status, total_amount)
            VALUES (%s, %s, %s, %s)
            """

            try:
                # Insert order with placeholder total
                order_id = self.db.execute_update_with_id(
                    order_query, (customer["customer_id"], random_date, status, 0.00)
                )

                if not order_id:
                    continue

                # Generate 1-5 order items
                num_items = random.randint(1, 5)
                order_total = 0.00

                for _ in range(num_items):
                    product = random.choice(products)
                    quantity = random.randint(1, 3)
                    unit_price = product["price"]
                    total_price = unit_price * quantity
                    order_total += total_price

                    # Insert order item
                    item_query = """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                    """

                    self.db.execute_update(
                        item_query,
                        (
                            order_id,
                            product["product_id"],
                            quantity,
                            unit_price,
                            total_price,
                        ),
                    )

                # Update order total
                update_query = "UPDATE orders SET total_amount = %s WHERE order_id = %s"
                self.db.execute_update(update_query, (order_total, order_id))

                orders_generated += 1

                if orders_generated % 100 == 0:
                    print(f"  Generated {orders_generated} orders...")

            except Exception as e:
                print(f"  Error generating order {i}: {e}")
                continue

        print(f"✅ Generated {orders_generated} orders with items")
        return orders_generated

    def generate_sample_views(self):
        """Create useful database views for analysis."""
        if not self._check_connection():
            return
        assert self.db is not None

        print("Creating analytical views...")

        views = [
            # Customer summary view
            (
                "customer_summary",
                """
                CREATE OR REPLACE VIEW customer_summary AS
                SELECT 
                    c.customer_id,
                    CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                    c.email,
                    c.city,
                    c.state,
                    COUNT(DISTINCT o.order_id) as total_orders,
                    COALESCE(SUM(o.total_amount), 0) as total_spent,
                    COALESCE(AVG(o.total_amount), 0) as avg_order_value,
                    MAX(o.order_date) as last_order_date,
                    DATEDIFF(CURDATE(), MAX(o.order_date)) as days_since_last_order
                FROM customers c
                LEFT JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state
            """,
            ),
            # Product performance view
            (
                "product_performance",
                """
                CREATE OR REPLACE VIEW product_performance AS
                SELECT 
                    p.product_id,
                    p.product_name,
                    cat.category_name,
                    p.price,
                    p.stock_quantity,
                    COALESCE(SUM(oi.quantity), 0) as total_sold,
                    COALESCE(SUM(oi.total_price), 0) as total_revenue,
                    COALESCE(AVG(oi.unit_price), p.price) as avg_selling_price,
                    COUNT(DISTINCT oi.order_id) as number_of_orders
                FROM products p
                JOIN categories cat ON p.category_id = cat.category_id
                LEFT JOIN order_items oi ON p.product_id = oi.product_id
                GROUP BY p.product_id, p.product_name, cat.category_name, p.price, p.stock_quantity
            """,
            ),
            # Monthly sales summary
            (
                "monthly_sales",
                """
                CREATE OR REPLACE VIEW monthly_sales AS
                SELECT 
                    YEAR(order_date) as year,
                    MONTH(order_date) as month,
                    DATE_FORMAT(order_date, '%Y-%m') as year_month,
                    COUNT(DISTINCT order_id) as total_orders,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value,
                    MIN(total_amount) as min_order_value,
                    MAX(total_amount) as max_order_value
                FROM orders
                GROUP BY YEAR(order_date), MONTH(order_date)
                ORDER BY year, month
            """,
            ),
        ]

        for view_name, view_sql in views:
            try:
                self.db.execute_update(view_sql)
                print(f"  ✅ Created view: {view_name}")
            except Exception as e:
                print(f"  ❌ Error creating view {view_name}: {e}")


def main():
    """Generate sample data for testing."""
    print("🏭 MySQL Data Generator")
    print("=" * 30)

    generator = DataGenerator()

    try:
        if not generator.setup():
            print("❌ Failed to connect to database")
            return

        print("\nChoose data generation options:")
        print("1. Generate customers (1000)")
        print("2. Generate products (500)")
        print("3. Generate orders (2000)")
        print("4. Create analytical views")
        print("5. Generate all data (recommended)")
        print("0. Exit")

        choice = input("\nEnter your choice (0-5): ").strip()

        if choice == "1":
            generator.generate_customers(1000)
        elif choice == "2":
            generator.generate_products(500)
        elif choice == "3":
            generator.generate_orders(2000)
        elif choice == "4":
            generator.generate_sample_views()
        elif choice == "5":
            print("\n🚀 Generating complete dataset...")
            generator.generate_customers(1000)
            generator.generate_products(500)
            generator.generate_orders(2000)
            generator.generate_sample_views()
            print("\n🎉 Data generation complete!")
        elif choice == "0":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        generator.cleanup()


if __name__ == "__main__":
    main()
