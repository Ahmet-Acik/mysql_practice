"""
Intermediate MySQL Exercises
Practice intermediate level MySQL operations including complex JOINs, subqueries, and data analysis.
"""

import sys
import os
from typing import Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class IntermediateExercises:
    """Intermediate level MySQL exercises."""
    
    def __init__(self):
        self.db: Optional[MySQLConnection] = None
    
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
            print("   Error: No database connection")
            return False
        return True

    def exercise_1_complex_joins(self):
        """
        Exercise 1: Complex JOIN operations
        
        Tasks:
        1. Find customers who haven't placed any orders (LEFT JOIN)
        2. Show products that have never been ordered
        3. Create a sales report with customer, product, and category info
        """
        print("=== Exercise 1: Complex JOINs ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # Task 1: Customers without orders
        print("\n1. Customers who haven't placed orders:")
        no_orders_query = """
        SELECT 
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.email,
            c.city,
            c.state
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.customer_id IS NULL
        ORDER BY c.last_name, c.first_name
        """
        
        try:
            results = self.db.execute_query(no_orders_query)
            if results:
                for row in results:
                    print(f"   {row['customer_name']} ({row['email']}) - {row['city']}, {row['state']}")
            else:
                print("   All customers have placed orders!")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Task 2: Products never ordered
        print("\n2. Products that have never been ordered:")
        no_sales_query = """
        SELECT 
            p.product_id,
            p.product_name,
            c.category_name,
            p.price,
            p.stock_quantity
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        WHERE oi.product_id IS NULL
        ORDER BY c.category_name, p.product_name
        """
        
        try:
            results = self.db.execute_query(no_sales_query)
            if results:
                current_category = ""
                for row in results:
                    if row['category_name'] != current_category:
                        current_category = row['category_name']
                        print(f"\n   {current_category}:")
                    print(f"     {row['product_name']}: ${row['price']:.2f} (Stock: {row['stock_quantity']})")
            else:
                print("   All products have been ordered!")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Task 3: Comprehensive sales report
        print("\n3. Comprehensive sales report:")
        sales_report_query = """
        SELECT 
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            cat.category_name,
            p.product_name,
            oi.quantity,
            oi.unit_price,
            oi.total_price,
            o.order_date,
            o.status
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN categories cat ON p.category_id = cat.category_id
        ORDER BY o.order_date DESC, oi.total_price DESC
        LIMIT 10
        """
        
        try:
            results = self.db.execute_query(sales_report_query)
            if results:
                for row in results:
                    print(f"   {row['customer_name']} bought {row['quantity']}x {row['product_name']}")
                    print(f"     Category: {row['category_name']}, Total: ${row['total_price']:.2f}")
                    print(f"     Date: {row['order_date']}, Status: {row['status']}")
                    print()
        except Exception as e:
            print(f"   Error: {e}")

    def exercise_2_subqueries_cte(self):
        """
        Exercise 2: Subqueries and Common Table Expressions
        
        Tasks:
        1. Find customers who spent more than the average customer
        2. Get products with prices higher than the category average
        3. Use a CTE to calculate running totals
        """
        print("\n=== Exercise 2: Subqueries and CTEs ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # Task 1: High-spending customers
        print("\n1. Customers who spent more than average:")
        high_spenders_query = """
        SELECT 
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.email,
            SUM(o.total_amount) as total_spent,
            COUNT(o.order_id) as order_count,
            ROUND(SUM(o.total_amount) / COUNT(o.order_id), 2) as avg_order_value
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        HAVING SUM(o.total_amount) > (
            SELECT AVG(customer_total)
            FROM (
                SELECT SUM(o2.total_amount) as customer_total
                FROM orders o2
                GROUP BY o2.customer_id
            ) as customer_totals
        )
        ORDER BY total_spent DESC
        """
        
        try:
            results = self.db.execute_query(high_spenders_query)
            if results:
                for row in results:
                    print(f"   {row['customer_name']} ({row['email']})")
                    print(f"     Total Spent: ${row['total_spent']:.2f}")
                    print(f"     Orders: {row['order_count']}, Avg: ${row['avg_order_value']:.2f}")
                    print()
        except Exception as e:
            print(f"   Error: {e}")
        
        # Task 2: Products above category average
        print("\n2. Products priced above their category average:")
        above_avg_query = """
        SELECT 
            p.product_name,
            c.category_name,
            p.price as product_price,
            ROUND((
                SELECT AVG(p2.price)
                FROM products p2
                WHERE p2.category_id = p.category_id
            ), 2) as category_avg,
            ROUND(p.price - (
                SELECT AVG(p2.price)
                FROM products p2
                WHERE p2.category_id = p.category_id
            ), 2) as price_difference
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.price > (
            SELECT AVG(p2.price)
            FROM products p2
            WHERE p2.category_id = p.category_id
        )
        ORDER BY price_difference DESC
        """
        
        try:
            results = self.db.execute_query(above_avg_query)
            if results:
                for row in results:
                    print(f"   {row['product_name']} ({row['category_name']})")
                    print(f"     Price: ${row['product_price']:.2f} vs Avg: ${row['category_avg']:.2f}")
                    print(f"     Difference: +${row['price_difference']:.2f}")
                    print()
        except Exception as e:
            print(f"   Error: {e}")
        
        # Task 3: CTE for running totals (if supported)
        print("\n3. Running sales totals by date:")
        # Note: MySQL 8.0+ supports CTEs, earlier versions don't
        cte_query = """
        WITH daily_sales AS (
            SELECT 
                DATE(order_date) as sale_date,
                SUM(total_amount) as daily_total
            FROM orders
            GROUP BY DATE(order_date)
        ),
        running_totals AS (
            SELECT 
                sale_date,
                daily_total,
                SUM(daily_total) OVER (ORDER BY sale_date) as running_total
            FROM daily_sales
        )
        SELECT 
            sale_date,
            daily_total,
            running_total,
            ROUND((running_total / (SELECT SUM(daily_total) FROM daily_sales)) * 100, 2) as percent_of_total
        FROM running_totals
        ORDER BY sale_date
        """
        
        try:
            results = self.db.execute_query(cte_query)
            if results:
                for row in results:
                    print(f"   {row['sale_date']}: ${row['daily_total']:.2f}")
                    print(f"     Running Total: ${row['running_total']:.2f} ({row['percent_of_total']:.1f}%)")
        except Exception as e:
            print(f"   Error (CTEs may not be supported in older MySQL): {e}")
            # Fallback without CTE
            fallback_query = """
            SELECT 
                DATE(order_date) as sale_date,
                SUM(total_amount) as daily_total
            FROM orders
            GROUP BY DATE(order_date)
            ORDER BY sale_date
            """
            try:
                results = self.db.execute_query(fallback_query)
                if results:
                    running_total = 0
                    for row in results:
                        running_total += float(row['daily_total'])
                        print(f"   {row['sale_date']}: ${row['daily_total']:.2f}")
                        print(f"     Running Total: ${running_total:.2f}")
            except Exception as e2:
                print(f"   Fallback Error: {e2}")

    def exercise_3_data_analysis(self):
        """
        Exercise 3: Data Analysis and Reporting
        
        Tasks:
        1. Customer segmentation based on spending
        2. Product performance metrics
        3. Seasonal analysis (if applicable)
        """
        print("\n=== Exercise 3: Data Analysis ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # Task 1: Customer segmentation
        print("\n1. Customer segmentation by spending:")
        segmentation_query = """
        SELECT 
            customer_segment,
            COUNT(*) as customer_count,
            AVG(total_spent) as avg_spent,
            MIN(total_spent) as min_spent,
            MAX(total_spent) as max_spent
        FROM (
            SELECT 
                c.customer_id,
                CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                COALESCE(SUM(o.total_amount), 0) as total_spent,
                CASE 
                    WHEN COALESCE(SUM(o.total_amount), 0) = 0 THEN 'No Purchase'
                    WHEN COALESCE(SUM(o.total_amount), 0) < 100 THEN 'Low Value'
                    WHEN COALESCE(SUM(o.total_amount), 0) < 500 THEN 'Medium Value'
                    WHEN COALESCE(SUM(o.total_amount), 0) < 1000 THEN 'High Value'
                    ELSE 'Premium'
                END as customer_segment
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name
        ) as segmented_customers
        GROUP BY customer_segment
        ORDER BY avg_spent DESC
        """
        
        try:
            results = self.db.execute_query(segmentation_query)
            if results:
                print("   Segment      | Count | Avg Spent | Min Spent | Max Spent")
                print("   -------------|-------|-----------|-----------|----------")
                for row in results:
                    print(f"   {row['customer_segment']:12} | {row['customer_count']:5d} | ${row['avg_spent']:8.2f} | ${row['min_spent']:8.2f} | ${row['max_spent']:8.2f}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Task 2: Product performance metrics
        print("\n2. Product performance analysis:")
        performance_query = """
        SELECT 
            cat.category_name,
            COUNT(p.product_id) as total_products,
            COUNT(DISTINCT oi.product_id) as products_sold,
            ROUND(COUNT(DISTINCT oi.product_id) * 100.0 / COUNT(p.product_id), 2) as sell_through_rate,
            COALESCE(SUM(oi.quantity), 0) as total_units_sold,
            COALESCE(SUM(oi.total_price), 0) as total_revenue,
            COALESCE(AVG(oi.unit_price), 0) as avg_selling_price,
            AVG(p.price) as avg_list_price
        FROM categories cat
        LEFT JOIN products p ON cat.category_id = p.category_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY cat.category_id, cat.category_name
        ORDER BY total_revenue DESC
        """
        
        try:
            results = self.db.execute_query(performance_query)
            if results:
                for row in results:
                    print(f"   {row['category_name']}:")
                    print(f"     Products: {row['total_products']} total, {row['products_sold']} sold ({row['sell_through_rate']:.1f}%)")
                    print(f"     Units Sold: {row['total_units_sold']}, Revenue: ${row['total_revenue']:.2f}")
                    print(f"     Avg Selling Price: ${row['avg_selling_price']:.2f} vs List: ${row['avg_list_price']:.2f}")
                    print()
        except Exception as e:
            print(f"   Error: {e}")
        
        # Task 3: Order pattern analysis
        print("\n3. Order pattern analysis:")
        pattern_query = """
        SELECT 
            DAYNAME(order_date) as day_of_week,
            HOUR(order_date) as hour_of_day,
            COUNT(*) as order_count,
            AVG(total_amount) as avg_order_value,
            SUM(total_amount) as total_revenue
        FROM orders
        GROUP BY DAYNAME(order_date), HOUR(order_date)
        ORDER BY order_count DESC
        LIMIT 10
        """
        
        try:
            results = self.db.execute_query(pattern_query)
            if results:
                print("   Top Order Times:")
                for row in results:
                    print(f"   {row['day_of_week']} {row['hour_of_day']:02d}:00 - {row['order_count']} orders")
                    print(f"     Avg: ${row['avg_order_value']:.2f}, Total: ${row['total_revenue']:.2f}")
                    print()
        except Exception as e:
            print(f"   Error: {e}")

    def exercise_4_indexes_performance(self):
        """
        Exercise 4: Database Performance and Indexes
        
        Tasks:
        1. Analyze query performance with EXPLAIN
        2. Identify missing indexes
        3. Create performance improvement suggestions
        """
        print("\n=== Exercise 4: Performance Analysis ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # Task 1: Query performance analysis
        print("\n1. Query performance analysis:")
        
        # Check for slow queries (simulated)
        slow_query = """
        SELECT 
            c.first_name,
            c.last_name,
            p.product_name,
            o.order_date
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE c.email LIKE '%@email.com'
        AND p.price > 100
        ORDER BY o.order_date DESC
        """
        
        try:
            # Show explain plan
            explain_query = f"EXPLAIN {slow_query}"
            explain_results = self.db.execute_query(explain_query)
            if explain_results:
                print("   EXPLAIN output for complex query:")
                for row in explain_results:
                    print(f"   Table: {row.get('table', 'N/A')}, Type: {row.get('type', 'N/A')}, Rows: {row.get('rows', 'N/A')}")
        except Exception as e:
            print(f"   Error analyzing query: {e}")
        
        # Task 2: Index analysis
        print("\n2. Current indexes analysis:")
        index_query = """
        SELECT 
            TABLE_NAME,
            INDEX_NAME,
            COLUMN_NAME,
            NON_UNIQUE
        FROM INFORMATION_SCHEMA.STATISTICS 
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME IN ('customers', 'orders', 'products', 'order_items', 'categories')
        ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX
        """
        
        try:
            results = self.db.execute_query(index_query)
            if results:
                current_table = ""
                current_index = ""
                for row in results:
                    if row['TABLE_NAME'] != current_table:
                        current_table = row['TABLE_NAME']
                        print(f"\n   {current_table}:")
                    
                    if row['INDEX_NAME'] != current_index:
                        current_index = row['INDEX_NAME']
                        unique_text = "UNIQUE" if row['NON_UNIQUE'] == 0 else "NON-UNIQUE"
                        print(f"     {row['INDEX_NAME']} ({unique_text}): {row['COLUMN_NAME']}", end="")
                    else:
                        print(f", {row['COLUMN_NAME']}", end="")
                print()  # Final newline
        except Exception as e:
            print(f"   Error: {e}")
        
        # Task 3: Performance recommendations
        print("\n3. Performance improvement suggestions:")
        suggestions = [
            "Consider adding indexes on frequently queried columns:",
            "  - customers(email) for email lookups",
            "  - orders(order_date) for date range queries", 
            "  - products(price) for price range queries",
            "  - order_items(product_id, order_id) composite index",
            "",
            "Query optimization tips:",
            "  - Use LIMIT for large result sets",
            "  - Avoid SELECT * in production queries",
            "  - Use proper WHERE clauses to filter early",
            "  - Consider partitioning large tables by date"
        ]
        
        for suggestion in suggestions:
            print(f"   {suggestion}")


def main():
    """Run intermediate exercises."""
    print("MySQL Intermediate Exercises")
    print("=" * 35)
    
    exercises = IntermediateExercises()
    
    try:
        if not exercises.setup():
            print("Failed to connect to database. Please check your configuration.")
            return
        
        exercises.exercise_1_complex_joins()
        exercises.exercise_2_subqueries_cte()
        exercises.exercise_3_data_analysis()
        exercises.exercise_4_indexes_performance()
        
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
