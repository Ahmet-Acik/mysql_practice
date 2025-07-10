"""
MySQL Practice Project - REST API
Simple REST API using Flask to interact with the MySQL database.
"""

import sys
import os
from typing import Optional, Dict, Any, List
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class DatabaseAPI:
    """REST API for database operations."""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for all routes
        self.db: Optional[MySQLConnection] = None
        self.setup_routes()
    
    def get_db(self) -> Optional[MySQLConnection]:
        """Get database connection."""
        if not self.db:
            self.db = MySQLConnection()
            if not self.db.connect():
                return None
        return self.db
    
    def setup_routes(self):
        """Setup API routes."""
        
        @self.app.route('/')
        def index():
            """API documentation page."""
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>MySQL Practice API</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                    .endpoint { background: #f4f4f4; padding: 10px; margin: 10px 0; border-radius: 5px; }
                    .method { color: #fff; padding: 4px 8px; border-radius: 3px; font-size: 12px; }
                    .get { background: #61affe; }
                    .post { background: #49cc90; }
                    .put { background: #fca130; }
                    .delete { background: #f93e3e; }
                    h1 { color: #333; }
                    h2 { color: #555; border-bottom: 2px solid #ddd; }
                    code { background: #f8f8f8; padding: 2px 4px; border-radius: 3px; }
                </style>
            </head>
            <body>
                <h1>🗄️ MySQL Practice API</h1>
                <p>RESTful API for the MySQL Practice Database</p>
                
                <h2>📊 Database Statistics</h2>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/stats</code> - Get database statistics
                </div>
                
                <h2>👥 Customers</h2>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/customers</code> - List all customers
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/customers/{id}</code> - Get customer by ID
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/customers/{id}/orders</code> - Get customer orders
                </div>
                
                <h2>🛍️ Products</h2>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/products</code> - List all products
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/products/{id}</code> - Get product by ID
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/products/category/{category}</code> - Get products by category
                </div>
                
                <h2>📦 Orders</h2>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/orders</code> - List recent orders
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/orders/{id}</code> - Get order details
                </div>
                
                <h2>📈 Analytics</h2>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/analytics/sales-by-month</code> - Monthly sales data
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/analytics/top-products</code> - Best selling products
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/analytics/customer-segments</code> - Customer segmentation
                </div>
                
                <h2>🔍 Search</h2>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/search/customers?q={query}</code> - Search customers
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <code>/api/search/products?q={query}</code> - Search products
                </div>
                
                <h2>📊 Example Usage</h2>
                <p>Try these endpoints:</p>
                <ul>
                    <li><a href="/api/stats" target="_blank">/api/stats</a> - Database overview</li>
                    <li><a href="/api/customers?limit=5" target="_blank">/api/customers?limit=5</a> - First 5 customers</li>
                    <li><a href="/api/products?limit=10" target="_blank">/api/products?limit=10</a> - First 10 products</li>
                    <li><a href="/api/analytics/sales-by-month" target="_blank">/api/analytics/sales-by-month</a> - Sales analytics</li>
                </ul>
            </body>
            </html>
            """
            return html
        
        @self.app.route('/api/stats')
        def get_stats():
            """Get database statistics."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                stats = {}
                
                # Table counts
                tables = ['customers', 'products', 'categories', 'orders', 'order_items']
                for table in tables:
                    result = db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                    stats[f"{table}_count"] = result[0]['count'] if result else 0
                
                # Recent activity
                recent_orders = db.execute_query(
                    "SELECT COUNT(*) as count FROM orders WHERE order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)"
                )
                stats['recent_orders_30_days'] = recent_orders[0]['count'] if recent_orders else 0
                
                # Total revenue
                revenue = db.execute_query("SELECT SUM(total_amount) as total FROM orders")
                stats['total_revenue'] = float(revenue[0]['total']) if revenue and revenue[0]['total'] else 0
                
                return jsonify(stats)
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/customers')
        def get_customers():
            """Get customers with pagination."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                limit = request.args.get('limit', 50, type=int)
                offset = request.args.get('offset', 0, type=int)
                
                query = """
                SELECT customer_id, first_name, last_name, email, city, state
                FROM customers
                ORDER BY customer_id
                LIMIT %s OFFSET %s
                """
                
                customers = db.execute_query(query, (limit, offset))
                
                # Get total count
                count_result = db.execute_query("SELECT COUNT(*) as total FROM customers")
                total = count_result[0]['total'] if count_result else 0
                
                return jsonify({
                    "customers": customers or [],
                    "total": total,
                    "limit": limit,
                    "offset": offset
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/customers/<int:customer_id>')
        def get_customer(customer_id: int):
            """Get customer by ID."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query = """
                SELECT customer_id, first_name, last_name, email, phone, 
                       address, city, state, zip_code
                FROM customers
                WHERE customer_id = %s
                """
                
                result = db.execute_query(query, (customer_id,))
                
                if not result:
                    return jsonify({"error": "Customer not found"}), 404
                
                return jsonify(result[0])
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/customers/<int:customer_id>/orders')
        def get_customer_orders(customer_id: int):
            """Get orders for a customer."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query = """
                SELECT o.order_id, o.order_date, o.status, o.total_amount,
                       COUNT(oi.order_item_id) as item_count
                FROM orders o
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.customer_id = %s
                GROUP BY o.order_id, o.order_date, o.status, o.total_amount
                ORDER BY o.order_date DESC
                """
                
                orders = db.execute_query(query, (customer_id,))
                
                return jsonify({"orders": orders or []})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/products')
        def get_products():
            """Get products with pagination."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                limit = request.args.get('limit', 50, type=int)
                offset = request.args.get('offset', 0, type=int)
                category = request.args.get('category')
                
                base_query = """
                SELECT p.product_id, p.product_name, p.price, p.stock_quantity,
                       p.sku, c.category_name
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                """
                
                if category:
                    query = base_query + " WHERE c.category_name = %s ORDER BY p.product_name LIMIT %s OFFSET %s"
                    products = db.execute_query(query, (category, limit, offset))
                    
                    count_query = "SELECT COUNT(*) as total FROM products p JOIN categories c ON p.category_id = c.category_id WHERE c.category_name = %s"
                    count_result = db.execute_query(count_query, (category,))
                else:
                    query = base_query + " ORDER BY p.product_name LIMIT %s OFFSET %s"
                    products = db.execute_query(query, (limit, offset))
                    
                    count_result = db.execute_query("SELECT COUNT(*) as total FROM products")
                
                total = count_result[0]['total'] if count_result else 0
                
                return jsonify({
                    "products": products or [],
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "category": category
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/analytics/sales-by-month')
        def get_sales_by_month():
            """Get monthly sales analytics."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query = """
                SELECT 
                    DATE_FORMAT(order_date, '%Y-%m') as month,
                    COUNT(DISTINCT order_id) as order_count,
                    COUNT(DISTINCT customer_id) as customer_count,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value
                FROM orders
                GROUP BY DATE_FORMAT(order_date, '%Y-%m')
                ORDER BY month DESC
                LIMIT 12
                """
                
                sales_data = db.execute_query(query)
                
                return jsonify({"monthly_sales": sales_data or []})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/analytics/top-products')
        def get_top_products():
            """Get best selling products."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                limit = request.args.get('limit', 10, type=int)
                
                query = """
                SELECT 
                    p.product_name,
                    c.category_name,
                    p.price,
                    SUM(oi.quantity) as total_sold,
                    SUM(oi.total_price) as total_revenue,
                    COUNT(DISTINCT oi.order_id) as order_count
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                JOIN order_items oi ON p.product_id = oi.product_id
                GROUP BY p.product_id, p.product_name, c.category_name, p.price
                ORDER BY total_sold DESC
                LIMIT %s
                """
                
                top_products = db.execute_query(query, (limit,))
                
                return jsonify({"top_products": top_products or []})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/search/customers')
        def search_customers():
            """Search customers by name or email."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query_param = request.args.get('q', '').strip()
                if not query_param:
                    return jsonify({"error": "Query parameter 'q' is required"}), 400
                
                search_query = """
                SELECT customer_id, first_name, last_name, email, city, state
                FROM customers
                WHERE first_name LIKE %s 
                   OR last_name LIKE %s 
                   OR email LIKE %s
                   OR CONCAT(first_name, ' ', last_name) LIKE %s
                ORDER BY last_name, first_name
                LIMIT 20
                """
                
                search_term = f"%{query_param}%"
                results = db.execute_query(search_query, (search_term, search_term, search_term, search_term))
                
                return jsonify({"customers": results or [], "query": query_param})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/search/products')
        def search_products():
            """Search products by name or description."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query_param = request.args.get('q', '').strip()
                if not query_param:
                    return jsonify({"error": "Query parameter 'q' is required"}), 400
                
                search_query = """
                SELECT p.product_id, p.product_name, p.price, p.stock_quantity,
                       p.sku, c.category_name
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                WHERE p.product_name LIKE %s 
                   OR p.description LIKE %s
                   OR p.sku LIKE %s
                ORDER BY p.product_name
                LIMIT 20
                """
                
                search_term = f"%{query_param}%"
                results = db.execute_query(search_query, (search_term, search_term, search_term))
                
                return jsonify({"products": results or [], "query": query_param})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Endpoint not found"}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({"error": "Internal server error"}), 500
    
    def run(self, host='127.0.0.1', port=5000, debug=True):
        """Run the API server."""
        print(f"🚀 Starting MySQL Practice API...")
        print(f"📍 Server running at: http://{host}:{port}")
        print(f"📖 API Documentation: http://{host}:{port}")
        print(f"🔍 Example: http://{host}:{port}/api/stats")
        
        self.app.run(host=host, port=port, debug=debug)


def main():
    """Start the API server."""
    print("🌐 MySQL Practice REST API")
    print("=" * 30)
    
    try:
        # Test database connection first
        db = MySQLConnection()
        if not db.connect():
            print("❌ Failed to connect to database. Please check your configuration.")
            print("Make sure MySQL is running and .env file is configured correctly.")
            return
        db.disconnect()
        print("✅ Database connection successful")
        
        # Start API server
        api = DatabaseAPI()
        api.run(host='127.0.0.1', port=5000, debug=True)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except ImportError:
        print("❌ Flask not installed. Install with: pip install flask flask-cors")
    except Exception as e:
        print(f"❌ Error starting server: {e}")


if __name__ == "__main__":
    main()
