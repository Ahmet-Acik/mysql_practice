"""
MySQL Transactions Examples
Demonstrates transaction handling, ACID properties, and error recovery.
"""

import sys
import os
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
        if not self.db:
            print("   Error: No database connection")
            return False
        return True

    def basic_transaction_demo(self):
        """Demonstrate basic transaction operations."""
        print("=== Basic Transaction Demo ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Successful transaction - Transfer inventory:")
        
        try:
            # Start transaction
            if not self.db.connection:
                raise Exception("No database connection")
            self.db.connection.start_transaction()
            
            # Get current stock levels
            stock_query = "SELECT product_name, stock_quantity FROM products WHERE sku IN ('ELEC-001', 'ELEC-002')"
            initial_stock = self.db.execute_query(stock_query)
            
            if initial_stock and len(initial_stock) >= 2:
                product1, product2 = initial_stock[0], initial_stock[1]
                print(f"   Before: {product1['product_name']}: {product1['stock_quantity']}")
                print(f"   Before: {product2['product_name']}: {product2['stock_quantity']}")
                
                # Transfer 10 units from product1 to product2
                transfer_amount = 10
                
                # Reduce stock from first product
                update1 = "UPDATE products SET stock_quantity = stock_quantity - %s WHERE sku = 'ELEC-001'"
                rows1 = self.db.execute_update(update1, (transfer_amount,))
                
                # Add stock to second product
                update2 = "UPDATE products SET stock_quantity = stock_quantity + %s WHERE sku = 'ELEC-002'"
                rows2 = self.db.execute_update(update2, (transfer_amount,))
                
                if rows1 > 0 and rows2 > 0:
                    # Commit the transaction
                    self.db.connection.commit()
                    print(f"   ✓ Successfully transferred {transfer_amount} units")
                    
                    # Show final stock levels
                    final_stock = self.db.execute_query(stock_query)
                    if final_stock and len(final_stock) >= 2:
                        product1, product2 = final_stock[0], final_stock[1]
                        print(f"   After: {product1['product_name']}: {product1['stock_quantity']}")
                        print(f"   After: {product2['product_name']}: {product2['stock_quantity']}")
                else:
                    self.db.connection.rollback()
                    print("   ✗ Transaction failed - rolled back")
            else:
                self.db.connection.rollback()
                print("   ✗ Could not find required products")
                
        except Exception as e:
            if self.db.connection:
                self.db.connection.rollback()
            print(f"   ✗ Transaction failed: {e}")

    def rollback_demo(self):
        """Demonstrate transaction rollback on error."""
        print("\n=== Transaction Rollback Demo ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Failed transaction - Insufficient inventory:")
        
        try:
            # Start transaction
            self.db.connection.start_transaction()
            
            # Try to order more items than available
            product_query = "SELECT product_id, product_name, stock_quantity FROM products WHERE sku = 'ELEC-003' LIMIT 1"
            product_result = self.db.execute_query(product_query)
            
            if product_result:
                product = product_result[0]
                current_stock = int(product['stock_quantity'])
                order_quantity = current_stock + 50  # Try to order more than available
                
                print(f"   Product: {product['product_name']}")
                print(f"   Current Stock: {current_stock}")
                print(f"   Trying to order: {order_quantity}")
                
                # Check if we have enough stock
                if current_stock < order_quantity:
                    # This will cause a rollback
                    raise ValueError(f"Insufficient stock: need {order_quantity}, have {current_stock}")
                
                # If we had enough stock, we would continue with the order
                # ... order processing logic ...
                
                self.db.connection.commit()
                print("   ✓ Order processed successfully")
                
        except ValueError as e:
            self.db.connection.rollback()
            print(f"   ✗ Transaction rolled back: {e}")
        except Exception as e:
            self.db.connection.rollback()
            print(f"   ✗ Transaction failed: {e}")

    def complex_transaction_demo(self):
        """Demonstrate complex multi-table transaction."""
        print("\n=== Complex Transaction Demo ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Complete order processing transaction:")
        
        try:
            # Start transaction
            self.db.connection.start_transaction()
            
            # Customer and product info
            customer_id = 1  # John Doe
            products_to_order = [
                {'sku': 'ELEC-004', 'quantity': 2},
                {'sku': 'CLOTH-001', 'quantity': 1}
            ]
            
            # Step 1: Create order
            create_order_query = """
            INSERT INTO orders (customer_id, order_date, status, total_amount)
            VALUES (%s, NOW(), 'processing', 0)
            """
            order_rows = self.db.execute_update(create_order_query, (customer_id,))
            
            if order_rows == 0:
                raise Exception("Failed to create order")
            
            # Get the new order ID
            order_id_query = "SELECT LAST_INSERT_ID() as order_id"
            order_id_result = self.db.execute_query(order_id_query)
            order_id = order_id_result[0]['order_id'] if order_id_result else None
            
            if not order_id:
                raise Exception("Failed to get order ID")
            
            print(f"   Created order #{order_id}")
            
            total_amount = 0
            
            # Step 2: Process each product
            for item in products_to_order:
                # Get product info
                product_query = """
                SELECT product_id, product_name, price, stock_quantity 
                FROM products WHERE sku = %s
                """
                product_result = self.db.execute_query(product_query, (item['sku'],))
                
                if not product_result:
                    raise Exception(f"Product {item['sku']} not found")
                
                product = product_result[0]
                
                # Check stock
                if int(product['stock_quantity']) < item['quantity']:
                    raise Exception(f"Insufficient stock for {product['product_name']}")
                
                # Calculate prices
                unit_price = float(product['price'])
                line_total = unit_price * item['quantity']
                total_amount += line_total
                
                # Add order item
                add_item_query = """
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                VALUES (%s, %s, %s, %s, %s)
                """
                item_rows = self.db.execute_update(add_item_query, (
                    order_id, product['product_id'], item['quantity'], unit_price, line_total
                ))
                
                if item_rows == 0:
                    raise Exception(f"Failed to add {product['product_name']} to order")
                
                # Update stock
                update_stock_query = """
                UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s
                """
                stock_rows = self.db.execute_update(update_stock_query, (
                    item['quantity'], product['product_id']
                ))
                
                if stock_rows == 0:
                    raise Exception(f"Failed to update stock for {product['product_name']}")
                
                print(f"   Added {item['quantity']}x {product['product_name']} @ ${unit_price:.2f}")
            
            # Step 3: Update order total
            update_total_query = "UPDATE orders SET total_amount = %s WHERE order_id = %s"
            total_rows = self.db.execute_update(update_total_query, (total_amount, order_id))
            
            if total_rows == 0:
                raise Exception("Failed to update order total")
            
            # Commit the transaction
            self.db.connection.commit()
            print(f"   ✓ Order completed successfully! Total: ${total_amount:.2f}")
            
        except Exception as e:
            self.db.connection.rollback()
            print(f"   ✗ Order failed - all changes rolled back: {e}")

    def deadlock_simulation_demo(self):
        """Demonstrate deadlock detection and handling."""
        print("\n=== Deadlock Prevention Demo ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Transaction isolation levels:")
        
        # Show current isolation level
        try:
            isolation_query = "SELECT @@transaction_isolation as isolation_level"
            result = self.db.execute_query(isolation_query)
            if result:
                print(f"   Current isolation level: {result[0]['isolation_level']}")
            
            # Demonstrate different isolation levels
            isolation_levels = [
                'READ-UNCOMMITTED',
                'READ-COMMITTED', 
                'REPEATABLE-READ',
                'SERIALIZABLE'
            ]
            
            print("\n   Available isolation levels:")
            for level in isolation_levels:
                print(f"   - {level}")
                
            # Set isolation level example
            print("\n   Setting isolation level to READ COMMITTED:")
            self.db.execute_update("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
            
            result = self.db.execute_query(isolation_query)
            if result:
                print(f"   New isolation level: {result[0]['isolation_level']}")
                
        except Exception as e:
            print(f"   Error: {e}")

    def savepoint_demo(self):
        """Demonstrate savepoints for partial rollbacks."""
        print("\n=== Savepoint Demo ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Using savepoints for partial rollbacks:")
        
        try:
            # Start transaction
            self.db.connection.start_transaction()
            
            # Initial stock check
            stock_query = "SELECT product_name, stock_quantity FROM products WHERE sku = 'ELEC-005' LIMIT 1"
            initial_result = self.db.execute_query(stock_query)
            
            if initial_result:
                initial_stock = int(initial_result[0]['stock_quantity'])
                product_name = initial_result[0]['product_name']
                
                print(f"   Initial stock for {product_name}: {initial_stock}")
                
                # First operation - reduce stock by 5
                update1 = "UPDATE products SET stock_quantity = stock_quantity - 5 WHERE sku = 'ELEC-005'"
                self.db.execute_update(update1)
                print("   ✓ Reduced stock by 5")
                
                # Create savepoint
                self.db.connection.execute("SAVEPOINT sp1")
                print("   ✓ Created savepoint 'sp1'")
                
                # Second operation - reduce stock by 10 more
                update2 = "UPDATE products SET stock_quantity = stock_quantity - 10 WHERE sku = 'ELEC-005'"
                self.db.execute_update(update2)
                print("   ✓ Reduced stock by 10 more")
                
                # Check current stock
                current_result = self.db.execute_query(stock_query)
                if current_result:
                    current_stock = int(current_result[0]['stock_quantity'])
                    print(f"   Current stock: {current_stock}")
                
                # Simulate error condition - rollback to savepoint
                if current_stock < 10:  # Some business rule
                    print("   ✗ Stock too low! Rolling back to savepoint...")
                    self.db.connection.execute("ROLLBACK TO SAVEPOINT sp1")
                    
                    # Check stock after rollback
                    rollback_result = self.db.execute_query(stock_query)
                    if rollback_result:
                        rollback_stock = int(rollback_result[0]['stock_quantity'])
                        print(f"   Stock after rollback: {rollback_stock}")
                
                # Commit the transaction (keeps changes up to savepoint)
                self.db.connection.commit()
                print("   ✓ Transaction committed")
                
                # Final stock check
                final_result = self.db.execute_query(stock_query)
                if final_result:
                    final_stock = int(final_result[0]['stock_quantity'])
                    print(f"   Final stock: {final_stock}")
            
        except Exception as e:
            self.db.connection.rollback()
            print(f"   ✗ Transaction failed: {e}")

    def transaction_monitoring_demo(self):
        """Demonstrate transaction monitoring and diagnostics."""
        print("\n=== Transaction Monitoring Demo ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Transaction status information:")
        
        try:
            # Show transaction status
            status_queries = [
                ("Autocommit status", "SELECT @@autocommit as autocommit_status"),
                ("Transaction isolation", "SELECT @@transaction_isolation as isolation"),
                ("Transaction read only", "SELECT @@transaction_read_only as read_only"),
                ("InnoDB status", "SHOW ENGINE INNODB STATUS")
            ]
            
            for description, query in status_queries[:3]:  # Skip InnoDB status as it's very verbose
                try:
                    result = self.db.execute_query(query)
                    if result:
                        print(f"   {description}: {list(result[0].values())[0]}")
                except Exception as e:
                    print(f"   {description}: Error - {e}")
            
            # Show active transactions (if any)
            print("\n2. Active transactions information:")
            transactions_query = """
            SELECT 
                trx_id,
                trx_state,
                trx_started,
                trx_isolation_level,
                trx_tables_in_use,
                trx_tables_locked
            FROM INFORMATION_SCHEMA.INNODB_TRX
            """
            
            try:
                transactions = self.db.execute_query(transactions_query)
                if transactions:
                    for trx in transactions:
                        print(f"   Transaction {trx['trx_id']}: {trx['trx_state']}")
                        print(f"     Started: {trx['trx_started']}")
                        print(f"     Isolation: {trx['trx_isolation_level']}")
                        print(f"     Tables in use: {trx['trx_tables_in_use']}")
                else:
                    print("   No active transactions")
            except Exception as e:
                print(f"   Could not retrieve transaction info: {e}")
                
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
        examples.rollback_demo()
        examples.complex_transaction_demo()
        examples.deadlock_simulation_demo()
        examples.savepoint_demo()
        examples.transaction_monitoring_demo()
        
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
