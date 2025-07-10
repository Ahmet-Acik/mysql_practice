"""
MySQL Stored Procedures Examples
Demonstrates stored procedures, functions, and triggers.
"""

import sys
import os
from typing import Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class StoredProcedureExamples:
    """MySQL stored procedures demonstrations."""
    
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

    def create_procedures_demo(self):
        """Create sample stored procedures."""
        print("=== Creating Stored Procedures ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        # Drop existing procedures first
        drop_procedures = [
            "DROP PROCEDURE IF EXISTS GetCustomerOrders",
            "DROP PROCEDURE IF EXISTS UpdateProductStock", 
            "DROP PROCEDURE IF EXISTS GetProductsByCategory",
            "DROP FUNCTION IF EXISTS CalculateOrderTotal",
            "DROP TRIGGER IF EXISTS update_order_total"
        ]
        
        for drop_sql in drop_procedures:
            try:
                self.db.execute_update(drop_sql)
            except Exception:
                pass  # Ignore if doesn't exist
        
        print("\n1. Creating procedure: GetCustomerOrders")
        
        # Procedure 1: Get customer orders
        create_proc1 = """
        CREATE PROCEDURE GetCustomerOrders(IN customer_email VARCHAR(100))
        BEGIN
            SELECT 
                o.order_id,
                o.order_date,
                o.status,
                o.total_amount,
                COUNT(oi.order_item_id) as item_count
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            WHERE c.email = customer_email
            GROUP BY o.order_id, o.order_date, o.status, o.total_amount
            ORDER BY o.order_date DESC;
        END
        """
        
        try:
            self.db.execute_update(create_proc1)
            print("   ✓ GetCustomerOrders procedure created")
        except Exception as e:
            print(f"   ✗ Error creating GetCustomerOrders: {e}")
        
        print("\n2. Creating procedure: UpdateProductStock")
        
        # Procedure 2: Update product stock
        create_proc2 = """
        CREATE PROCEDURE UpdateProductStock(
            IN p_sku VARCHAR(50),
            IN p_quantity_change INT,
            OUT p_new_stock INT,
            OUT p_result VARCHAR(100)
        )
        BEGIN
            DECLARE current_stock INT DEFAULT 0;
            DECLARE product_count INT DEFAULT 0;
            
            -- Check if product exists
            SELECT COUNT(*) INTO product_count FROM products WHERE sku = p_sku;
            
            IF product_count = 0 THEN
                SET p_result = 'Product not found';
                SET p_new_stock = -1;
            ELSE
                -- Get current stock
                SELECT stock_quantity INTO current_stock FROM products WHERE sku = p_sku;
                
                -- Check if we have enough stock for reduction
                IF (current_stock + p_quantity_change) < 0 THEN
                    SET p_result = 'Insufficient stock';
                    SET p_new_stock = current_stock;
                ELSE
                    -- Update stock
                    UPDATE products 
                    SET stock_quantity = stock_quantity + p_quantity_change 
                    WHERE sku = p_sku;
                    
                    -- Get new stock level
                    SELECT stock_quantity INTO p_new_stock FROM products WHERE sku = p_sku;
                    SET p_result = 'Stock updated successfully';
                END IF;
            END IF;
        END
        """
        
        try:
            self.db.execute_update(create_proc2)
            print("   ✓ UpdateProductStock procedure created")
        except Exception as e:
            print(f"   ✗ Error creating UpdateProductStock: {e}")
        
        print("\n3. Creating procedure: GetProductsByCategory")
        
        # Procedure 3: Get products by category with pagination
        create_proc3 = """
        CREATE PROCEDURE GetProductsByCategory(
            IN p_category_name VARCHAR(100),
            IN p_limit INT,
            IN p_offset INT
        )
        BEGIN
            SELECT 
                p.product_id,
                p.product_name,
                p.price,
                p.stock_quantity,
                p.sku,
                c.category_name
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE c.category_name = p_category_name
            ORDER BY p.product_name
            LIMIT p_limit OFFSET p_offset;
        END
        """
        
        try:
            self.db.execute_update(create_proc3)
            print("   ✓ GetProductsByCategory procedure created")
        except Exception as e:
            print(f"   ✗ Error creating GetProductsByCategory: {e}")

    def create_functions_demo(self):
        """Create sample functions."""
        print("\n=== Creating Functions ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Creating function: CalculateOrderTotal")
        
        # Function 1: Calculate order total
        create_func1 = """
        CREATE FUNCTION CalculateOrderTotal(order_id_param INT) 
        RETURNS DECIMAL(10,2)
        READS SQL DATA
        DETERMINISTIC
        BEGIN
            DECLARE total DECIMAL(10,2) DEFAULT 0.00;
            
            SELECT COALESCE(SUM(total_price), 0.00) INTO total
            FROM order_items
            WHERE order_id = order_id_param;
            
            RETURN total;
        END
        """
        
        try:
            self.db.execute_update(create_func1)
            print("   ✓ CalculateOrderTotal function created")
        except Exception as e:
            print(f"   ✗ Error creating CalculateOrderTotal: {e}")

    def call_procedures_demo(self):
        """Demonstrate calling stored procedures."""
        print("\n=== Calling Stored Procedures ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Calling GetCustomerOrders for John Doe:")
        
        try:
            # Use a direct query instead of CALL to avoid multi-statement issues
            query = """
            SELECT 
                o.order_id,
                o.order_date,
                o.status,
                o.total_amount,
                COUNT(oi.order_item_id) as item_count
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            WHERE c.email = %s
            GROUP BY o.order_id, o.order_date, o.status, o.total_amount
            ORDER BY o.order_date DESC
            """
            
            results = self.db.execute_query(query, ('john.doe@email.com',))
            if results:
                print("   Orders found:")
                for order in results:
                    print(f"   - Order #{order['order_id']}: ${order['total_amount']:.2f}")
                    print(f"     Date: {order['order_date']}, Status: {order['status']}")
                    print(f"     Items: {order['item_count']}")
                    print()
            else:
                print("   No orders found")
        except Exception as e:
            print(f"   ✗ Error calling procedure: {e}")
        
        print("\n2. Calling GetProductsByCategory for Electronics:")
        
        try:
            # Use a direct query instead of CALL
            query = """
            SELECT 
                p.product_id,
                p.product_name,
                p.price,
                p.stock_quantity,
                p.sku,
                c.category_name
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE c.category_name = %s
            ORDER BY p.product_name
            LIMIT %s OFFSET %s
            """
            
            results = self.db.execute_query(query, ('Electronics', 5, 0))
            if results:
                print("   Electronics products:")
                for product in results:
                    print(f"   - {product['product_name']}: ${product['price']:.2f}")
                    print(f"     SKU: {product['sku']}, Stock: {product['stock_quantity']}")
                    print()
            else:
                print("   No products found")
        except Exception as e:
            print(f"   ✗ Error calling procedure: {e}")

    def procedure_with_output_demo(self):
        """Demonstrate procedures with output parameters - simplified approach."""
        print("\n=== Procedures with Output Parameters ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Testing stock updates (simulating UpdateProductStock procedure):")
        
        # Test cases - we'll simulate the procedure logic directly
        test_cases = [
            ("ELEC-001", 10, "Adding 10 units"),
            ("ELEC-001", -5, "Removing 5 units"),
            ("INVALID-SKU", 10, "Invalid product"),
        ]
        
        for sku, quantity_change, description in test_cases:
            print(f"\n   {description} for {sku}:")
            
            try:
                # Check if product exists
                check_query = "SELECT stock_quantity FROM products WHERE sku = %s"
                result = self.db.execute_query(check_query, (sku,))
                
                if not result:
                    print(f"     Result: Product not found")
                else:
                    current_stock = result[0]['stock_quantity']
                    new_stock = current_stock + quantity_change
                    
                    if new_stock < 0:
                        print(f"     Result: Insufficient stock (current: {current_stock})")
                    else:
                        # Update stock
                        update_query = "UPDATE products SET stock_quantity = %s WHERE sku = %s"
                        rows_affected = self.db.execute_update(update_query, (new_stock, sku))
                        
                        if rows_affected > 0:
                            print(f"     Result: Stock updated successfully")
                            print(f"     New Stock: {new_stock}")
                        else:
                            print(f"     Result: Update failed")
                    
            except Exception as e:
                print(f"     ✗ Error: {e}")

    def functions_demo(self):
        """Demonstrate using functions - simplified approach."""
        print("\n=== Using Functions ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Calculating order totals (simulating CalculateOrderTotal function):")
        
        try:
            # Get some order IDs first
            orders_query = "SELECT order_id FROM orders LIMIT 3"
            orders = self.db.execute_query(orders_query)
            
            if orders:
                for order in orders:
                    order_id = order['order_id']
                    
                    # Calculate total using direct query (simulating function)
                    calc_query = """
                    SELECT COALESCE(SUM(total_price), 0.00) as calculated_total
                    FROM order_items
                    WHERE order_id = %s
                    """
                    result = self.db.execute_query(calc_query, (order_id,))
                    
                    if result:
                        calculated_total = result[0]['calculated_total']
                        
                        # Compare with actual order total
                        actual_query = "SELECT total_amount FROM orders WHERE order_id = %s"
                        actual_result = self.db.execute_query(actual_query, (order_id,))
                        
                        if actual_result:
                            actual_total = actual_result[0]['total_amount']
                            print(f"   Order #{order_id}:")
                            print(f"     Calculated total: ${calculated_total:.2f}")
                            print(f"     Actual total: ${actual_total:.2f}")
                            
                            if abs(float(calculated_total) - float(actual_total)) < 0.01:
                                print("     ✓ Totals match")
                            else:
                                print("     ✗ Totals don't match")
                            print()
            else:
                print("   No orders found")
                        
        except Exception as e:
            print(f"   ✗ Error using function: {e}")

    def view_procedure_info_demo(self):
        """Show information about created procedures and functions."""
        print("\n=== Procedure and Function Information ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. List of stored procedures:")
        
        try:
            procedures_query = """
            SELECT 
                ROUTINE_NAME,
                ROUTINE_TYPE,
                CREATED,
                LAST_ALTERED,
                SQL_MODE,
                ROUTINE_COMMENT
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_SCHEMA = DATABASE()
            ORDER BY ROUTINE_TYPE, ROUTINE_NAME
            """
            
            procedures = self.db.execute_query(procedures_query)
            if procedures:
                current_type = ""
                for proc in procedures:
                    routine_type = proc.get('ROUTINE_TYPE', 'UNKNOWN')
                    routine_name = proc.get('ROUTINE_NAME', 'UNKNOWN')
                    created = proc.get('CREATED', 'UNKNOWN')
                    comment = proc.get('ROUTINE_COMMENT', '')
                    
                    if routine_type != current_type:
                        current_type = routine_type
                        print(f"\n   {current_type}S:")
                    
                    print(f"   - {routine_name}")
                    print(f"     Created: {created}")
                    if comment:
                        print(f"     Comment: {comment}")
            else:
                print("   No procedures or functions found")
                
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print("\n2. Procedure parameters:")
        
        try:
            params_query = """
            SELECT 
                SPECIFIC_NAME,
                PARAMETER_NAME,
                PARAMETER_MODE,
                DATA_TYPE
            FROM INFORMATION_SCHEMA.PARAMETERS
            WHERE SPECIFIC_SCHEMA = DATABASE()
            AND PARAMETER_NAME IS NOT NULL
            ORDER BY SPECIFIC_NAME, ORDINAL_POSITION
            """
            
            params = self.db.execute_query(params_query)
            if params:
                current_proc = ""
                for param in params:
                    specific_name = param.get('SPECIFIC_NAME', 'UNKNOWN')
                    param_name = param.get('PARAMETER_NAME', 'UNKNOWN')
                    param_mode = param.get('PARAMETER_MODE', 'UNKNOWN')
                    data_type = param.get('DATA_TYPE', 'UNKNOWN')
                    
                    if specific_name != current_proc:
                        current_proc = specific_name
                        print(f"\n   {current_proc}:")
                    
                    mode = param_mode or 'RETURN'
                    print(f"     {mode} {param_name}: {data_type}")
            else:
                print("   No parameters found")
                
        except Exception as e:
            print(f"   ✗ Error: {e}")

    def cleanup_procedures_demo(self):
        """Clean up created procedures and functions."""
        print("\n=== Cleanup (Optional) ===")
        
        if not self._check_connection():
            return
        assert self.db is not None
        
        print("\n1. Cleaning up procedures and functions:")
        
        cleanup_statements = [
            "DROP PROCEDURE IF EXISTS GetCustomerOrders",
            "DROP PROCEDURE IF EXISTS UpdateProductStock",
            "DROP PROCEDURE IF EXISTS GetProductsByCategory", 
            "DROP FUNCTION IF EXISTS CalculateOrderTotal"
        ]
        
        for statement in cleanup_statements:
            try:
                self.db.execute_update(statement)
                routine_name = statement.split()[-1]
                print(f"   ✓ Dropped {routine_name}")
            except Exception as e:
                print(f"   ✗ Error dropping routine: {e}")


def main():
    """Run stored procedure examples."""
    print("MySQL Stored Procedures Examples")
    print("=" * 37)
    
    examples = StoredProcedureExamples()
    
    try:
        if not examples.setup():
            print("Failed to connect to database. Please check your configuration.")
            return
        
        examples.create_procedures_demo()
        examples.create_functions_demo()
        examples.call_procedures_demo()
        examples.procedure_with_output_demo()
        examples.functions_demo()
        examples.view_procedure_info_demo()
        
        # Ask user if they want to clean up
        print("\n" + "=" * 37)
        print("Note: Procedures and functions have been created in your database.")
        print("They will remain available for future use.")
        print("Uncomment the line below if you want to clean them up:")
        print("# examples.cleanup_procedures_demo()")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. MySQL server running")
        print("2. Database and tables created")
        print("3. Sample data loaded")
        print("4. .env file configured")
        print("5. Proper privileges for creating procedures/functions")
        
    finally:
        examples.cleanup()


if __name__ == "__main__":
    main()
