"""
Advanced MySQL queries examples.
This module demonstrates complex queries, joins, subqueries, and analytical functions.
"""

import sys
import os
from typing import Optional, List, Dict, Any
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class AdvancedQueries:
    """Advanced MySQL queries demonstrations."""
    
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

    def complex_joins_demo(self):
        """Demonstrate complex JOIN operations."""
        print("=== Complex JOINs ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # Multi-table JOIN with aggregation
        print("\n1. Customer order summary with product details:")
        complex_join_query = """
        SELECT 
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.email,
            COUNT(DISTINCT o.order_id) as total_orders,
            COUNT(oi.order_item_id) as total_items,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.total_price) as total_spent,
            AVG(o.total_amount) as avg_order_value,
            MAX(o.order_date) as last_order_date,
            GROUP_CONCAT(DISTINCT cat.category_name ORDER BY cat.category_name) as categories_purchased
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        LEFT JOIN products p ON oi.product_id = p.product_id
        LEFT JOIN categories cat ON p.category_id = cat.category_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        HAVING total_orders > 0
        ORDER BY total_spent DESC
        """
        
        try:
            results = self.db.execute_query(complex_join_query)
            if results:
                for row in results:
                    print(f"   {row['customer_name']} ({row['email']}):")
                    print(f"     Orders: {row['total_orders']}, Items: {row['total_items']}")
                    print(f"     Total Spent: ${row['total_spent']:.2f}, Avg Order: ${row['avg_order_value']:.2f}")
                    print(f"     Categories: {row['categories_purchased']}")
                    print(f"     Last Order: {row['last_order_date']}")
                    print()
        except Exception as e:
            print(f"   Error: {e}")

    def subqueries_demo(self):
        """Demonstrate subquery techniques."""
        print("\n=== Subqueries ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # Correlated subquery
        print("\n1. Products with above-average category prices:")
        correlated_subquery = """
        SELECT 
            p1.product_name,
            c.category_name,
            p1.price,
            (SELECT AVG(p2.price) 
             FROM products p2 
             WHERE p2.category_id = p1.category_id) as category_avg_price,
            ROUND(p1.price - (SELECT AVG(p2.price) 
                             FROM products p2 
                             WHERE p2.category_id = p1.category_id), 2) as price_difference
        FROM products p1
        JOIN categories c ON p1.category_id = c.category_id
        WHERE p1.price > (SELECT AVG(p2.price) 
                         FROM products p2 
                         WHERE p2.category_id = p1.category_id)
        ORDER BY price_difference DESC
        """
        
        try:
            results = self.db.execute_query(correlated_subquery)
            if results:
                for row in results:
                    print(f"   {row['product_name']} ({row['category_name']})")
                    print(f"     Price: ${row['price']:.2f} vs Category Avg: ${row['category_avg_price']:.2f}")
                    print(f"     Difference: +${row['price_difference']:.2f}")
                    print()
        except Exception as e:
            print(f"   Error: {e}")
        
        # EXISTS subquery
        print("\n2. Customers who have ordered from multiple categories:")
        exists_subquery = """
        SELECT 
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.email,
            COUNT(DISTINCT cat.category_id) as categories_count,
            GROUP_CONCAT(DISTINCT cat.category_name ORDER BY cat.category_name) as categories
        FROM customers c
        WHERE EXISTS (
            SELECT 1 
            FROM orders o 
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.customer_id = c.customer_id
        )
        AND (
            SELECT COUNT(DISTINCT p.category_id)
            FROM orders o2
            JOIN order_items oi2 ON o2.order_id = oi2.order_id
            JOIN products p ON oi2.product_id = p.product_id
            WHERE o2.customer_id = c.customer_id
        ) > 1
        JOIN orders o3 ON c.customer_id = o3.customer_id
        JOIN order_items oi3 ON o3.order_id = oi3.order_id
        JOIN products p2 ON oi3.product_id = p2.product_id
        JOIN categories cat ON p2.category_id = cat.category_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        ORDER BY categories_count DESC
        """
        
        try:
            results = self.db.execute_query(exists_subquery)
            if results:
                for row in results:
                    print(f"   {row['customer_name']} ({row['email']})")
                    print(f"     Categories: {row['categories_count']} - {row['categories']}")
                    print()
            else:
                print("   No customers found with multi-category orders")
        except Exception as e:
            print(f"   Error: {e}")

    def window_functions_demo(self):
        """Demonstrate window functions (if supported by MySQL version)."""
        print("\n=== Window Functions ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # ROW_NUMBER and RANK
        print("\n1. Product ranking by price within categories:")
        window_query = """
        SELECT 
            category_name,
            product_name,
            price,
            ROW_NUMBER() OVER (PARTITION BY c.category_id ORDER BY p.price DESC) as price_rank,
            RANK() OVER (PARTITION BY c.category_id ORDER BY p.price DESC) as price_rank_with_ties,
            ROUND(AVG(p.price) OVER (PARTITION BY c.category_id), 2) as category_avg_price,
            ROUND(price - AVG(p.price) OVER (PARTITION BY c.category_id), 2) as price_vs_avg
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        ORDER BY c.category_name, price_rank
        """
        
        try:
            results = self.db.execute_query(window_query)
            if results:
                current_category = ""
                for row in results:
                    if row['category_name'] != current_category:
                        current_category = row['category_name']
                        print(f"\n   {current_category}:")
                    
                    print(f"     #{row['price_rank']} {row['product_name']}: ${row['price']:.2f}")
                    print(f"         vs avg ${row['category_avg_price']:.2f} ({row['price_vs_avg']:+.2f})")
        except Exception as e:
            print(f"   Error (Window functions may not be supported): {e}")
        
        # Running totals
        print("\n2. Running total of orders by date:")
        running_total_query = """
        SELECT 
            order_date,
            order_id,
            total_amount,
            SUM(total_amount) OVER (ORDER BY order_date, order_id) as running_total,
            AVG(total_amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg_3
        FROM orders
        ORDER BY order_date, order_id
        """
        
        try:
            results = self.db.execute_query(running_total_query)
            if results:
                for row in results:
                    print(f"   {row['order_date']} Order #{row['order_id']}: ${row['total_amount']:.2f}")
                    print(f"     Running Total: ${row['running_total']:.2f}, 3-Order Avg: ${row['moving_avg_3']:.2f}")
        except Exception as e:
            print(f"   Error (Window functions may not be supported): {e}")

    def analytical_queries_demo(self):
        """Demonstrate analytical and reporting queries."""
        print("\n=== Analytical Queries ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # Cohort analysis
        print("\n1. Monthly cohort analysis:")
        cohort_query = """
        SELECT 
            DATE_FORMAT(order_date, '%Y-%m') as order_month,
            COUNT(DISTINCT customer_id) as new_customers,
            COUNT(order_id) as total_orders,
            SUM(total_amount) as monthly_revenue,
            AVG(total_amount) as avg_order_value,
            MIN(total_amount) as min_order,
            MAX(total_amount) as max_order
        FROM orders
        GROUP BY DATE_FORMAT(order_date, '%Y-%m')
        ORDER BY order_month
        """
        
        try:
            results = self.db.execute_query(cohort_query)
            if results:
                print("   Month    | Customers | Orders | Revenue  | Avg Order | Min   | Max")
                print("   ---------|-----------|--------|----------|-----------|-------|-------")
                for row in results:
                    print(f"   {row['order_month']}  |    {row['new_customers']:2d}     |   {row['total_orders']:2d}   | ${row['monthly_revenue']:6.2f} | ${row['avg_order_value']:7.2f} | ${row['min_order']:5.2f} | ${row['max_order']:6.2f}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Product performance analysis
        print("\n2. Product performance analysis:")
        performance_query = """
        SELECT 
            p.product_name,
            c.category_name,
            p.price,
            p.stock_quantity,
            COALESCE(SUM(oi.quantity), 0) as total_sold,
            COALESCE(SUM(oi.total_price), 0) as total_revenue,
            CASE 
                WHEN SUM(oi.quantity) IS NULL THEN 'No Sales'
                WHEN SUM(oi.quantity) >= 10 THEN 'Best Seller'
                WHEN SUM(oi.quantity) >= 5 THEN 'Good Seller'
                WHEN SUM(oi.quantity) >= 1 THEN 'Low Seller'
                ELSE 'No Sales'
            END as performance_category,
            ROUND(COALESCE(SUM(oi.total_price), 0) / NULLIF(SUM(oi.quantity), 0), 2) as avg_selling_price
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, c.category_name, p.price, p.stock_quantity
        ORDER BY total_revenue DESC, total_sold DESC
        """
        
        try:
            results = self.db.execute_query(performance_query)
            if results:
                for row in results:
                    print(f"   {row['product_name']} ({row['category_name']})")
                    print(f"     Price: ${row['price']:.2f}, Stock: {row['stock_quantity']}")
                    print(f"     Sold: {row['total_sold']}, Revenue: ${row['total_revenue']:.2f}")
                    print(f"     Category: {row['performance_category']}")
                    if row['avg_selling_price']:
                        print(f"     Avg Selling Price: ${row['avg_selling_price']:.2f}")
                    print()
        except Exception as e:
            print(f"   Error: {e}")

    def pivot_like_queries_demo(self):
        """Demonstrate pivot-like operations using conditional aggregation."""
        print("\n=== Pivot-like Queries ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # Category sales by month (pivot-like)
        print("\n1. Category sales by month:")
        pivot_query = """
        SELECT 
            DATE_FORMAT(o.order_date, '%Y-%m') as month,
            SUM(CASE WHEN c.category_name = 'Electronics' THEN oi.total_price ELSE 0 END) as Electronics,
            SUM(CASE WHEN c.category_name = 'Clothing' THEN oi.total_price ELSE 0 END) as Clothing,
            SUM(CASE WHEN c.category_name = 'Books' THEN oi.total_price ELSE 0 END) as Books,
            SUM(CASE WHEN c.category_name = 'Sports' THEN oi.total_price ELSE 0 END) as Sports,
            SUM(CASE WHEN c.category_name = 'Home & Garden' THEN oi.total_price ELSE 0 END) as Home_Garden,
            SUM(oi.total_price) as Total
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
        ORDER BY month
        """
        
        try:
            results = self.db.execute_query(pivot_query)
            if results:
                print("   Month   | Electronics | Clothing | Books   | Sports  | Home&Garden | Total")
                print("   --------|-------------|----------|---------|---------|-------------|--------")
                for row in results:
                    print(f"   {row['month']} | ${row['Electronics']:9.2f} | ${row['Clothing']:6.2f} | ${row['Books']:5.2f} | ${row['Sports']:5.2f} | ${row['Home_Garden']:9.2f} | ${row['Total']:6.2f}")
        except Exception as e:
            print(f"   Error: {e}")


def main():
    """Run advanced queries demonstrations."""
    print("MySQL Advanced Queries Examples")
    print("=" * 40)
    
    queries = AdvancedQueries()
    
    try:
        if not queries.setup():
            print("Failed to connect to database. Please check your configuration.")
            return
        
        queries.complex_joins_demo()
        queries.subqueries_demo()
        queries.window_functions_demo()
        queries.analytical_queries_demo()
        queries.pivot_like_queries_demo()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. MySQL server running")
        print("2. Database and tables created")
        print("3. Sample data loaded")
        print("4. .env file configured")
        
    finally:
        queries.cleanup()


if __name__ == "__main__":
    main()
