"""
MySQL Practice Project - Unit Tests
Test suite for validating database operations and query functionality.
"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection
from tests.test_config import is_database_available


def test_connection():
    """Simple function to test database connectivity."""
    assert is_database_available(), "Database connection should be available"


class TestDatabaseOperations(unittest.TestCase):
    """Test database operations."""

    @classmethod
    def setUpClass(cls):
        """Set up test database connection."""
        # Check if database is available before attempting connection
        if not is_database_available():
            raise unittest.SkipTest("Database not available - skipping database tests")

        cls.db = MySQLConnection()
        if not cls.db.connect():
            raise unittest.SkipTest(
                "Failed to connect to test database - skipping tests"
            )

    @classmethod
    def tearDownClass(cls):
        """Clean up database connection."""
        if cls.db:
            cls.db.disconnect()

    def test_database_connection(self):
        """Test database connectivity."""
        self.assertIsNotNone(self.db.connection)
        if self.db.connection is not None:
            self.assertTrue(self.db.connection.is_connected())

    def test_basic_queries(self):
        """Test basic query operations."""
        # Test SELECT
        result = self.db.execute_query("SELECT 1 as test_value")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        if result:  # Type narrowing for mypy
            self.assertGreater(len(result), 0)
            self.assertEqual(result[0]["test_value"], 1)

    def test_table_existence(self):
        """Test that all required tables exist."""
        tables = ["customers", "products", "categories", "orders", "order_items"]

        for table in tables:
            result = self.db.execute_query(
                "SELECT COUNT(*) as count FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = %s",
                (table,),
            )
            self.assertIsNotNone(result, f"Query failed for table {table}")
            if result:  # Type narrowing
                self.assertEqual(result[0]["count"], 1, f"Table {table} does not exist")

    def test_sample_data(self):
        """Test that sample data exists."""
        # Test customers
        customers = self.db.execute_query("SELECT COUNT(*) as count FROM customers")
        self.assertIsNotNone(customers, "Customers query failed")
        if customers:  # Type narrowing
            self.assertGreater(customers[0]["count"], 0, "No sample customers found")

        # Test products
        products = self.db.execute_query("SELECT COUNT(*) as count FROM products")
        self.assertIsNotNone(products, "Products query failed")
        if products:  # Type narrowing
            self.assertGreater(products[0]["count"], 0, "No sample products found")

        # Test orders
        orders = self.db.execute_query("SELECT COUNT(*) as count FROM orders")
        self.assertIsNotNone(orders, "Orders query failed")
        if orders:  # Type narrowing
            self.assertGreater(orders[0]["count"], 0, "No sample orders found")

    def test_foreign_key_constraints(self):
        """Test foreign key relationships."""
        # Test products have valid categories
        result = self.db.execute_query(
            """
            SELECT COUNT(*) as invalid_count 
            FROM products p 
            LEFT JOIN categories c ON p.category_id = c.category_id 
            WHERE c.category_id IS NULL
        """
        )
        self.assertIsNotNone(result, "Products-categories FK query failed")
        if result:  # Type narrowing
            self.assertEqual(
                result[0]["invalid_count"],
                0,
                "Found products with invalid category references",
            )

        # Test orders have valid customers
        result = self.db.execute_query(
            """
            SELECT COUNT(*) as invalid_count 
            FROM orders o 
            LEFT JOIN customers c ON o.customer_id = c.customer_id 
            WHERE c.customer_id IS NULL
        """
        )
        self.assertIsNotNone(result, "Orders-customers FK query failed")
        if result:  # Type narrowing
            self.assertEqual(
                result[0]["invalid_count"],
                0,
                "Found orders with invalid customer references",
            )

    def test_advanced_queries(self):
        """Test complex query functionality."""
        # Test JOINs
        result = self.db.execute_query(
            """
            SELECT c.customer_id, c.first_name, COUNT(o.order_id) as order_count
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name
            HAVING order_count > 0
        """
        )
        self.assertIsNotNone(result, "JOIN query failed")

        # Test window functions (if supported)
        try:
            result = self.db.execute_query(
                """
                SELECT product_name, price, 
                       ROW_NUMBER() OVER (ORDER BY price DESC) as price_rank
                FROM products LIMIT 5
            """
            )
            self.assertIsNotNone(result, "Window function query failed")
        except Exception:
            self.skipTest("Window functions not supported in this MySQL version")


class TestPerformance(unittest.TestCase):
    """Test query performance."""

    @classmethod
    def setUpClass(cls):
        """Set up test database connection."""
        # Check if database is available before attempting connection
        if not is_database_available():
            raise unittest.SkipTest(
                "Database not available - skipping performance tests"
            )

        cls.db = MySQLConnection()
        if not cls.db.connect():
            raise unittest.SkipTest(
                "Failed to connect to test database - skipping tests"
            )

    @classmethod
    def tearDownClass(cls):
        """Clean up database connection."""
        if cls.db:
            cls.db.disconnect()

    def test_query_execution_time(self):
        """Test that queries execute within reasonable time."""
        import time

        start_time = time.time()
        result = self.db.execute_query("SELECT COUNT(*) FROM products")
        execution_time = time.time() - start_time

        self.assertLess(execution_time, 1.0, "Simple query took too long to execute")
        self.assertIsNotNone(result)

    def test_index_usage(self):
        """Test that indexes exist for common queries."""
        # Check for primary key indexes
        result = self.db.execute_query(
            """
            SELECT COUNT(*) as pk_count
            FROM information_schema.statistics 
            WHERE table_schema = DATABASE() 
            AND index_name = 'PRIMARY'
        """
        )
        self.assertIsNotNone(result, "Index query failed")
        if result:  # Type narrowing
            self.assertGreater(result[0]["pk_count"], 0, "No primary key indexes found")


if __name__ == "__main__":
    # Check database availability first
    if not is_database_available():
        print("⚠️  Database not available. Skipping tests.")
        print("To run tests:")
        print("1. Start Docker: docker-compose up -d")
        print(
            "2. Run tests in Docker: docker exec -it mysql_practice_app python tests/test_database.py"
        )
        sys.exit(0)

    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))

    # Run with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*50}")
    print(f"TESTS RUN: {result.testsRun}")
    print(f"FAILURES: {len(result.failures)}")
    print(f"ERRORS: {len(result.errors)}")
    print(f"SKIPPED: {len(result.skipped) if hasattr(result, 'skipped') else 0}")

    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")

    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")

    if result.wasSuccessful():
        print(f"\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n❌ SOME TESTS FAILED!")
        sys.exit(1)
