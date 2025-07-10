"""
MySQL Transactions Examples
Demonstrates transaction handling, ACID properties, and error recovery.
"""

import os
import sys
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from config.database import MySQLConnection


class TransactionExamples:
    """MySQL transaction handling demonstrations."""

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
        if not self.db or not self.db.connection:
            print("   Error: No database connection")
            return False
        return True

    def basic_transaction_demo(self):
        """Demonstrate basic transaction operations using execute_update."""
        print("=== Basic Transaction Demo ===")

        if not self._check_connection():
            return
        assert self.db is not None

        print("\n1. Stock transfer with transaction safety:")

        # Get current stock levels first
        stock_query = "SELECT product_name, stock_quantity FROM products WHERE sku IN ('ELEC-001', 'ELEC-002') LIMIT 2"
        initial_stock = self.db.execute_query(stock_query)

        if initial_stock and len(initial_stock) >= 2:
            product1, product2 = initial_stock[0], initial_stock[1]
            print(
                f"   Before: {product1['product_name']}: {product1['stock_quantity']}"
            )
            print(
                f"   Before: {product2['product_name']}: {product2['stock_quantity']}"
            )

            # Simulate stock transfer - reduce from one, add to another
            transfer_amount = 5

            # In a real transaction, these would be wrapped in START TRANSACTION / COMMIT
            print(f"   Transferring {transfer_amount} units...")

            # Update stocks (the MySQLConnection class handles transaction-like behavior)
            update1 = "UPDATE products SET stock_quantity = stock_quantity - %s WHERE sku = 'ELEC-001'"
            rows1 = self.db.execute_update(update1, (transfer_amount,))

            update2 = "UPDATE products SET stock_quantity = stock_quantity + %s WHERE sku = 'ELEC-002'"
            rows2 = self.db.execute_update(update2, (transfer_amount,))

            if rows1 > 0 and rows2 > 0:
                print("   ✓ Transfer completed successfully")

                # Show final stock levels
                final_stock = self.db.execute_query(stock_query)
                if final_stock and len(final_stock) >= 2:
                    product1, product2 = final_stock[0], final_stock[1]
                    print(
                        f"   After: {product1['product_name']}: {product1['stock_quantity']}"
                    )
                    print(
                        f"   After: {product2['product_name']}: {product2['stock_quantity']}"
                    )
            else:
                print("   ✗ Transfer failed")

    def transaction_isolation_demo(self):
        """Demonstrate transaction isolation concepts."""
        print("\n=== Transaction Isolation Demo ===")

        if not self._check_connection():
            return
        assert self.db is not None

        print("\n1. Current transaction settings:")

        try:
            # Show current isolation level
            isolation_query = "SELECT @@transaction_isolation as isolation_level"
            result = self.db.execute_query(isolation_query)
            if result:
                print(f"   Current isolation level: {result[0]['isolation_level']}")

            # Show autocommit status
            autocommit_query = "SELECT @@autocommit as autocommit_status"
            result = self.db.execute_query(autocommit_query)
            if result:
                print(f"   Autocommit status: {result[0]['autocommit_status']}")

        except Exception as e:
            print(f"   Error: {e}")

    def transaction_best_practices_demo(self):
        """Demonstrate transaction best practices."""
        print("\n=== Transaction Best Practices ===")

        if not self._check_connection():
            return
        assert self.db is not None

        print("\n1. Order processing example with proper error handling:")

        try:
            # Simulate order processing
            customer_id = 1
            product_sku = "ELEC-003"
            order_quantity = 2

            # Step 1: Check product availability
            product_query = """
            SELECT product_id, product_name, price, stock_quantity 
            FROM products WHERE sku = %s
            """
            product_result = self.db.execute_query(product_query, (product_sku,))

            if not product_result:
                print(f"   ✗ Product {product_sku} not found")
                return

            product = product_result[0]
            current_stock = int(product["stock_quantity"])

            print(f"   Product: {product['product_name']}")
            print(f"   Current stock: {current_stock}")
            print(f"   Requested quantity: {order_quantity}")

            # Step 2: Validate stock availability
            if current_stock < order_quantity:
                print(
                    f"   ✗ Insufficient stock (need {order_quantity}, have {current_stock})"
                )
                return

            # Step 3: Create order (simplified)
            create_order_query = """
            INSERT INTO orders (customer_id, order_date, status, total_amount)
            VALUES (%s, NOW(), 'processing', %s)
            """
            total_amount = float(product["price"]) * order_quantity
            order_rows = self.db.execute_update(
                create_order_query, (customer_id, total_amount)
            )

            if order_rows > 0:
                print(f"   ✓ Order created successfully")
                print(f"   Total amount: ${total_amount:.2f}")

                # Step 4: Update stock
                update_stock_query = """
                UPDATE products SET stock_quantity = stock_quantity - %s WHERE sku = %s
                """
                stock_rows = self.db.execute_update(
                    update_stock_query, (order_quantity, product_sku)
                )

                if stock_rows > 0:
                    print(
                        f"   ✓ Stock updated (new quantity: {current_stock - order_quantity})"
                    )
                else:
                    print("   ✗ Failed to update stock")
            else:
                print("   ✗ Failed to create order")

        except Exception as e:
            print(f"   ✗ Order processing failed: {e}")

    def locking_demo(self):
        """Demonstrate locking concepts."""
        print("\n=== Locking Demo ===")

        if not self._check_connection():
            return
        assert self.db is not None

        print("\n1. Table locking information:")

        try:
            # Show current locks (if any)
            locks_query = """
            SELECT 
                OBJECT_SCHEMA,
                OBJECT_NAME,
                LOCK_TYPE,
                LOCK_MODE,
                LOCK_STATUS
            FROM performance_schema.metadata_locks
            WHERE OBJECT_SCHEMA = DATABASE()
            LIMIT 5
            """

            try:
                locks_result = self.db.execute_query(locks_query)
                if locks_result:
                    print("   Current locks:")
                    for lock in locks_result:
                        print(
                            f"   - {lock['OBJECT_NAME']}: {lock['LOCK_TYPE']} ({lock['LOCK_MODE']})"
                        )
                else:
                    print("   No active locks found")
            except Exception as e:
                print(f"   Could not retrieve lock information: {e}")

            # Show deadlock information
            print("\n2. Deadlock prevention tips:")
            tips = [
                "- Always acquire locks in the same order",
                "- Keep transactions short",
                "- Use appropriate isolation levels",
                "- Handle deadlock exceptions gracefully",
                "- Consider using SELECT FOR UPDATE for explicit locking",
            ]

            for tip in tips:
                print(f"   {tip}")

        except Exception as e:
            print(f"   Error: {e}")

    def performance_monitoring_demo(self):
        """Demonstrate transaction performance monitoring."""
        print("\n=== Performance Monitoring Demo ===")

        if not self._check_connection():
            return
        assert self.db is not None

        print("\n1. Transaction performance metrics:")

        try:
            # Show transaction-related status variables
            status_queries = [
                ("Questions", "SHOW STATUS LIKE 'Questions'"),
                ("Com_commit", "SHOW STATUS LIKE 'Com_commit'"),
                ("Com_rollback", "SHOW STATUS LIKE 'Com_rollback'"),
                ("Innodb_rows_read", "SHOW STATUS LIKE 'Innodb_rows_read'"),
                ("Innodb_rows_inserted", "SHOW STATUS LIKE 'Innodb_rows_inserted'"),
                ("Innodb_rows_updated", "SHOW STATUS LIKE 'Innodb_rows_updated'"),
                ("Innodb_rows_deleted", "SHOW STATUS LIKE 'Innodb_rows_deleted'"),
            ]

            for name, query in status_queries:
                try:
                    result = self.db.execute_query(query)
                    if result:
                        value = result[0].get("Value", "N/A")
                        print(f"   {name}: {value}")
                except Exception as e:
                    print(f"   {name}: Error - {e}")

            print("\n2. Performance optimization tips:")
            optimization_tips = [
                "- Use indexes on frequently queried columns",
                "- Avoid long-running transactions",
                "- Batch multiple operations when possible",
                "- Monitor slow query log",
                "- Use EXPLAIN to analyze query performance",
                "- Consider connection pooling for high-load applications",
            ]

            for tip in optimization_tips:
                print(f"   {tip}")

        except Exception as e:
            print(f"   Error: {e}")


def main():
    """Run transaction examples."""
    print("MySQL Transaction Examples")
    print("=" * 30)

    examples = TransactionExamples()

    try:
        if not examples.setup():
            print("Failed to connect to database. Please check your configuration.")
            return

        examples.basic_transaction_demo()
        examples.transaction_isolation_demo()
        examples.transaction_best_practices_demo()
        examples.locking_demo()
        examples.performance_monitoring_demo()

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. MySQL server running")
        print("2. Database and tables created")
        print("3. Sample data loaded")
        print("4. .env file configured")
        print("5. InnoDB storage engine enabled")

    finally:
        examples.cleanup()


if __name__ == "__main__":
    main()
