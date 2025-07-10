"""
Advanced MySQL Exercises
Challenge exercises for advanced MySQL concepts including optimization, 
complex analytics, and database design.
"""

import sys
import os
from typing import Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class AdvancedExercises:
    """Advanced level MySQL exercises."""
    
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

    def exercise_1_query_optimization(self):
        """
        Exercise 1: Query Optimization Challenge
        
        Tasks:
        1. Identify slow queries using EXPLAIN
        2. Create optimal indexes
        3. Rewrite queries for better performance
        """
        print("=== Exercise 1: Query Optimization ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Analyzing query performance with EXPLAIN:")
        
        # Slow query example
        slow_query = """
        SELECT 
            c.first_name,
            c.last_name,
            c.email,
            COUNT(o.order_id) as order_count,
            SUM(o.total_amount) as total_spent,
            MAX(o.order_date) as last_order
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE c.email LIKE '%@email.com'
        AND c.city IN ('New York', 'Los Angeles', 'Chicago')
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        HAVING total_spent > 100
        ORDER BY total_spent DESC
        """
        
        try:
            print("   Original query performance:")
            explain_query = f"EXPLAIN FORMAT=JSON {slow_query}"
            explain_result = self.db.execute_query(explain_query)
            
            if explain_result:
                # Simplified explain output
                print("   ✓ Query analyzed (use EXPLAIN for detailed analysis)")
            
            # Execute the query
            results = self.db.execute_query(slow_query)
            if results:
                print(f"   Query returned {len(results)} rows")
                for row in results[:3]:  # Show first 3
                    print(f"   - {row['first_name']} {row['last_name']}: ${row['total_spent']:.2f}")
            
        except Exception as e:
            print(f"   Error analyzing query: {e}")
        
        print("\n2. Optimization suggestions:")
        optimizations = [
            "CREATE INDEX idx_customers_email_city ON customers(email, city)",
            "CREATE INDEX idx_orders_customer_amount ON orders(customer_id, total_amount)",
            "Consider partitioning orders table by date",
            "Use covering indexes for frequently accessed columns"
        ]
        
        for opt in optimizations:
            print(f"   - {opt}")

    def exercise_2_complex_analytics(self):
        """
        Exercise 2: Complex Analytics Challenge
        
        Tasks:
        1. Customer lifetime value calculation
        2. Cohort analysis
        3. Product recommendation engine
        """
        print("\n=== Exercise 2: Complex Analytics ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Customer Lifetime Value (CLV) Analysis:")
        
        clv_query = """
        SELECT 
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) as customer_name,
            c.email,
            COUNT(DISTINCT o.order_id) as total_orders,
            DATEDIFF(MAX(o.order_date), MIN(o.order_date)) + 1 as customer_lifespan_days,
            SUM(o.total_amount) as total_revenue,
            AVG(o.total_amount) as avg_order_value,
            SUM(o.total_amount) / NULLIF(COUNT(DISTINCT o.order_id), 0) as revenue_per_order,
            CASE 
                WHEN DATEDIFF(MAX(o.order_date), MIN(o.order_date)) = 0 THEN SUM(o.total_amount)
                ELSE SUM(o.total_amount) / (DATEDIFF(MAX(o.order_date), MIN(o.order_date)) + 1) * 365
            END as estimated_annual_value,
            CASE
                WHEN SUM(o.total_amount) >= 1000 THEN 'High Value'
                WHEN SUM(o.total_amount) >= 500 THEN 'Medium Value'  
                WHEN SUM(o.total_amount) >= 100 THEN 'Low Value'
                ELSE 'New Customer'
            END as customer_segment
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.order_id IS NOT NULL
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        ORDER BY total_revenue DESC
        """
        
        try:
            results = self.db.execute_query(clv_query)
            if results:
                print("   Customer Lifetime Value Analysis:")
                print("   Name                 | Segment      | Orders | Revenue  | Est. Annual")
                print("   ---------------------|--------------|--------|----------|------------")
                
                for row in results:
                    name = row['customer_name'][:20].ljust(20)
                    segment = row['customer_segment'][:12].ljust(12)
                    orders = str(row['total_orders']).rjust(6)
                    revenue = f"${row['total_revenue']:.2f}".rjust(8)
                    annual = f"${row['estimated_annual_value']:.2f}".rjust(10)
                    
                    print(f"   {name} | {segment} | {orders} | {revenue} | {annual}")
        except Exception as e:
            print(f"   Error: {e}")
        
        print("\n2. Product Affinity Analysis:")
        
        affinity_query = """
        SELECT 
            p1.product_name as product_a,
            p2.product_name as product_b,
            COUNT(*) as times_bought_together,
            ROUND(COUNT(*) * 100.0 / (
                SELECT COUNT(DISTINCT oi1.order_id) 
                FROM order_items oi1 
                WHERE oi1.product_id = p1.product_id
            ), 2) as affinity_percentage
        FROM order_items oi1
        JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
        JOIN products p1 ON oi1.product_id = p1.product_id
        JOIN products p2 ON oi2.product_id = p2.product_id
        GROUP BY p1.product_id, p2.product_id, p1.product_name, p2.product_name
        HAVING times_bought_together >= 1
        ORDER BY times_bought_together DESC, affinity_percentage DESC
        LIMIT 10
        """
        
        try:
            results = self.db.execute_query(affinity_query)
            if results:
                print("   Product Affinity Analysis (Frequently Bought Together):")
                for row in results:
                    print(f"   • {row['product_a']} + {row['product_b']}")
                    print(f"     Bought together {row['times_bought_together']} times ({row['affinity_percentage']:.1f}% affinity)")
                    print()
            else:
                print("   No product affinity patterns found")
        except Exception as e:
            print(f"   Error: {e}")

    def exercise_3_data_warehousing(self):
        """
        Exercise 3: Data Warehousing Concepts
        
        Tasks:
        1. Create summary tables
        2. Implement incremental updates
        3. Build reporting views
        """
        print("\n=== Exercise 3: Data Warehousing ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Creating sales summary table:")
        
        # Create summary table
        try:
            # Drop if exists
            self.db.execute_update("DROP TABLE IF EXISTS sales_summary")
            
            # Create summary table
            create_summary = """
            CREATE TABLE sales_summary (
                summary_date DATE PRIMARY KEY,
                total_orders INT DEFAULT 0,
                total_revenue DECIMAL(12,2) DEFAULT 0.00,
                total_customers INT DEFAULT 0,
                avg_order_value DECIMAL(10,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            self.db.execute_update(create_summary)
            print("   ✓ Sales summary table created")
            
            # Populate with data
            populate_summary = """
            INSERT INTO sales_summary (summary_date, total_orders, total_revenue, total_customers, avg_order_value)
            SELECT 
                DATE(order_date) as summary_date,
                COUNT(*) as total_orders,
                SUM(total_amount) as total_revenue,
                COUNT(DISTINCT customer_id) as total_customers,
                AVG(total_amount) as avg_order_value
            FROM orders
            GROUP BY DATE(order_date)
            """
            
            rows = self.db.execute_update(populate_summary)
            print(f"   ✓ Populated with {rows} daily summaries")
            
        except Exception as e:
            print(f"   Error creating summary table: {e}")
        
        print("\n2. Sales summary report:")
        
        try:
            summary_query = """
            SELECT 
                summary_date,
                total_orders,
                total_revenue,
                total_customers,
                avg_order_value,
                LAG(total_revenue) OVER (ORDER BY summary_date) as prev_day_revenue,
                ROUND(
                    (total_revenue - LAG(total_revenue) OVER (ORDER BY summary_date)) 
                    / NULLIF(LAG(total_revenue) OVER (ORDER BY summary_date), 0) * 100, 2
                ) as revenue_growth_pct
            FROM sales_summary
            ORDER BY summary_date
            """
            
            results = self.db.execute_query(summary_query)
            if results:
                print("   Daily Sales Summary:")
                print("   Date       | Orders | Revenue  | Customers | Avg Order | Growth %")
                print("   -----------|--------|----------|-----------|-----------|----------")
                
                for row in results:
                    date = str(row['summary_date'])
                    orders = str(row['total_orders']).rjust(6)
                    revenue = f"${row['total_revenue']:.2f}".rjust(8)
                    customers = str(row['total_customers']).rjust(9)
                    avg_order = f"${row['avg_order_value']:.2f}".rjust(9)
                    growth = f"{row['revenue_growth_pct'] or 0:.1f}%".rjust(8)
                    
                    print(f"   {date} | {orders} | {revenue} | {customers} | {avg_order} | {growth}")
                    
        except Exception as e:
            print(f"   Error: {e}")

    def exercise_4_database_design(self):
        """
        Exercise 4: Advanced Database Design
        
        Tasks:
        1. Analyze current schema
        2. Identify normalization issues
        3. Propose improvements
        """
        print("\n=== Exercise 4: Database Design Analysis ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Schema analysis:")
        
        try:
            # Analyze table sizes
            table_analysis = """
            SELECT 
                TABLE_NAME,
                TABLE_ROWS,
                ROUND(DATA_LENGTH / 1024 / 1024, 2) as data_size_mb,
                ROUND(INDEX_LENGTH / 1024 / 1024, 2) as index_size_mb,
                ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) as total_size_mb
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC
            """
            
            results = self.db.execute_query(table_analysis)
            if results:
                print("   Table Size Analysis:")
                print("   Table Name       | Rows | Data MB | Index MB | Total MB")
                print("   -----------------|------|---------|----------|----------")
                
                for row in results:
                    table = row['TABLE_NAME'][:16].ljust(16)
                    rows = str(row['TABLE_ROWS'] or 0).rjust(4)
                    data_mb = f"{row['data_size_mb'] or 0:.2f}".rjust(7)
                    index_mb = f"{row['index_size_mb'] or 0:.2f}".rjust(8)
                    total_mb = f"{row['total_size_mb'] or 0:.2f}".rjust(8)
                    
                    print(f"   {table} | {rows} | {data_mb} | {index_mb} | {total_mb}")
                    
        except Exception as e:
            print(f"   Error: {e}")
        
        print("\n2. Foreign key relationships:")
        
        try:
            fk_analysis = """
            SELECT 
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME,
                CONSTRAINT_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = DATABASE()
            AND REFERENCED_TABLE_NAME IS NOT NULL
            ORDER BY TABLE_NAME, COLUMN_NAME
            """
            
            results = self.db.execute_query(fk_analysis)
            if results:
                print("   Foreign Key Relationships:")
                current_table = ""
                for row in results:
                    if row['TABLE_NAME'] != current_table:
                        current_table = row['TABLE_NAME']
                        print(f"\n   {current_table}:")
                    
                    print(f"     {row['COLUMN_NAME']} -> {row['REFERENCED_TABLE_NAME']}.{row['REFERENCED_COLUMN_NAME']}")
                    
        except Exception as e:
            print(f"   Error: {e}")
        
        print("\n3. Database design recommendations:")
        
        recommendations = [
            "✓ Good: Proper foreign key relationships maintained",
            "✓ Good: Primary keys on all tables",
            "✓ Good: Appropriate indexes for common queries",
            "→ Consider: Adding created_at/updated_at to all tables",
            "→ Consider: Soft deletes instead of hard deletes",
            "→ Consider: Partitioning large tables by date",
            "→ Consider: Archive strategy for old data",
            "→ Consider: Adding audit trail tables"
        ]
        
        for rec in recommendations:
            print(f"   {rec}")

    def exercise_5_performance_tuning(self):
        """
        Exercise 5: Advanced Performance Tuning
        
        Tasks:
        1. Identify bottlenecks
        2. Optimize queries
        3. Suggest infrastructure improvements
        """
        print("\n=== Exercise 5: Performance Tuning ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Database configuration analysis:")
        
        try:
            # Check important MySQL variables
            important_vars = [
                'innodb_buffer_pool_size',
                'max_connections',
                'query_cache_size',
                'tmp_table_size',
                'max_heap_table_size'
            ]
            
            print("   Key MySQL Configuration Variables:")
            for var in important_vars:
                try:
                    result = self.db.execute_query(f"SHOW VARIABLES LIKE '{var}'")
                    if result:
                        value = result[0].get('Value', 'N/A')
                        print(f"   - {var}: {value}")
                except Exception:
                    print(f"   - {var}: Unable to retrieve")
                    
        except Exception as e:
            print(f"   Error: {e}")
        
        print("\n2. Query performance analysis:")
        
        try:
            # Analyze slow query patterns
            slow_query_tips = [
                "Enable slow query log: SET GLOBAL slow_query_log = 'ON'",
                "Set slow query time: SET GLOBAL long_query_time = 2",
                "Monitor with: SHOW FULL PROCESSLIST",
                "Use EXPLAIN ANALYZE for detailed query analysis",
                "Profile with: SET profiling = 1; [query]; SHOW PROFILES"
            ]
            
            print("   Slow Query Analysis Tips:")
            for tip in slow_query_tips:
                print(f"   - {tip}")
                
        except Exception as e:
            print(f"   Error: {e}")
        
        print("\n3. Performance optimization recommendations:")
        
        optimizations = [
            "Database Level:",
            "  • Increase innodb_buffer_pool_size to 70-80% of RAM",
            "  • Enable query cache for read-heavy workloads",
            "  • Use connection pooling",
            "  • Regular OPTIMIZE TABLE maintenance",
            "",
            "Query Level:",
            "  • Add indexes on WHERE, JOIN, and ORDER BY columns",
            "  • Avoid SELECT * in production queries",
            "  • Use LIMIT for large result sets",
            "  • Consider query rewriting for complex JOINs",
            "",
            "Application Level:",
            "  • Implement application-level caching",
            "  • Use read replicas for reporting",
            "  • Batch multiple operations",
            "  • Implement proper connection management"
        ]
        
        for opt in optimizations:
            print(f"   {opt}")


def main():
    """Run advanced exercises."""
    print("MySQL Advanced Exercises")
    print("=" * 30)
    print("Challenge yourself with advanced MySQL concepts!")
    print()
    
    exercises = AdvancedExercises()
    
    try:
        if not exercises.setup():
            print("Failed to connect to database. Please check your configuration.")
            return
        
        exercises.exercise_1_query_optimization()
        exercises.exercise_2_complex_analytics()
        exercises.exercise_3_data_warehousing()
        exercises.exercise_4_database_design()
        exercises.exercise_5_performance_tuning()
        
        print("\n" + "=" * 30)
        print("🎉 Congratulations! You've completed the advanced exercises!")
        print("You now have experience with:")
        print("• Query optimization and performance analysis")
        print("• Complex analytics and business intelligence")
        print("• Data warehousing concepts")
        print("• Database design principles")
        print("• Performance tuning strategies")
        print()
        print("Continue practicing with real-world datasets and scenarios!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. MySQL server running")
        print("2. Database and tables created")
        print("3. Sample data loaded")
        print("4. .env file configured")
        print("5. Sufficient privileges for advanced operations")
        
    finally:
        exercises.cleanup()


if __name__ == "__main__":
    main()
